from music21 import *
from dumper import *

# i = interval.Interval()
# j = interval.Interval()

n1 = note.Note('c3')
n2 = note.Note('d3')
n3 = note.Note('e3')
n4 = note.Note('f3')
n5 = note.Note('g3')
n6 = note.Note('a3')
n7 = note.Note('b3')
aInterval = interval.Interval(noteStart=n1, noteEnd=n2)
print(aInterval)
aInterval = interval.Interval(noteStart=n1, noteEnd=n3)
print(aInterval)
aInterval = interval.Interval(noteStart=n1, noteEnd=n4)
print(aInterval)
aInterval = interval.Interval(noteStart=n1, noteEnd=n5)
print(aInterval)
aInterval = interval.Interval(noteStart=n1, noteEnd=n6)
print(aInterval)
aInterval = interval.Interval(noteStart=n1, noteEnd=n7)
print(aInterval)

# aInterval.name
# aInterval.noteStart is n1
# aInterval.noteEnd is n2