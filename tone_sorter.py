# -*- coding: utf-8 -*-

from sys import argv
from operator import itemgetter, attrgetter
import csv

script, unsorted_file = argv

def extract_tone(syllable_with_tone):
    tone = int(syllable_with_tone[-1])
    syllable = syllable_with_tone[:-1]
    return (syllable, tone)

def format_phrase(phrase):
    syllables = phrase.split(" ")
    syllables_and_tones = [extract_tone(syllable) for syllable in syllables]
    return (len(syllables_and_tones), syllables_and_tones)

phrases = []
with open(unsorted_file, 'rb') as csvfile:
    tonereader = csv.reader(csvfile)
    for row in tonereader:
        _, _, _, phrase, _ = row
        phrases.append(format_phrase(phrase))

for phrase in phrases:
    print phrase