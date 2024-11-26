import unittest
from app import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_sum(self):
        payload = {'num1': 2, 'num2': 2}
        response = self.app.post('/sum', json=payload)
        data = response.get_json()
        self.assertEqual(data['result'], 4)

    def test__get_all_resultNum(self):  # this test proves the filter does find a result that does exist
        result = 6    # ensure this result does exist within the database
        response = self.app.get(f'/sum/{result}')
        data = response.get_json()
        # could also assert equal the response code, 200
        self.assertEqual(data[0]['result'], result)     # gets the first item from the list of returned results

    def test_negative_get_all_resultNum(self):  # this test proves the filter does not find a result that does not exist
        result = 2345678976543      # ensure this result does not exist within the database
        response = self.app.get(f'/sum/{result}')
        data = response.get_json()
        # could also assert equal the response code, 404
        self.assertEqual(data['message'], 'Result not found')

if __name__ == "__main__":
    unittest.main()

