

# Import music21.base namespace so we avoid name collisions, e.g., between local symbol "note"
# and "music21.note"
import music21
from music21 import *
# from re import *
import re
from dumper import *

import traceback

key_sig_re = r'\[([A-Z])\](\[([b.])([b.])([b.])([b.])([b.])([b.])([b.])\])?'

# Default to major key (ionian mode)
tonic = 'C'
tonicNote = music21.note.Note(tonic)

# Needed to compute intervals from tonic
perfect_major_minor_dict = {
  "b1"  : 'diminished',
  "1"   : 'perfect',
  "#1"  : 'augmented',
  "n1"  : 'perfect',
  "b2"  : 'minor',
  "n2"  : 'major',
  "2"   : 'major',
  "b3"  : 'minor',
  "n3"  : 'major',
  "3"   : 'major',
  "b4"  : 'diminished',
  "n4"  : 'perfect',
  "4"   : 'perfect',
  "n4"  : 'perfect',
  "#4"  : 'augmented',
  "b5"  : 'diminished',
  "n5"  : 'perfect',
  "5"   : 'perfect',
  "#5"  : 'augmented',
  "nb6" : 'minor',
  "b6"  : 'minor',
  "n6"  : 'major',
  "6"   : 'major',
  "b7"  : 'minor',
  "n7"  : 'major',
  "7"   : 'major'
};

#######################################################################################
def getModalTonality(s):

  tonic = 'C'

  # m = re.search()
  # m.group(0) = '[C][..b..bb]'
  # m.group(1) = 'C'
  # m.group(2) = '[..b..bb]'
  # m.group(3) = '.'
  # m.group(4) = '.'
  # m.group(5) = 'b'
  # m.group(6) = '.'
  # m.group(7) = '.'
  # m.group(8) = 'b'
  # m.group(9) = 'b'
  # m.group(10) = No such group!

  re_match_key_sig = re.match(key_sig_re, s)
  if re_match_key_sig.group(1):
    tonic = re_match_key_sig.group(1)

    # We're only handling minor mode right now
    mode = 'major'
    if re_match_key_sig.group(5) == 'b':
      mode = 'minor'
      perfect_major_minor_dict["3"] = 'minor'

    if re_match_key_sig.group(8) == 'b':
      perfect_major_minor_dict["6"] = 'minor'

    if re_match_key_sig.group(9) == 'b':
      perfect_major_minor_dict["7"] = 'minor'

  return [tonic, mode]

#######################################################################################

filepath = '/Library/WebServer/Documents/iqss/rock_corpus/annotations/rs200_melody/all_along_the_watchtower_dt.mel'
with open(filepath) as fp:

  p1 = music21.stream.Part()
  p1.id = 'part1'

  sc = music21.stream.Score([p1])
  sc.insert(0, metadata.Metadata())

  # This looks a little odd because python doesn't let us conditionalize our while loop
  # on an assignment expression, e.g., line = fp.readline()
  while True:
    line = fp.readline()
    if not line:
      break

    print("Line " + line)

    # % All Along the Watchtower
    re_search_song_title = re.search(r'%\s+(.*)', line)
    if re_search_song_title and re_search_song_title.group(1) and not sc.metadata.title:
      sc.metadata.title = re_search_song_title.group(1)
      continue

    if re.match(key_sig_re, line):
      tonic, mode = getModalTonality(line)
      tonicNote = music21.note.Note(tonic)
      continue

    # [C][..b..bb] [OCT = 4] R * 9 |
    key_header_re = re.compile(r"""\[([A-Z][^\]]*)\]\s*   # Tonic of key signature
                                   \[OCT\s*=\s*(\d)\]\s*  # the octave of the melody
                                   R\s+\*\s+\d+           # Something about section repeats? """, re.X)

    re_search_key_header = re.search(key_header_re, line)
    if re_search_key_header and re_search_key_header.group(1) and not sc.metadata.title:
      sc.metadata.title = m.group(1)
      continue

    m = re.search(r'\|', line)

    if m is None:
      continue

    try:
      measure_re = r'([^\|]+)\|'
      m = re.match(measure_re, line)
      measure = m.group(0)
      print("Measure: {}".format(measure.strip()))

      measures = re.findall(r'([^\|]+)\|', line)
      for measure in measures:

        # Measures are delineated by |'s, so create a new measure for each string between the |'s
        print("measure = " + measure)
        measureObj = music21.stream.Measure()

        # v - transpose down the octave
        # ^ - transpose up the octave
        # n - natural note (e.g., when contradicting a flat note in the key signature)
        # b - flattened note
        # # - sharpened note
        notes = re.findall(r'([a-z^]*\d\s*|[\. ]*)', measure)
        for note in notes:
          stripped_note = note.strip()
          print("note = " + stripped_note)

          # Add a note or rest to the measure
          n1 = None

          if re.match(r'\d', stripped_note):
            intervalValue = re.findall(r'\d', stripped_note)[0]
            intervalType = perfect_major_minor_dict[stripped_note]
            n1 = tonicNote.transpose(interval.DiatonicInterval(intervalType, int(intervalValue)))
          elif re.match(r'\.', stripped_note):
            numEighthNotes = len(re.findall(r'\.', stripped_note))
            n1 = music21.note.Rest(quarterLength=(0.5 * numEighthNotes))

          # Add note to the melody part line
          if n1 is not None:
            measureObj.append(n1)

        # Add the measure to the part
        p1.append([measureObj])

    # If there are no measures to read in, read the next line
    except Exception as e:
      print(traceback.format_exc())
      #print("e = " + str(e))
      print("No measures in this line: " + line)

# Write stream to MusicXML file
sc.show()
sc.show('text')
sc.write("musicxml", "test.musicxml")