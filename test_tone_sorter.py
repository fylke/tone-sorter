import unittest
from tone_sorter import *
 
class TestToneSorter(unittest.TestCase):
    def setUp(self):
        pass
 
    def test_extract_tone(self):
        self.assertEqual(extract_tone("ni3"), ("ni", 3))


 
if __name__ == '__main__':
    unittest.main()