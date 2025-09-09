import unittest
from src.process import clean_data

class TestProcess(unittest.TestCase):
    def test_clean_data(self):
        data = [{'date': '2023-01-01', 'phone': '1234567890', 'amount': 100.0}]
        cleaned = clean_data(data)
        self.assertEqual(cleaned[0]['phone'], '+1234567890')

if __name__ == '__main__':
    unittest.main()