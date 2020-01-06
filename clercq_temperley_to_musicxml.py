from music21 import *
# from re import *
import re
from dumper import *

key_sig_re = r'\[([A-Z])\](\[([b.])([b.])([b.])([b.])([b.])([b.])([b.])\])?'

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

  return [tonic, mode]

#######################################################################################

filepath = '/Library/WebServer/Documents/iqss/rock_corpus/annotations/rs200_melody/all_along_the_watchtower_dt.mel'
with open(filepath) as fp:

  sc = stream.Score()
  sc.insert(0, metadata.Metadata())

  p1 = stream.Part()
  p1.id = 'part1'

  while True:
    line = fp.readline()
    if not line:
      break

    print("Line " + line)

    # TODO: Parse score header for attributes like key, title, composer, octave range, etc.

    # % All Along the Watchtower
    re_search_song_title = re.search(r'%\s+(.*)', line)
    if re_search_song_title and re_search_song_title.group(1) and not sc.metadata.title:
      sc.metadata.title = re_search_song_title.group(1)
      continue


    if re.match(key_sig_re, line):
      tonic, mode = getModalTonality(line)
      continue

    # [C][..b..bb] [OCT = 4] R * 9 |
    key_header_re = re.compile(r"""\[([A-Z][^\]]*)\]\s*   # Tonic of key signature
                                   \[OCT\s*=\s*(\d)\]\s*  # the octave of the melody
                                   R\s+\*\s+\d+           # Something about section repeats? """, re.X)

    re_search_key_header = re.search(key_header_re, line)
    if re_search_key_header and re_search_key_header.group(1) and not sc.metadata.title:
      sc.metadata.title = m.group(1)
      continue

    n1 = note.Note('C4')
    n2 = note.Note('D4')
    p1.append(n1)
    p1.append(n2)

    m = re.search(r'\|', line)

    if m is None:
      # FIXME:  Can we read the next line in just one place?
      continue

    try:
      measure_re = r'([^\|]+)\|'
      m = re.match(measure_re, line)
      measure = m.group(0)
      print("Measure: {}".format(measure.strip()))

      measures = re.findall(r'([^\|]+)\|', line)
      for measure in measures:

        # TODO: Add measure to stream score

        print("measure = " + measure)

        # v - transpose down the octave
        # ^ - transpose up the octave
        # n - natural note (e.g., when contradicting a flat note in the key signature)
        # b - flattened note
        # # - sharpened note
        notes = re.findall(r'[a-z^]*\d[\. ]*', measure)
        for note in notes:
          print("note = " + note)

          # TODO: Add notes to measure

          # FIXME: compute note value as interval from tonic of key signature to parsed integer value
          n1 = note.Note('?')
          p1.append(n1)


    # If there are no measures to read in, read the next line
    except:
      print("No measures in this line: " + line)
