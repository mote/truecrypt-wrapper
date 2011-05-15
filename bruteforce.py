#!/usr/bin/python
"""Bruteforce a truecrypt volume by trying ordered words.

I had a truecrypt volume where I knew the passphrase was a line (or part of
a line) from a poem.
Unfortunately, I didn't know which line.

This brute-forces trying all n-grams from length 4-10 words from a dictionary
file.

It tries the original text, the text stripped of whitespace, and the text
stripped of non-alphanumeric characters.
"""
import os

import truecrypt

DICTIONARY_FILE = '/home/mote/dev/truecrypt/poems.txt'
TARGET_FILE='/home/mote/dls/volume.tpt'

MOUNT_PT = '/home/mote/dev/truecrypt/dest'

def removeNonAlpha(s, include_spaces=True):
  if include_spaces:
    return "".join(i for i in s if i.isalpha() or i.isdigit() or i == ' ')
  else:
    return "".join(i for i in s if i.isalpha() or i.isdigit())

def try_candidate(passwd):
  #print 'trying: ', passwd
  if truecrypt.mount(TARGET_FILE, passwd, MOUNT_PT):
    print '******Found! ', passwd
    return True
  return False

def permute(candidate):
  candidates = [
    candidate,
    removeNonAlpha(candidate),
    removeNonAlpha(candidate, False)]
  candidates.extend([c.lower() for c in candidates])
  return candidates


def generate_all_candidates_of_length(dictionary_file, minlen=4, maxlen=10):
  contents = open(dictionary_file).read()
  words = contents.split()
  for n in range(minlen, maxlen):
    already = set()
    for i in range(len(words)):
      candidate = ' '.join(words[i:i+n])
      for c in permute(candidate):
        if c in already:
          continue
        yield c
        already.add(c)

def generate_all_sentence_candidates(dictionary_file):
  already = set()
  for line in open(dictionary_file):
    line = line.strip()
    candidates = permute(line)
    for c in candidates:
      if c in already:
        continue
      yield c
      already.add(c)


def try_all(dictionary_file):
  #for c in generate_all_sentence_candidates(dictionary_file):
  for c in generate_all_candidates_of_length(dictionary_file):
    print '> ', c
    if try_candidate(c):
      return c
  return ''

try_all(DICTIONARY_FILE)

truecrypt.dismount()
os.rmdir(MOUNT_PT)
