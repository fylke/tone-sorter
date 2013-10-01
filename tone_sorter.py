# -*- coding: utf-8 -*-

from sys import argv
from operator import itemgetter
import ucsv as csv

script, unsorted_file, sorted_file = argv

def construct_sort_value(reversed_phrase, multiplicator, sort_value):
    if not reversed_phrase:
        return sort_value
    else:
        (_syllable, tone), tail = reversed_phrase[0], reversed_phrase[1:]
        return construct_sort_value(tail, multiplicator * 10,
                                    sort_value + tone * multiplicator)

def extract_tone(syllable_with_tone):
    tone = int(syllable_with_tone[-1])
    syllable = syllable_with_tone[:-1]
    return (syllable, tone)

def annotate_phrase(phrase):
    syllables = phrase.split(" ")
    syllables_and_tones = [extract_tone(syllable) for syllable in syllables]
    sort_value = construct_sort_value(syllables_and_tones[::-1], 1, 0)
    (first_syllable, _tone) = syllables_and_tones[0]
    return (sort_value, first_syllable)

def deannotate_phrase(annotated_phrase):
    (_, _, hanzi_phrase, annotated_pinyin_phrase)= annotated_phrase
    deannotated_pinyin_phrase = [syllable[0:-1] for syllable in annotated_pinyin_phrase]
    print "".join(repr(deannotated_pinyin_phrase))
    return deannotated_pinyin_phrase

phrases = []
with open(unsorted_file, 'rb') as csvfile:
    tonereader = csv.reader(csvfile)
    for row in tonereader:
        _, _, hanzi_phrase, pinyin_phrase, _, _ = row
        (sort_value, first_syllable) = annotate_phrase(pinyin_phrase)
        phrases.append((sort_value, first_syllable, hanzi_phrase, pinyin_phrase))

sorted_phrases = sorted(phrases, key = itemgetter(0, 1))

output_ready_phrases = [phrase[2:4] for phrase in sorted_phrases]

with open(sorted_file, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(output_ready_phrases)