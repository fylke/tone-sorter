# -*- coding: utf-8 -*-

import unittest
from tone_sorter import *
 
class TestToneSorter(unittest.TestCase):
    def setUp(self):
        pass
 
    def test_extract_tone(self):
        self.assertEqual(extract_tone("ni3"), ("ni", 3))
        self.assertEqual(extract_tone("ni"), ("ni", 5))

    def test_sanitize_file(self):
        test_file = "lingomi_file.csv"
        with open(test_file, "w") as f:
            f.write("http://lingomi.com, bork bork\n")
            row2 = "row 2, row 2"
            f.write(row2)

        sanitized_file = sanitize_file(test_file)
        self.assertTrue(sanitized_file.endswith("sanitized.csv"))
        with open(sanitized_file, 'r') as f:
            content = f.read()
            self.assertEqual(content, row2)
        os.remove(sanitized_file)
        os.remove(test_file)

    def test_annotate_phrase(self):
        self.assertEqual([("ba", 4), ("ba", 5)],
                         annotate_phrase("ba4 ba5"))
        self.assertEqual([("ba", 4), ("ba", 5)],
                         annotate_phrase("ba4 ba"))
        self.assertEqual([("ba", 4), ("ba", 5)],
                         annotate_phrase("ba4ba5"))

    def test_main(self):
        sdf = "dsdf" #self.get_sorted_content()
        print sdf

    def get_sorted_content():
        return """
               八,ba1
               茶,cha2
               本,ben3
               爱,ai4
               不,bu4
               菜,cai4
               杯子,bei1 zi5
               北京,Bei3 jing1
               爸爸,ba4 ba5
               不客气,bu4 ke4 qi5
               """
 
if __name__ == '__main__':
    unittest.main()