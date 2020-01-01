from music21 import *
from dumper import *
url = '/Users/hmdcadministrator/Documents/MuseScore3/Scores/Paint_It_Black2.musicxml'
score = converter.parse(url)
print(score.notes)
#noteFilter = stream.filters.ClassFilter('Note')
#score.notes.addFilter(noteFilter)

# dump(score)

# FIXME: How does python know to use MuseScore for showing MusicXML?
# score.show()
print(score.flat.notes)

for el in score.recurse().notes:
    print(el)

# dump(sAlt)
# sAlt.show()


