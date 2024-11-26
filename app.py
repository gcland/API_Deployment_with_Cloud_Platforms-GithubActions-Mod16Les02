from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

app = Flask(__name__)
ma = Marshmallow(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sum_postgres_user:ps97xpQesk6Ze8s51qR5WYsIIkI1aU9d@dpg-ct2utqu8ii6s73b2jfhg-a.oregon-postgres.render.com/sum_postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)

class Sum(Base):
    __tablename__ = "Sum"
    id: Mapped[int] = mapped_column(primary_key=True)
    num1: Mapped[int] = mapped_column(db.Integer, nullable=False)
    num2: Mapped[int] = mapped_column(db.Integer, nullable=False)
    result: Mapped[int] = mapped_column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Sum {self.id}: {self.num1} + {self.num2} {self.result}>'
    
class SumSchema(ma.Schema):
    id = fields.Integer()
    num1 = fields.Integer()
    num2 = fields.Integer()
    result = fields.Integer()

sums_schema = SumSchema(many=True)

@app.route('/sum', methods=['GET'])
def find_all():
    sums = db.session.execute(db.select(Sum)).scalars()
    return sums_schema.jsonify(sums), 200

@app.route('/sum', methods=['POST'])
def sum():
    data = request.get_json()
    num1 = data['num1']
    num2 = data['num2']
    result = num1 + num2

    with Session(db.engine) as session:
        with session.begin():
            sum_entry = Sum(num1=num1, num2=num2, result=result)    #saves result and nums into database
            session.add(sum_entry)

    return jsonify({'result': result}), 201

@app.route('/sum/<int:result>', methods=['GET'])
def get_all_resultNum(result):
    with Session(db.engine) as session:
        with session.begin():
            results = (db.session.execute(db.select(Sum).where(Sum.result == result)).scalars().all())
    if results:
        return (sums_schema.jsonify(results)), 200
    else:
        return jsonify({"message": "Result not found"}), 404

with app.app_context():
    # db.drop_all()
    db.create_all()


# Activate for testing with postman
# if __name__ == '__main__':
#     app.run(debug=True)


# @app.route('/sum', methods=['POST'])
# def sum():
#     data = request.get_json()
#     num1 = data['num1']
#     num2 = data['num2']
#     result = num1 + num2
#     return jsonify({'result': result})