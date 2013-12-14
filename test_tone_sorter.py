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

    def test_calc_sort_value(self):
        self.assertEqual(44, calc_sort_value([('dou', 4), ('lü', 4)], 1, 0))
        self.assertEqual(4, calc_sort_value([('lüe', 4)], 1, 0))
        self.assertEqual(34, calc_sort_value([('xing', 4), ('nü', 3)], 1, 0))

    def test_annotate_phrase(self):
        self.assertEqual([("ba", 4), ("ba", 5)],
                         annotate_phrase("ba4 ba5"))
        self.assertEqual([("ba", 4), ("ba", 5)],
                         annotate_phrase("ba4 ba"))
        self.assertEqual([("ba", 4), ("ba", 5)],
                         annotate_phrase("ba4ba5"))
        self.assertEqual([("nü", 3), ("xing", 4)],
                         annotate_phrase("nü3xing4"))
        # There is a corner case when it comes to the character 儿. 小孩儿 is 
        # pronounced xiao3hai2r but the dangling 'r' is actually merged with
        # the second syllable when you pronounce it. So with regards to sorting
        # we pretend it isn't there.
        self.assertEqual([("xiao", 3), ("hai", 2)],
                         annotate_phrase("xiao3hai2r"))
        self.assertRaises(ValueError, annotate_phrase, "")
        self.assertRaises(ValueError, annotate_phrase, "13-11-01")

    def test_main(self):
        input_file = "test_input.csv"
        with open(input_file, "w") as i:
            i.write(self.get_unsorted_content())
        output_file = "test_output.csv"
        main(["-i", input_file, "-o", output_file])
        with open(output_file, 'r') as o:
            lines = o.readlines()
            self.assertEqual(self.get_sorted_content(), lines)


    def get_sorted_content(self):
        return """Word,Pronunciation
八,ba1
茶,cha2
本,ben3
爱,ai4
不,bu4
菜,cai4
略,lüe4
杯子,bei1 zi5
北京,Bei3 jing1
女性,nü3xing4
綠豆,lü4dou4
爸爸,ba4 ba5
不客气,bu4 ke4 qi5
"""
    
    def get_unsorted_content(self):
        return """Word,Pronunciation
爱,ai4
爸爸,ba4 ba5
杯子,bei1 zi5
本,ben3
不客气,bu4 ke4 qi5
菜,cai4
綠豆,lü4dou4
略,lüe4
女性,nü3xing4
不,bu4
八,ba1
北京,Bei3 jing1
茶,cha2
"""

if __name__ == '__main__':
    unittest.main()