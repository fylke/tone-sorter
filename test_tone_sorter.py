# -*- coding: utf-8 -*-

import unittest, codecs
from tone_sorter import *
 
class TestToneSorter(unittest.TestCase):
    def setUp(self):
        pass
 
    def test_extract_tone(self):
        self.assertEqual(extract_tone(u'ni3'), (u'ni', 3))
        self.assertEqual(extract_tone(u'ni'), (u'ni', 5))

    def test_sanitize_file(self):
        test_file = 'lingomi_file.csv'
        with open(test_file, 'w') as f:
            f.write(u'http://lingomi.com, bork bork\n')
            row2 = u'row 2, row 2'
            f.write(row2)

        sanitized_file = sanitize_file(test_file)
        self.assertTrue(sanitized_file.endswith(u'sanitized.csv'))
        with open(sanitized_file, 'r') as f:
            content = f.read()
            self.assertEqual(content, row2)
        os.remove(sanitized_file)
        os.remove(test_file)

    def test_calc_sort_value(self):
        self.assertEqual(44, calc_sort_value([(u'dou', 4), (u'lü', 4)], 1, 0))
        self.assertEqual(4, calc_sort_value([(u'lüe', 4)], 1, 0))
        self.assertEqual(34, calc_sort_value([(u'xing', 4), (u'nü', 3)], 1, 0))

    def test_annotate_phrase(self):
        self.assertEqual([(u'ba', 4), (u'ba', 5)],
                         annotate_phrase(u'ba4 ba5'))
        self.assertEqual([(u'ba', 4), (u'ba', 5)],
                         annotate_phrase(u'ba4 ba'))
        self.assertEqual([(u'ba', 4), (u'ba', 5)],
                         annotate_phrase(u'ba4ba5'))
        self.assertEqual([(u'nü', 3), (u'xing', 4)],
                         annotate_phrase(u'nü3xing4'))
        # There is a corner case when it comes to the character 儿. 小孩儿 is 
        # pronounced xiao3hai2r but the dangling 'r' is actually merged with
        # the second syllable when you pronounce it. So with regards to sorting
        # we pretend it isn't there.
        self.assertEqual([(u'xiao', 3), (u'hai', 2)],
                         annotate_phrase(u'xiao3hai2r'))
        self.assertRaises(ValueError, annotate_phrase, u'')
        self.assertRaises(ValueError, annotate_phrase, u'13-11-01')

    def test_main(self):
        input_file = 'test_input.csv'
        with codecs.open(input_file, encoding='utf-8', mode='w') as i:
            i.write(self.get_unsorted_content())
        output_file = 'test_output.csv'
        main(['-i', input_file, '-o', output_file])
        with codecs.open(output_file, encoding='utf-8', mode='r') as o:
            lines = o.readlines()
            stripped_lines = [line.strip() for line in lines]
            self.assertEqual(self.get_sorted_content(), stripped_lines)
        os.remove(input_file)
        os.remove(output_file)


    def get_sorted_content(self):
        return [u'Word,Pronunciation',
                u'八,ba1',
                u'茶,cha2',
                u'本,ben3',
                u'爱,ai4',
                u'不,bu4',
                u'菜,cai4',
                u'略,lüe4',
                u'杯子,bei1 zi5',
                u'北京,Bei3 jing1',
                u'女性,nü3xing4',
                u'綠豆,lü4dou4',
                u'爸爸,ba4 ba5',
                u'不客气,bu4 ke4 qi5']

    def get_unsorted_content(self):
        return u"""Word,Pronunciation
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