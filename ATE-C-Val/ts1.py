#!/usr/bin/env python2
#encoding: UTF-8

import ahocorasick

A = ahocorasick.Automaton()
for idx, key in enumerate('he her hers she'.split()):
    print idx, key
    A.add_word(key, (idx, key))
