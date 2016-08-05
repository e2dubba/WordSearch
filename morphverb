#!/usr/bin/env python3

import re
import sys
import subprocess

BIBLE = '2TGreek'

def diatheke(key, module=BIBLE, options='cva', search_type=None, scope=None):
    """wraps most of diatheke. -r (range) is called scope."""
    cmd = 'diatheke -b %s' % (module)
    if options is not None: cmd = '%s -o %s' % (cmd, options)
    if search_type is not None: cmd = '%s -s %s' % (cmd, search_type)
    if scope is not None: cmd = '%s -r %s' % (cmd, scope)
    cmd = '%s -k %s 2> /dev/null' % (cmd, key)
    return subprocess.getoutput(cmd)

def verse_split(key, module, options=None):
    """
    Turns passages into lists of verses. Each verse is list with the reference
    at 0 and the text at 1.
    """
    passage = diatheke(key, module, options).split('\n')
    # delete module name from the diatheke result
    del passage[-1]
    verse_list = []
    for verse in passage:
        split = re.split(r'([\w ]+ \d+:\d+): ', verse)
        verse_list.append([split[1],split[2]])
    return verse_list

def get_tags(verse, dlmtr='()'):
    """
    The tagged (morph or Strong's) text of a verse as input and returns a
    list of lists of the word and the tag.
    """
    if dlmtr == '()':
        verse = re.sub(r'(.*[^A-Z])\)', r'\1', verse)
    verse =  re.split(r'\%s\W* ?' % dlmtr[1], verse)
    tag_list = [re.split('\W? \%s' % dlmtr[0], i) for i in verse]
    if len(tag_list[-1]) == 1:
        del tag_list[-1]
    return tag_list

def form_finder(match_form, color):
    forms = [word[0] for word in get_tags(tagged[verse][1])
            if re.search(match_form, word[1])]
    forms.sort(key=len)
    forms.reverse()
    for form in forms[::-1]:
        passage[verse][1] = re.sub(r'([^#]?)(%s)([^#?])' % form,
            r'\1[%s]##\2##\3' % color,
            passage[verse][1])


def bold_iti():
    indic_forms = [word[0] for word in get_tags(tagged[verse][1])
            if re.search('V-[A-Z][A-Z]I', word[1])]
    nonindic_forms = [word[0] for word in get_tags(tagged[verse][1])
            if re.search('V-[A-Z][A-Z][^I]', word[1])]
    for forms, tag in (indic_forms, '*'), (nonindic_forms, '_'):
        forms.sort(key=len)
        forms.reverse()
        for form in forms:
            passage[verse][1] = re.sub(
                    r'([^{0}]?)({1})([^{0}]?)'.format(tag, form),
                    r'\1{0}\2{0}\3'.format(tag),
                    passage[verse][1])

verb_dict = {
    'aorist': ['V-A[A-Z][A-Z]', 'red'],
    'imperfect': ['V-I[A-Z][A-Z]', 'navy'],
    'present': ['V-P[A-Z][A-Z]', 'blue'],
    'pluperfect': ['V-L[A-Z][A-Z]', 'green'],
    'perfective': ['V-R[A-Z][A-Z]', 'lime'],
    'future': ['V-F[A-Z][A-Z]', 'yellow'] }

if __name__ == '__main__': 
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('passage', nargs='*') 
    args = parser.parse_args()
    key = ' '.join(args.passage)

    passage = verse_split(key, 'MorphGNT', 'a')
    tagged = verse_split(key, 'MorphGNT', 'am') 
    print('.%s' % key) 
    for verse in range(len(tagged)):
         for key in verb_dict:
             match_form = verb_dict[key][0]
             color = verb_dict[key][1]
             form_finder(match_form, color) 
         bold_iti()
         print('%s%s' % ( 
             re.sub(r'[\w ]+ \d+:(\d+)', r'[gray]^\1^', passage[verse][0]), 
             passage[verse][1]))

