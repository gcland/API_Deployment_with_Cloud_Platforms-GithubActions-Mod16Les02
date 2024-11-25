import unittest
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_sum(self):
        payload = {'num1': -2, 'num2': -4}
        response = self.app.post('/sum', json=payload)
        data = response.get_json()
        self.assertEqual(data['result'], -6)

if __name__ == "__main__":
    unittest.main()

