#!/usr/bin/env python3

import morphverb
from morphverb import get_tags as gt
import re

def verse_list(key, module, options, search_type, scope=None):
    versenums = morphverb.diatheke(key, module, options, search_type, scope)
    versenums = re.split(r'--', versenums)
    del versenums[0]
    del versenums[-1]
    versenums = re.split(r';', versenums[0])
    return versenums 


def eng_tags(key, verse, dlmtr='<>'):
    """
    this is like get_tags in morphverb, but specially designed
    to deal with the bizareness of the KJVA 
    """
    verse = re.split(r'\%s\W* ?' % dlmtr[1], verse)
    ptag_list = [re.split(r'\W? \%s' % dlmtr[0], i) for i in verse]
    tag_list = [] 
    for word in ptag_list:
        if len(word) == 2:
            if re.search(key, word[1]):
                tag_list.append(word)
        else:
            del word
    return tag_list 


def versification(key, module, options):
    """
    This is like verse_split, but deals only with one verse input
    """  
    passage = morphverb.diatheke(key, module, options).split('\n')
    del passage[-1]
    if len(passage) == 2:
        passage = re.split(r'([\w ]+ \d+:\d+): ', passage[0])
        if passage[0] == '':
            del passage[0]
    if passage[-1] == '':
        del passage[-1]
    return passage 


if __name__ == '__main__':
    import argparse 
    parser = argparse.ArgumentParser()
    parser.add_argument('search_key', nargs='*')
    args = parser.parse_args()
    key = ' '.join(args.search_key)
    from xtermcolor import colorize 

    versenums = verse_list(key, module='MorphGNT', options='an', search_type='Phrase', scope=None)
    for verse in versenums: 
       tagged = morphverb.verse_split(verse, '2TGreek', options='an') 
       passage = morphverb.verse_split(verse, '2TGreek', options='a')
       forms = [word[0] for word in gt(tagged[0][1], dlmtr='<>')
               if re.search(key, word[1])]
       forms.sort(key=len)
       forms.reverse()
       for form in forms[::-1]:
           passage[0][1] = re.sub(form, colorize(form, ansi=1), passage[0][1])
       eng_pass = versification(verse, 'KJVA', options='a')
       eng_gloss = versification(verse, 'KJVA', options='n')
       eng_forms = [word[0] for word in eng_tags(key, eng_gloss[1], dlmtr='<>') ]
       eng_forms.sort(key=len)
       eng_forms.reverse()
       # eng_words = eng_tags(key, eng_gloss[1], dlmtr='<>') 
       # eng_words.sort(key=len)
       #eng_words.reverse()
       for word in eng_forms[::-1]:
           eng_pass[1] = re.sub(word, colorize(word, ansi=3), eng_pass[1])
       print(passage[0][0] + ' ' + passage[0][1]  + '\n' + 
               eng_pass[0] + ' ' + eng_pass[1] + '\n')

