# -*- coding: utf-8 -*-

"""
.. module:: tone_sorter
   :platform: Unix, Windows
   :synopsis: Takes a CSV file containing Hanzi and Pinyin phrases annotated 
              with tones and sorts them in descending order. Phrases with
              more syllables gets sorted after phrases with fewer. A phrase
              with the tones 2, 1, 2 gets sorted before one with 2, 2, 1. If
              the tones are the same, it will sort them alphabetically
              according to the first syllable.

              The input file must have the fields 'Word' and 'Pronunciation',
              which must contain Hanzi in the former field and Pinyin in the
              latter and be encoded in utf-8.

.. moduleauthor:: Magnus Falk <magnus.falk@gmail.com>
"""

import sys, ucsv, getopt, os, re
from operator import itemgetter

def calc_sort_value(reversed_phrase, multiplicator, sort_value):
    if not reversed_phrase:
        return sort_value
    else:
        (_syllable, tone), tail = reversed_phrase[0], reversed_phrase[1:]
        return calc_sort_value(tail, multiplicator * 10,
                                    sort_value + tone * multiplicator)

def extract_tone(syllable_with_tone):
    if syllable_with_tone[-1].isdigit():
        tone = int(syllable_with_tone[-1])
        syllable = syllable_with_tone[:-1]
    else:
        tone = 5 # If no tone is given, we assume tone-less
        syllable = syllable_with_tone
    return (syllable, tone)

def annotate_phrase(phrase):
    if not phrase:
        raise ValueError
    # The input can look either like "Bei3 jing1" or like "Bei3jing1", this
    # takes care of both cases.
    syllables = re.findall('([a-zA-Z]+[1-5]?)', phrase)
    return [extract_tone(syllable) for syllable in syllables]

def sanitize_file(original_file):
    with open(original_file, 'r') as f:
        lines = f.readlines()
        # The lists from Lingomi have an improper first line that needs to go
        if lines[0].startswith("http://lingomi.com"):
            del lines[0]
            clean_file = original_file + "_sanitized.csv"
            out = open(clean_file, 'w')
            out.writelines(lines)
            out.close()
            return clean_file
        else:
            f.close()
            return original_file

def main(argv):
    inputfile = ""
    outputfile = ""
    try:
        opts, args = getopt.getopt(argv, 'hi:o:', ['ifile=','ofile='])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'tone_sorter.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg

    phrases = []
    try:
        cleaned_file = sanitize_file(inputfile)
        line_number = 1
        with open(cleaned_file, 'rb') as csvfile:
            for row in ucsv.DictReader(csvfile):
                line_number += 1
                pinyin_phrase = row["Pronunciation"]
                try:
                    annotated_pinyin = annotate_phrase(pinyin_phrase)
                except ValueError:
                    print "Bad pronunciation entry on line %d. " % line_number
                    continue
                sort_value = calc_sort_value(annotated_pinyin[::-1], 1, 0)
                (first_syllable, _tone) = annotated_pinyin[0]

                hanzi_phrase = row["Word"]
                phrases.append((sort_value, first_syllable,
                                hanzi_phrase, pinyin_phrase))
        if cleaned_file.endswith("sanitized.csv"):
            os.remove(cleaned_file)
    except IOError:
        if cleaned_file.endswith("sanitized.csv"):
            os.remove(cleaned_file)
        print "Bad input file:", inputfile 

    sorted_phrases = sorted(phrases, key = itemgetter(0, 1))

    output_ready_phrases = [phrase[2:4] for phrase in sorted_phrases]
    
    with open(outputfile, 'wb') as f:
        writer = ucsv.writer(f)
        writer.writerows(output_ready_phrases)

if __name__ == "__main__":
   main(sys.argv[1:])