
s1 = stream.Stream()
s1.append(note.Note('C#4', type='half'))
s1.append(note.Note('D5', type='quarter'))
s1.duration.quarterLength
# 3.0
for thisNote in s1.notes:
  print(thisNote.octave)
# ...
# 4
# 5
# This is a demonstration of creating a Stream with other elements, including embedded Streams (in this case, music21.stream.Part, a Stream subclass):
# 

c1 = clef.TrebleClef()
c1.offset = 0.0
c1.priority = -1
n1 = note.Note('E-6', type='eighth')
n1.offset = 1.0
p1 = stream.Part()
p1.offset = 0.0
p1.id = 'embeddedPart'
p1.append(note.Rest())  # quarter rest
s2 = stream.Stream([c1, n1, p1])
s2.duration.quarterLength
# 1.5
s2.show('text')
# {0.0} <music21.clef.TrebleClef>
# {0.0} <music21.stream.Part embeddedPart>
    # {0.0} <music21.note.Rest rest>
# {1.0} <music21.note.Note E->
# Stream bases
# 
# StreamCoreMixin
# 
# Music21Object
# 
# ProtoM21Object
# 
# Stream read-only properties
# 
# Stream.beat
# beat returns None for a Stream.
# 
# Stream.beatDuration
# unlike other Music21Objects, streams always have beatDuration of None
# 
# Stream.beatStr
# unlike other Music21Objects, streams always have beatStr (beat string) of None
# 
# May change to ‘’ soon.
# 
# Stream.beatStrength
# unlike other Music21Objects, streams always have beatStrength of None
# 
# Stream.flat
# A very important read-only property that returns a new Stream that has all sub-containers “flattened” within it, that is, it returns a new Stream where no elements nest within other elements.
# 
# Here is a simple example of the usefulness of .flat. We will create a Score with two Parts in it, each with two Notes:
# 

sc = stream.Score()
p1 = stream.Part()
p1.id = 'part1'
n1 = note.Note('C4')
n2 = note.Note('D4')
p1.append(n1)
p1.append(n2)

p2 = stream.Part()
p2.id = 'part2'
n3 = note.Note('E4')
n4 = note.Note('F4')
p2.append(n3)
p2.append(n4)

sc.insert(0, p1)
sc.insert(0, p2)
# When we look at sc, we will see only the two parts:
# 

sc.elements
# (<music21.stream.Part part1>, <music21.stream.Part part2>)
# We can get at the notes by using the indices of the stream to get the parts and then looking at the .elements there:
# 

sc[0].elements
# (<music21.note.Note C>, <music21.note.Note D>)

sc.getElementById('part2').elements
# (<music21.note.Note E>, <music21.note.Note F>)
# …but if we want to get all the notes, the easiest way is via calling .flat on sc and looking at the elements there:
# 

sc.flat.elements
# (<music21.note.Note C>, <music21.note.Note E>,
 # <music21.note.Note D>, <music21.note.Note F>)
# Flattening a stream is a great way to get at all the notes in a larger piece. For instance if we load a four-part Bach chorale into music21 from the integrated corpus, it will appear at first that there are no notes in the piece:
# 

bwv66 = corpus.parse('bach/bwv66.6')
len(bwv66.notes)
# 0
# This is because all the notes in the piece lie within music21.stream.Measure objects and those measures lie within music21.stream.Part objects. It’d be a pain to navigate all the way through all those objects just to count notes. Fortunately we can get a Stream of all the notes in the piece with .flat.notes and then use the length of that Stream to count notes:
# 

bwv66flat = bwv66.flat
len(bwv66flat.notes)
# 165
# If you look back to our simple example of four notes above, you can see that the E (the first note in part2) comes before the D (the second note of part1). This is because the flat stream is automatically sorted like all streams are by default. The next example shows how to change this behavior.
# 

s = stream.Stream()
s.autoSort = False
s.repeatInsert(note.Note('C#'), [0, 2, 4])
s.repeatInsert(note.Note('D-'), [1, 3, 5])
s.isSorted
# False

g = ''
for myElement in s:
# ...    g += '%s: %s; ' % (myElement.offset, myElement.name)
# ...

g
# '0.0: C#; 2.0: C#; 4.0: C#; 1.0: D-; 3.0: D-; 5.0: D-; '

y = s.sorted
y.isSorted
# True

g = ''
for myElement in y:
# ...    g += '%s: %s; ' % (myElement.offset, myElement.name)
# ...

g
# '0.0: C#; 1.0: D-; 2.0: C#; 3.0: D-; 4.0: C#; 5.0: D-; '

q = stream.Stream()
for i in range(5):
# ...     p = stream.Stream()
# ...     p.repeatInsert(base.Music21Object(), [0, 1, 2, 3, 4])
# ...     q.insert(i * 10, p)
# ...

len(q)
# 5

qf = q.flat
len(qf)
# 25
qf[24].offset
# 44.0
# Stream.highestOffset
# Get start time of element with the highest offset in the Stream. Note the difference between this property and highestTime which gets the end time of the highestOffset
# 

stream1 = stream.Stream()
for offset in [0, 4, 8]:
# ...     n = note.Note('G#', type='whole')
# ...     stream1.insert(offset, n)
stream1.highestOffset
# 8.0
stream1.highestTime
# 12.0
# Stream.highestTime
# Returns the maximum of all Element offsets plus their Duration in quarter lengths. This value usually represents the last “release” in the Stream.
# 
# Stream.duration is usually equal to the highestTime expressed as a Duration object, but it can be set separately for advanced operations.
# 
# Example: Insert a dotted half note at position 0 and see where it cuts off:
# 

p1 = stream.Stream()
p1.highestTime
# 0.0

n = note.Note('A-')
n.quarterLength = 3
p1.insert(0, n)
p1.highestTime
# 3.0
# Now insert in the same stream, the dotted half note at positions 1, 2, 3, 4 and see when the final note cuts off:
# 

p1.repeatInsert(n, [1, 2, 3, 4])
p1.highestTime
# 7.0
# Another example.
# 

n = note.Note('C#')
n.quarterLength = 3

q = stream.Stream()
for i in [20, 0, 10, 30, 40]:
# ...    p = stream.Stream()
# ...    p.repeatInsert(n, [0, 1, 2, 3, 4])
# ...    q.insert(i, p)  # insert out of order
len(q.flat)
# 25
q.highestTime  # this works b/c the component Stream has an duration
# 47.0
r = q.flat
# Stream.isGapless
# Returns True if there are no gaps between the lowest offset and the highest time. Otherwise returns False
# 

s = stream.Stream()
s.append(note.Note('C'))
s.append(note.Note('D'))
s.isGapless
# True
s.insert(10.0, note.Note('E'))
s.isGapless
# False
# Stream.iter
# The Stream iterator, used in all for loops and similar iteration routines. This method returns the specialized music21.stream.StreamIterator class, which adds necessary Stream-specific features.
# 
# Generally you don’t need this, just iterate over a stream, but it is necessary to add custom filters to an iterative search before iterating.
# 
# Stream.lowestOffset
# Get the start time of the Element with the lowest offset in the Stream.
# 

stream1 = stream.Stream()
for x in range(3, 5):
# ...     n = note.Note('G#')
# ...     stream1.insert(x, n)
# ...
stream1.lowestOffset
# 3.0
# If the Stream is empty, then the lowest offset is 0.0:
# 

stream2 = stream.Stream()
stream2.lowestOffset
# 0.0

p = stream.Stream()
p.repeatInsert(note.Note('D5'), [0, 1, 2, 3, 4])
q = stream.Stream()
q.repeatInsert(p, list(range(0, 50, 10)))
len(q.flat)
# 25
q.lowestOffset
# 0.0
r = stream.Stream()
r.repeatInsert(q, list(range(97, 500, 100)))
len(r.flat)
# 125
r.lowestOffset
# 97.0
# Stream.notes
# The notes property of a Stream returns an iterator that consists only of the notes (that is, Note, Chord, etc.) found in the stream. This excludes Rest objects.
# 

p1 = stream.Part()
k1 = key.KeySignature(0)  # key of C
n1 = note.Note('B')
r1 = note.Rest()
c1 = chord.Chord(['A', 'B-'])
p1.append([k1, n1, r1, c1])
p1.show('text')
# {0.0} <music21.key.KeySignature of no sharps or flats>
# {0.0} <music21.note.Note B>
# {1.0} <music21.note.Rest rest>
# {2.0} <music21.chord.Chord A B->

noteStream = p1.notes.stream()
noteStream.show('text')
# {0.0} <music21.note.Note B>
# {2.0} <music21.chord.Chord A B->
# Notice that .notes returns a StreamIterator object
# 

p1.notes
# <music21.stream.iterator.StreamIterator for Part:0x105b56128 @:0>
# Let’s add a measure to p1:
# 

m1 = stream.Measure()
n2 = note.Note('D')
m1.insert(0, n2)
p1.append(m1)
# Now note that n2 is not found in p1.notes
# 

p1.notes.stream().show('text')
# {0.0} <music21.note.Note B>
# {2.0} <music21.chord.Chord A B->
# We need to call p1.flat.notes to find it:
# 

p1.flat.notes.stream().show('text')
# {0.0} <music21.note.Note B>
# {2.0} <music21.chord.Chord A B->
# {3.0} <music21.note.Note D>
# Stream.notesAndRests
# The notesAndRests property of a Stream returns a StreamIterator that consists only of the GeneralNote objects found in the stream. The new Stream will contain mostly notes and rests (including Note, Chord, Rest) but also their subclasses, such as Harmony objects (ChordSymbols, FiguredBass), SpacerRests etc.
# 

s1 = stream.Stream()
k1 = key.KeySignature(0)  # key of C
n1 = note.Note('B')
r1 = note.Rest()
c1 = chord.Chord(['A', 'B-'])
s1.append([k1, n1, r1, c1])
s1.show('text')
# {0.0} <music21.key.KeySignature of no sharps or flats>
# {0.0} <music21.note.Note B>
# {1.0} <music21.note.Rest rest>
# {2.0} <music21.chord.Chord A B->
# .notesAndRests removes the KeySignature object but keeps the Rest.
# 

notes1 = s1.notesAndRests.stream()
notes1.show('text')
# {0.0} <music21.note.Note B>
# {1.0} <music21.note.Rest rest>
# {2.0} <music21.chord.Chord A B->
# The same caveats about Stream classes and .flat in .notes apply here.
# 
# Stream.pitches
# Returns all Pitch objects found in any element in the Stream as a Python List. Elements such as Streams, and Chords will have their Pitch objects accumulated as well. For that reason, a flat representation is not required.
# 
# Pitch objects are returned in a List, not a Stream. This usage differs from the .notes property, but makes sense since Pitch objects usually have by default a Duration of zero. This is an important difference between them and music21.note.Note objects.
# 
# key.Key objects are subclasses of Scales, which DO have a .pitches list, but they are specifically exempt from looking for pitches, since that is unlikely what someone wants here.
# 
# N.B., TODO: This may turn to an Iterator soon.
# 

from music21 import corpus
a = corpus.parse('bach/bwv324.xml')
partOnePitches = a.parts[0].pitches
len(partOnePitches)
# 25
partOnePitches[0]
# <music21.pitch.Pitch B4>
[str(p) for p in partOnePitches[0:10]]
# ['B4', 'D5', 'B4', 'B4', 'B4', 'B4', 'C5', 'B4', 'A4', 'A4']
# Note that the pitches returned above are objects, not text:
# 

partOnePitches[0].octave
# 4
# Since all elements with a .pitches list are returned and streams themselves have .pitches properties (the docs you are reading now), pitches from embedded streams are also returned. Flattening a stream is not necessary. Whether this is a feature or a bug is in the eye of the beholder.
# 

len(a.pitches)
# 104
# Chords get their pitches found as well:
# 

c = chord.Chord(['C4', 'E4', 'G4'])
n = note.Note('F#4')
m = stream.Measure()
m.append(n)
m.append(c)
m.pitches
# [<music21.pitch.Pitch F#4>, <music21.pitch.Pitch C4>,
 # <music21.pitch.Pitch E4>, <music21.pitch.Pitch G4>]
# Stream.secondsMap
# Returns a list where each element is a dictionary consisting of the ‘offsetSeconds’ in seconds of each element in a Stream, the ‘duration’ in seconds, the ‘endTimeSeconds’ in seconds (that is, the offset plus the duration), and the ‘element’ itself. Also contains a ‘voiceIndex’ entry which contains the voice number of the element, or None if there are no voices.
# 

mm1 = tempo.MetronomeMark(number=120)
n1 = note.Note(type='quarter')
c1 = clef.AltoClef()
n2 = note.Note(type='half')
s1 = stream.Stream()
s1.append([mm1, n1, c1, n2])
om = s1.secondsMap
om[3]['offsetSeconds']
# 0.5
om[3]['endTimeSeconds']
# 1.5
om[3]['element'] is n2
# True
om[3]['voiceIndex']
# Stream.semiFlat
# Returns a flat-like Stream representation. Stream sub-classed containers, such as Measure or Part, are retained in the output Stream, but positioned at their relative offset.
# 

s = stream.Stream()

p1 = stream.Part()
p1.id = 'part1'
n1 = note.Note('C5')
p1.append(n1)

p2 = stream.Part()
p2.id = 'part2'
n2 = note.Note('D5')
p2.append(n2)

s.insert(0, p1)
s.insert(0, p2)
sf = s.semiFlat
sf.elements
# (<music21.stream.Part part1>,
 # <music21.stream.Part part2>,
 # <music21.note.Note C>,
 # <music21.note.Note D>)
sf[0]
# <music21.stream.Part part1>
sf[2]
# <music21.note.Note C>
sf[0][0]
# <music21.note.Note C>
# Stream.sorted
# Returns a new Stream where all the elements are sorted according to offset time, then priority, then classSortOrder (so that, for instance, a Clef at offset 0 appears before a Note at offset 0)
# 
# if this Stream is not flat, then only the highest elements are sorted. To sort all, run myStream.flat.sorted
# 
# For instance, here is an unsorted Stream
# 

s = stream.Stream()
s.autoSort = False  # if True, sorting is automatic
s.insert(1, note.Note('D'))
s.insert(0, note.Note('C'))
s.show('text')
# {1.0} <music21.note.Note D>
# {0.0} <music21.note.Note C>
# But a sorted version of the Stream puts the C first:
# 

s.sorted.show('text')
# {0.0} <music21.note.Note C>
# {1.0} <music21.note.Note D>
# While the original stream remains unsorted:
# 

s.show('text')
# {1.0} <music21.note.Note D>
# {0.0} <music21.note.Note C>
# Stream.spanners
# Return all Spanner objects (things such as Slurs, long trills, or anything that connects many objects) in an Iterator
# 

s = stream.Stream()
s.insert(0, spanner.Slur())
s.insert(0, spanner.Slur())
len(s.spanners)
# 2
# Stream.variants
# Return a Stream containing all Variant objects in this Stream.
# 

s = stream.Stream()
s.repeatAppend(note.Note('C4'), 8)
v1 = variant.Variant([note.Note('D#4'), note.Note('F#4')])
s.insert(3, v1)

varStream = s.variants
len(varStream)
# 1
varStream[0] is v1
# True
len(s.variants[0])
# 2
# Note that the D# and F# aren’t found in the original Stream’s pitches
# 

[str(p) for p in s.pitches]
# ['C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4', 'C4']
# Stream.voices
# Return all Voices objects in an iterator
# 

s = stream.Stream()
s.insert(0, stream.Voice())
s.insert(0, stream.Voice())
len(s.voices)
# 2
# Read-only properties inherited from StreamCoreMixin:
# 
# spannerBundle
# 
# Read-only properties inherited from Music21Object:
# 
# hasEditorialInformation
# 
# hasStyleInformation
# 
# measureNumber
# 
# Read-only properties inherited from ProtoM21Object:
# 
# classSet
# 
# classes
# 
# Stream read/write properties
# 
# Stream.atSoundingPitch
# Get or set the atSoundingPitch status, that is whether the score is at concert pitch or may have transposing instruments that will not sound as notated.
# 
# Valid values are True, False, and ‘unknown’.
# 
# Note that setting “atSoundingPitch” does not actually transpose the notes. See toSoundingPitch() for that information.
# 

s = stream.Stream()
s.atSoundingPitch = True
s.atSoundingPitch = False
s.atSoundingPitch = 'unknown'
s.atSoundingPitch
# 'unknown'
s.atSoundingPitch = 'junk'
# Traceback (most recent call last):
# music21.exceptions21.StreamException: not a valid at sounding pitch value: junk
# Stream.clef
# Finds or sets a Clef at offset 0.0 in the measure:
# 

m = stream.Measure()
m.number = 10
m.clef = clef.TrebleClef()
thisTrebleClef = m.clef
thisTrebleClef.sign
# 'G'
thisTrebleClef.getOffsetBySite(m)
# 0.0
# Setting the clef for the measure a second time removes the previous clef from the measure and replaces it with the new one:
# 

m.clef = clef.BassClef()
m.clef.sign
# 'F'
# And the TrebleClef is no longer in the measure:
# 

thisTrebleClef.getOffsetBySite(m)
# Traceback (most recent call last):
# music21.sites.SitesException: an entry for this object <music21.clef.TrebleClef> is not
      # stored in stream <music21.stream.Measure 10 offset=0.0>
# The .clef appears in a .show() or other call just like any other element
# 

m.append(note.Note('D#', type='whole'))
m.show('text')
# {0.0} <music21.clef.BassClef>
# {0.0} <music21.note.Note D#>
# Stream.duration
# Returns the total duration of the Stream, from the beginning of the stream until the end of the final element. May be set independently by supplying a Duration object.
# 

a = stream.Stream()
q = note.Note(type='quarter')
a.repeatInsert(q, [0, 1, 2, 3])
a.highestOffset
# 3.0
a.highestTime
# 4.0
a.duration
# <music21.duration.Duration 4.0>
a.duration.quarterLength
# 4.0
# Advanced usage: override the duration from what is set:
# 

newDuration = duration.Duration('half')
newDuration.quarterLength
# 2.0

a.duration = newDuration
a.duration.quarterLength
# 2.0
# Restore normal behavior by setting duration to None:
# 

a.duration = None
a.duration
# <music21.duration.Duration 4.0>
# Note that the highestTime for the stream is the same whether duration is overridden or not:
# 

a.highestTime
# 4.0
# Stream.elements
# .elements is a list representing the elements contained in the Stream.
# 
# Directly getting, setting, and manipulating this list is reserved for advanced usage. Instead, use the the provided high-level methods.
# 
# In other words: Don’t use unless you really know what you’re doing. Treat a Stream like a list!
# 
# When setting .elements, a list of Music21Objects can be provided, or a complete Stream. If a complete Stream is provided, elements are extracted from that Stream. This has the advantage of transferring offset correctly and getting _endElements.
# 

a = stream.Stream()
a.repeatInsert(note.Note('C'), list(range(10)))
b = stream.Stream()
b.repeatInsert(note.Note('D'), list(range(10)))
b.offset = 6
c = stream.Stream()
c.repeatInsert(note.Note('E'), list(range(10)))
c.offset = 12
b.insert(c)
b.isFlat
# False

a.isFlat
# True
# Assigning from a Stream works well.
# 

a.elements = b
a.isFlat
# False

len(a.flat.notes) == len(b.flat.notes) == 20
# True
# Return type
# list(base.Music21Object)
# 
# Stream.finalBarline
# Get or set the final barline of this Stream’s Measures, if and only if there are Measures defined as elements in this Stream. This method will not create Measures if non exist. Setting a final barline to a Stream that does not have Measure will raise an exception.
# 
# This property also works on Scores that contain one or more Parts. In that case a list of barlines can be used to set the final barline.
# 

s = corpus.parse('bwv66.6')
s.finalBarline = 'none'
s.finalBarline
# [<music21.bar.Barline type=none>,
 # <music21.bar.Barline type=none>,
 # <music21.bar.Barline type=none>,
 # <music21.bar.Barline type=none>]
# Stream.keySignature
# Find or set a Key or KeySignature at offset 0 of a stream.
# 

a = stream.Measure()
a.keySignature = key.KeySignature(2)
a.keySignature.sharps
# 2
# A key.Key object can be used instead of key.KeySignature, since the former derives from the latter.
# 

a.keySignature = key.Key('E-', 'major')
a.keySignature.sharps
# -3
# Setting a new key signature replaces any previous ones:
# 

len(a.getElementsByClass('KeySignature'))
# 1
# Stream.metadata
# Get or set the Metadata object found at the beginning (offset 0) of this Stream.
# 

s = stream.Stream()
s.metadata = metadata.Metadata()
s.metadata.composer = 'frank'
s.metadata.composer
# 'frank'
# Stream.seconds
# Get or set the duration of this Stream in seconds, assuming that this object contains a MetronomeMark or MetricModulation.
# 

s = corpus.parse('bwv66.6')  # piece without a tempo
sFlat = s.flat
t = tempo.MetronomeMark('adagio')
sFlat.insert(0, t)
sFlat.seconds
# 38.57142857...
tFast = tempo.MetronomeMark('allegro')
sFlat.replace(t, tFast)
sFlat.seconds
# 16.363...
# Stream.timeSignature

a = stream.Measure()
a.timeSignature = meter.TimeSignature('2/4')
a.timeSignature.numerator, a.timeSignature.denominator
# (2, 4)
# Read/write properties inherited from Music21Object:
# 
# activeSite
# 
# derivation
# 
# editorial
# 
# offset
# 
# priority
# 
# quarterLength
# 
# style
# 
# Stream methods
# 
# Stream.activateVariants(group=None, *, matchBySpan=True, inPlace=False)
# For any Variant objects defined in this Stream (or selected by matching the group parameter), replace elements defined in the Variant with those in the calling Stream. Elements replaced will be gathered into a new Variant given the group ‘default’. If a variant is activated with .replacementDuration different from its length, the appropriate elements in the stream will have their offsets shifted, and measure numbering will be fixed. If matchBySpan is True, variants with lengthType ‘replacement’ will replace all of the elements in the replacement region of comparable class. If matchBySpan is False, elements will be swapped in when a match is found between an element in the variant and an element in the replacement region of the string.
# 

sStr   = 'd4 e4 f4 g4   a2 b-4 a4    g4 a8 g8 f4 e4    d2 a2              '
v1Str  = '              a2. b-8 a8 '
v2Str1 = '                                             d4 f4 a2 '
v2Str2 = '                                                      d4 f4 AA2 '

sStr += "d4 e4 f4 g4    a2 b-4 a4    g4 a8 b-8 c'4 c4    f1"

s = converter.parse('tinynotation: 4/4 ' + sStr, makeNotation=False)
s.makeMeasures(inPlace=True)  # maybe not necessary?
v1stream = converter.parse('tinynotation: 4/4 ' + v1Str, makeNotation=False)
v2stream1 = converter.parse('tinynotation: 4/4 ' + v2Str1, makeNotation=False)
v2stream2 = converter.parse('tinynotation: 4/4 ' + v2Str2, makeNotation=False)

v1 = variant.Variant()
v1measure = stream.Measure()
v1.insert(0.0, v1measure)
for e in v1stream.notesAndRests:
# ...    v1measure.insert(e.offset, e)

v2 = variant.Variant()
v2measure1 = stream.Measure()
v2measure2 = stream.Measure()
v2.insert(0.0, v2measure1)
v2.insert(4.0, v2measure2)
for e in v2stream1.notesAndRests:
# ...    v2measure1.insert(e.offset, e)
for e in v2stream2.notesAndRests:
# ...    v2measure2.insert(e.offset, e)

v3 = variant.Variant()
v2.replacementDuration = 4.0
v3.replacementDuration = 4.0
v1.groups = ['docVariants']
v2.groups = ['docVariants']
v3.groups = ['docVariants']

s.insert(4.0, v1)    # replacement variant
s.insert(12.0, v2)  # insertion variant (2 bars replace 1 bar)
s.insert(20.0, v3)  # deletion variant (0 bars replace 1 bar)
s.show('text')
# {0.0} <music21.stream.Measure 1 offset=0.0>
    # {0.0} <music21.clef.TrebleClef>
    # {0.0} <music21.meter.TimeSignature 4/4>
    # {0.0} <music21.note.Note D>
    # {1.0} <music21.note.Note E>
    # {2.0} <music21.note.Note F>
    # {3.0} <music21.note.Note G>
# {4.0} <music21.variant.Variant object of length 4.0>
# {4.0} <music21.stream.Measure 2 offset=4.0>
    # {0.0} <music21.note.Note A>
    # {2.0} <music21.note.Note B->
    # {3.0} <music21.note.Note A>
# {8.0} <music21.stream.Measure 3 offset=8.0>
    # {0.0} <music21.note.Note G>
    # {1.0} <music21.note.Note A>
    # {1.5} <music21.note.Note G>
    # {2.0} <music21.note.Note F>
    # {3.0} <music21.note.Note E>
# {12.0} <music21.variant.Variant object of length 8.0>
# {12.0} <music21.stream.Measure 4 offset=12.0>
    # {0.0} <music21.note.Note D>
    # {2.0} <music21.note.Note A>
# {16.0} <music21.stream.Measure 5 offset=16.0>
    # {0.0} <music21.note.Note D>
    # {1.0} <music21.note.Note E>
    # {2.0} <music21.note.Note F>
    # {3.0} <music21.note.Note G>
# {20.0} <music21.variant.Variant object of length 0.0>
# {20.0} <music21.stream.Measure 6 offset=20.0>
    # {0.0} <music21.note.Note A>
    # {2.0} <music21.note.Note B->
    # {3.0} <music21.note.Note A>
# {24.0} <music21.stream.Measure 7 offset=24.0>
    # {0.0} <music21.note.Note G>
    # {1.0} <music21.note.Note A>
    # {1.5} <music21.note.Note B->
    # {2.0} <music21.note.Note C>
    # {3.0} <music21.note.Note C>
# {28.0} <music21.stream.Measure 8 offset=28.0>
    # {0.0} <music21.note.Note F>
    # {4.0} <music21.bar.Barline type=final>

docVariant = s.activateVariants('docVariants')

s.show()
# ../_images/stream_activateVariants1.png

docVariant.show()
# ../_images/stream_activateVariants2.png

docVariant.show('text')
# {0.0} <music21.stream.Measure 1 offset=0.0>
    # {0.0} <music21.clef.TrebleClef>
    # {0.0} <music21.meter.TimeSignature 4/4>
    # {0.0} <music21.note.Note D>
    # {1.0} <music21.note.Note E>
    # {2.0} <music21.note.Note F>
    # {3.0} <music21.note.Note G>
# {4.0} <music21.variant.Variant object of length 4.0>
# {4.0} <music21.stream.Measure 2 offset=4.0>
    # {0.0} <music21.note.Note A>
    # {3.0} <music21.note.Note B->
    # {3.5} <music21.note.Note A>
# {8.0} <music21.stream.Measure 3 offset=8.0>
    # {0.0} <music21.note.Note G>
    # {1.0} <music21.note.Note A>
    # {1.5} <music21.note.Note G>
    # {2.0} <music21.note.Note F>
    # {3.0} <music21.note.Note E>
# {12.0} <music21.variant.Variant object of length 4.0>
# {12.0} <music21.stream.Measure 4 offset=12.0>
    # {0.0} <music21.note.Note D>
    # {1.0} <music21.note.Note F>
    # {2.0} <music21.note.Note A>
# {16.0} <music21.stream.Measure 5 offset=16.0>
    # {0.0} <music21.note.Note D>
    # {1.0} <music21.note.Note F>
    # {2.0} <music21.note.Note A>
# {20.0} <music21.stream.Measure 6 offset=20.0>
    # {0.0} <music21.note.Note D>
    # {1.0} <music21.note.Note E>
    # {2.0} <music21.note.Note F>
    # {3.0} <music21.note.Note G>
# {24.0} <music21.variant.Variant object of length 4.0>
# {24.0} <music21.stream.Measure 7 offset=24.0>
    # {0.0} <music21.note.Note G>
    # {1.0} <music21.note.Note A>
    # {1.5} <music21.note.Note B->
    # {2.0} <music21.note.Note C>
    # {3.0} <music21.note.Note C>
# {28.0} <music21.stream.Measure 8 offset=28.0>
    # {0.0} <music21.note.Note F>
    # {4.0} <music21.bar.Barline type=final>
# After a variant group has been activated, the regions it replaced are stored as variants with the group ‘default’. It should be noted that this means .activateVariants should rarely if ever be used on a stream which is returned by activateVariants because the group information is lost.
# 

defaultVariant = docVariant.activateVariants('default')
defaultVariant.show()
# ../_images/stream_activateVariants3.png

defaultVariant.show('text')
# {0.0} <music21.stream.Measure 1 offset=0.0>
    # {0.0} <music21.clef.TrebleClef>
    # {0.0} <music21.meter.TimeSignature 4/4>
    # {0.0} <music21.note.Note D>
    # {1.0} <music21.note.Note E>
    # {2.0} <music21.note.Note F>
    # {3.0} <music21.note.Note G>
# {4.0} <music21.variant.Variant object of length 4.0>
# {4.0} <music21.stream.Measure 2 offset=4.0>
    # {0.0} <music21.note.Note A>
    # {2.0} <music21.note.Note B->
    # {3.0} <music21.note.Note A>
# {8.0} <music21.stream.Measure 3 offset=8.0>
    # {0.0} <music21.note.Note G>
    # {1.0} <music21.note.Note A>
    # {1.5} <music21.note.Note G>
    # {2.0} <music21.note.Note F>
    # {3.0} <music21.note.Note E>
# {12.0} <music21.variant.Variant object of length 8.0>
# {12.0} <music21.stream.Measure 4 offset=12.0>
    # {0.0} <music21.note.Note D>
    # {2.0} <music21.note.Note A>
# {16.0} <music21.stream.Measure 5 offset=16.0>
    # {0.0} <music21.note.Note D>
    # {1.0} <music21.note.Note E>
    # {2.0} <music21.note.Note F>
    # {3.0} <music21.note.Note G>
# {20.0} <music21.variant.Variant object of length 0.0>
# {20.0} <music21.stream.Measure 6 offset=20.0>
    # {0.0} <music21.note.Note A>
    # {2.0} <music21.note.Note B->
    # {3.0} <music21.note.Note A>
# {24.0} <music21.stream.Measure 7 offset=24.0>
    # {0.0} <music21.note.Note G>
    # {1.0} <music21.note.Note A>
    # {1.5} <music21.note.Note B->
    # {2.0} <music21.note.Note C>
    # {3.0} <music21.note.Note C>
# {28.0} <music21.stream.Measure 8 offset=28.0>
    # {0.0} <music21.note.Note F>
    # {4.0} <music21.bar.Barline type=final>
# Stream.addGroupForElements(group, classFilter=None)
# Add the group to the groups attribute of all elements. if classFilter is set then only those elements whose objects belong to a certain class (or for Streams which are themselves of a certain class) are set.
# 

a = stream.Stream()
a.repeatAppend(note.Note('A-'), 30)
a.repeatAppend(note.Rest(), 30)
a.addGroupForElements('flute')
a[0].groups
# ['flute']
a.addGroupForElements('quietTime', note.Rest)
a[0].groups
# ['flute']
a[50].groups
# ['flute', 'quietTime']
a[1].groups.append('quietTime')  # set one note to it
a[1].step = 'B'
b = a.getElementsByGroup('quietTime')
len(b)
# 31
c = b.getElementsByClass(note.Note)
len(c)
# 1
c[0].name
# 'B-'
# Stream.allPlayingWhileSounding(el, elStream=None)
# Returns a new Stream of elements in this stream that sound at the same time as el, an element presumably in another Stream.
# 
# The offset of this new Stream is set to el’s offset, while the offset of elements within the Stream are adjusted relative to their position with respect to the start of el. Thus, a note that is sounding already when el begins would have a negative offset. The duration of otherStream is forced to be the length of el – thus a note sustained after el ends may have a release time beyond that of the duration of the Stream.
# 
# As above, elStream is an optional Stream to look up el’s offset in. Use this to work on an element in another part.
# 
# The method always returns a Stream, but it might be an empty Stream.
# 
# Stream.analyze(*args, **keywords)
# Runs a particular analytical method on the contents of the stream to find its ambitus (range) or key.
# 
# ambitus – runs Ambitus
# 
# key – runs KrumhanslSchmuckler
# 
# Some of these methods can take additional arguments. For details on these arguments, see analyzeStream().
# 
# Example:
# 

s = corpus.parse('bach/bwv66.6')
s.analyze('ambitus')
# <music21.interval.Interval m21>
s.analyze('key')
# <music21.key.Key of f# minor>
# Example: music21 allows you to automatically run an analysis to get the key of a piece or excerpt not based on the key signature but instead on the frequency with which some notes are used as opposed to others (first described by Carol Krumhansl). For instance, a piece with mostly Cs and Gs, some Fs, and Ds, but fewer G#s, C#s, etc. is more likely to be in the key of C major than in D-flat major (or A minor, etc.). You can easily get this analysis from a stream by running:
# 

myStream = corpus.parse('luca/gloria')
analyzedKey = myStream.analyze('key')
analyzedKey
# <music21.key.Key of F major>
# analyzedKey is a Key object with a few extra parameters. correlationCoefficient shows how well this key fits the profile of a piece in that key:
# 

analyzedKey.correlationCoefficient
# 0.86715...
# alternateInterpretations is a list of the other possible interpretations sorted from most likely to least:
# 

analyzedKey.alternateInterpretations
# [<music21.key.Key of d minor>,
 # <music21.key.Key of C major>,
 # <music21.key.Key of g minor>,
 # ...]
# Each of these can be examined in turn to see its correlation coefficient:
# 

analyzedKey.alternateInterpretations[1].correlationCoefficient
# 0.788528...
analyzedKey.alternateInterpretations[22].correlationCoefficient
# -0.86728...
# Stream.append(others)
# Add a Music21Object (including another Stream) to the end of the current Stream.
# 
# If given a list, will append each element in order after the previous one.
# 
# The “end” of the stream is determined by the highestTime property (that is the latest “release” of an object, or directly after the last element ends).
# 
# Runs fast for multiple addition and will preserve isSorted if True
# 

a = stream.Stream()
notes = []
for x in range(3):
# ...     n = note.Note('G#')
# ...     n.duration.quarterLength = 3
# ...     notes.append(n)
a.append(notes[0])
a.highestOffset, a.highestTime
# (0.0, 3.0)
a.append(notes[1])
a.highestOffset, a.highestTime
# (3.0, 6.0)
a.append(notes[2])
a.highestOffset, a.highestTime
# (6.0, 9.0)
notes2 = []
# Since notes are not embedded in Elements here, their offset changes when they are added to a stream!
# 

for x in range(3):
# ...     n = note.Note('A-')
# ...     n.duration.quarterLength = 3
# ...     n.offset = 0
# ...     notes2.append(n)
a.append(notes2)  # add em all again
a.highestOffset, a.highestTime
# (15.0, 18.0)
a.isSequence()
# True
# Adding a note that already has an offset set does nothing different from above! That is, it is still added to the end of the Stream:
# 

n3 = note.Note('B-')
n3.offset = 1
n3.duration.quarterLength = 3
a.append(n3)
a.highestOffset, a.highestTime
# (18.0, 21.0)
n3.getOffsetBySite(a)
# 18.0
# Prior to v5.7 there was a bug where appending a Clef after a KeySignature or a Measure after a KeySignature, etc. would not cause sorting to be re-run. This bug is now fixed.
# 

s = stream.Stream()
s.append([meter.TimeSignature('4/4'),
# ...           clef.TrebleClef()])
s.elements[0]
# <music21.clef.TrebleClef>
s.show('text')
# {0.0} <music21.clef.TrebleClef>
# {0.0} <music21.meter.TimeSignature 4/4>

s.append(metadata.Metadata(composer='Cage'))
s.show('text')
# {0.0} <music21.metadata.Metadata object at 0x11ca356a0>
# {0.0} <music21.clef.TrebleClef>
# {0.0} <music21.meter.TimeSignature 4/4>
# Stream.attachIntervalsBetweenStreams(cmpStream)
# For each element in self, creates an interval.Interval object in the element’s editorial that is the interval between it and the element in cmpStream that is sounding at the moment the element in srcStream is attacked.
# 
# Remember that if you are comparing two streams with measures, etc., you’ll need to flatten each stream as follows:
# 

stream1.flat.attachIntervalsBetweenStreams(stream2.flat)
# Example usage:
# 

s1 = converter.parse('tinynotation: 7/4 C4 d8 e f# g A2 d2', makeNotation=False)
s2 = converter.parse('tinynotation: 7/4 g4 e8 d c4   a2 r2', makeNotation=False)
s1.attachIntervalsBetweenStreams(s2)
for n in s1.notes:
# ...     if n.editorial.harmonicInterval is None:
# ...         print('None')  # if other voice had a rest...
# ...     else:
# ...         print(n.editorial.harmonicInterval.directedName)
# P12
# M2
# M-2
# A-4
# P-5
# P8
# None
# Stream.attachMelodicIntervals()
# For each element in self, creates an interval.Interval object in the element’s editorial that is the interval between it and the previous element in the stream. Thus, the first element will have a value of None.
# 
# DEPRECATED sometime soon. A replacement to come presently.
# 

s1 = converter.parse('tinyNotation: 7/4 C4 d8 e f# g A2 d2', makeNotation=False)
s1.attachMelodicIntervals()
for n in s1.notes:
# ...     if n.editorial.melodicInterval is None:
# ...         print('None')
# ...     else:
# ...         print(n.editorial.melodicInterval.directedName)
# None
# M9
# M2
# M2
# m2
# m-7
# P4

s = stream.Stream()
s.append(note.Note('C'))
s.append(note.Note('D'))
s.append(note.Rest(quarterLength=4.0))
s.append(note.Note('D'))
s.attachMelodicIntervals()
for n in s.notes:
# ...     if n.editorial.melodicInterval is None:
# ...         print('None')  # if other voice had a rest...
# ...     else:
# ...         print(n.editorial.melodicInterval.directedName)
# None
# M2
# P1
# Stream.augmentOrDiminish(amountToScale, *, inPlace=False)
# Given a number greater than zero, multiplies the current quarterLength of the duration of each element by this number as well as their offset and returns a new Stream. Or if inPlace is set to True, modifies the durations of each element within the stream.
# 
# A number of 0.5 will halve the durations and relative offset positions; a number of 2 will double the durations and relative offset positions.
# 
# Note that the default for inPlace is the opposite of what it is for augmentOrDiminish on a Duration. This is done purposely to reflect the most common usage.
# 

s = stream.Stream()
n = note.Note()
s.repeatAppend(n, 10)
s.highestOffset, s.highestTime
# (9.0, 10.0)
s1 = s.augmentOrDiminish(2)
s1.highestOffset, s1.highestTime
# (18.0, 20.0)
s1 = s.augmentOrDiminish(0.5)
s1.highestOffset, s1.highestTime
# (4.5, 5.0)
# Stream.beatAndMeasureFromOffset(searchOffset, fixZeros=True)
# Returns a two-element tuple of the beat and the Measure object (or the first one if there are several at the same offset; unlikely but possible) for a given offset from the start of this Stream (that contains measures).
# 
# Recursively searches for measures. Note that this method assumes that all parts have measures of consistent length. If that’s not the case, this method can be called on the relevant part.
# 
# This algorithm should work even for weird time signatures such as 2+3+2/8.
# 

bach = corpus.parse('bach/bwv1.6')
bach.parts[0].measure(2).getContextByClass('TimeSignature')
# <music21.meter.TimeSignature 4/4>
returnTuples = []
for offset in [0.0, 1.0, 2.0, 5.0, 5.5]:
# ...     returnTuples.append(bach.beatAndMeasureFromOffset(offset))
returnTuples
# [(4.0, <music21.stream.Measure 0 offset=0.0>),
 # (1.0, <music21.stream.Measure 1 offset=1.0>),
 # (2.0, <music21.stream.Measure 1 offset=1.0>),
 # (1.0, <music21.stream.Measure 2 offset=5.0>),
 # (1.5, <music21.stream.Measure 2 offset=5.0>)]
# To get just the measureNumber and beat, use a transformation like this: >>> [(beat, measureObj.number) for beat, measureObj in returnTuples] [(4.0, 0), (1.0, 1), (2.0, 1), (1.0, 2), (1.5, 2)]
# 
# Adapted from contributed code by Dmitri Tymoczko. With thanks to DT.
# 
# Stream.chordify(*, addTies=True, addPartIdAsGroup=False, removeRedundantPitches=True, toSoundingPitch=True)
# Create a chordal reduction of polyphonic music, where each change to a new pitch results in a new chord. If a Score or Part of Measures is provided, a Stream of Measures will be returned. If a flat Stream of notes, or a Score of such Streams is provided, no Measures will be returned.
# 
# If using chordify with chord symbols, ensure that the chord symbols have durations (by default the duration of a chord symbol object is 0, unlike a chord object). If harmony objects are not provided a duration, they will not be included in the chordified output pitches but may appear as chord symbol in notation on the score. To realize the chord symbol durations on a score, call music21.harmony.realizeChordSymbolDurations() and pass in the score.
# 
# This functionality works by splitting all Durations in all parts, or if multi-part by all unique offsets. All simultaneous durations are then gathered into single chords.
# 
# If addPartIdAsGroup is True, all elements found in the Stream will have their source Part id added to the element’s pitches’ Group. These groups names are useful for partially “de-chordifying” the output. If the element chordifies to a Chord object, then the group will be found in each Pitch element’s .groups in Chord.pitches. If the element chordifies to a single Note then .pitch.groups will hold the group name.
# 
# The addTies parameter currently does not work for pitches in Chords.
# 
# If toSoundingPitch is True, all parts that define one or more transpositions will be transposed to sounding pitch before chordification. True by default.
# 

s = stream.Score()
p1 = stream.Part()
p1.id = 'part1'
p1.insert(4, note.Note('C#4'))
p1.insert(5.3, note.Rest())
p2 = stream.Part()
p2.id = 'part2'
p2.insert(2.12, note.Note('D-4', type='half'))
p2.insert(5.5, note.Rest())
s.insert(0, p1)
s.insert(0, p2)
s.show('text', addEndTimes=True)
# {0.0 - 6.3} <music21.stream.Part part1>
    # {4.0 - 5.0} <music21.note.Note C#>
    # {5.3 - 6.3} <music21.note.Rest rest>
# {0.0 - 6.5} <music21.stream.Part part2>
    # {2.12 - 4.12} <music21.note.Note D->
    # {5.5 - 6.5} <music21.note.Rest rest>

cc = s.chordify()

cc[3]
# <music21.chord.Chord C#4>
cc[3].duration.quarterLength
# Fraction(22, 25)

cc.show('text', addEndTimes=True)
# {0.0 - 2.12} <music21.note.Rest rest>
# {2.12 - 4.0} <music21.chord.Chord D-4>
# {4.0 - 4.12} <music21.chord.Chord C#4 D-4>
# {4.12 - 5.0} <music21.chord.Chord C#4>
# {5.0 - 6.5} <music21.note.Rest rest>
# Here’s how addPartIdAsGroup works:
# 

cc2 = s.chordify(addPartIdAsGroup=True)
cSharpDFlatChord = cc2[2]
for p in cSharpDFlatChord.pitches:
# ...     (str(p), p.groups)
# ('C#4', ['part1'])
# ('D-4', ['part2'])

s = stream.Stream()
p1 = stream.Part()
p1.insert(0, harmony.ChordSymbol('Cm', quarterLength=4.0))
p1.insert(2, note.Note('C2'))
p1.insert(4, harmony.ChordSymbol('D', quarterLength=4.0))
p1.insert(7, note.Note('A2'))
s.insert(0, p1)
s.chordify().show('text')
# {0.0} <music21.chord.Chord C3 E-3 G3>
# {2.0} <music21.chord.Chord C2 C3 E-3 G3>
# {3.0} <music21.chord.Chord C3 E-3 G3>
# {4.0} <music21.chord.Chord D3 F#3 A3>
# {7.0} <music21.chord.Chord A2 D3 F#3 A3>
# Note that ChordSymbol objects can also be chordified:
# 

s = stream.Stream()
p2 = stream.Part()
p1 = stream.Part()
p2.insert(0, harmony.ChordSymbol('Cm', quarterLength=4.0))
p1.insert(2, note.Note('C2'))
p2.insert(4, harmony.ChordSymbol('D', quarterLength=4.0))
p1.insert(7, note.Note('A2'))
s.insert(0, p1)
s.insert(0, p2)
s.chordify().show('text')
# {0.0} <music21.chord.Chord C3 E-3 G3>
# {2.0} <music21.chord.Chord C2 C3 E-3 G3>
# {3.0} <music21.chord.Chord C3 E-3 G3>
# {4.0} <music21.chord.Chord D3 F#3 A3>
# {7.0} <music21.chord.Chord A2 D3 F#3 A3>
# If addPartIdAsGroup is True, and there are redundant pitches, ensure that the merged pitch has both groups
# 

s = stream.Score()
p0 = stream.Part(id='p0')
p0.insert(0, note.Note('C4'))
p1 = stream.Part(id='p1')
p1.insert(0, note.Note('C4'))
s.insert(0, p0)
s.insert(0, p1)
s1 = s.chordify(addPartIdAsGroup=True)
c = s1.recurse().notes[0]
c
# <music21.chord.Chord C4>
c.pitches[0].groups
# ['p0', 'p1']
# Changes in v.5:
# 
# Runs a little faster for small scores and run a TON faster for big scores running in O(n) time not O(n^2)
# 
# no longer supported: displayTiedAccidentals=False,
# 
# Stream.clear()
# Remove all elements in a stream.
# 

m = stream.Measure(number=3)
m.append(note.Note('C'))
m.storeAtEnd(bar.Barline('final'))
len(m)
# 2
m.clear()
len(m)
# 0
# Does not remove any other attributes
# 

m.number
# 3
# Stream.cloneEmpty(derivationMethod=None)
# Create a Stream that is identical to this one except that the elements are empty and set derivation (Should this be deleted???)
# 

p = stream.Part()
p.autoSort = False
p.id = 'hi'
p.insert(0, note.Note())
q = p.cloneEmpty(derivationMethod='demo')
q.autoSort
# False
q
# <music21.stream.Part hi>
q.derivation.origin is p
# True
q.derivation.method
# 'demo'
len(q)
# 0
# Stream.containerInHierarchy(el, *, setActiveSite=True)
# Returns the container in a hierarchy that this element belongs to.
# 
# For instance, assume a Note (n) is in a Measure (m1) which is in a Part, in a Score (s1), and the Note is also in another hierarchy (say, a chordified version of a Score, s2). if s1.containerInHierarchy(n) is called, it will return m1, and (unless setActiveSite is False) will return the Measure, m1, that contains the note.
# 
# If it cannot be found, then None is returned.
# 

s1 = stream.Score(id='s1')
p1 = stream.Part()
m1 = stream.Measure(id='m1')
n = note.Note('D')
m1.append(n)
p1.append(m1)
s1.insert(0, p1)
s2 = stream.Stream(id='s2')
s2.append(n)
n.activeSite.id
# 's2'
s1.containerInHierarchy(n).id
# 'm1'
n.activeSite.id
# 'm1'
n.activeSite = s2
s1.containerInHierarchy(n, setActiveSite=False).id
# 'm1'
n.activeSite.id
# 's2'
# @return Stream or None
# 
# Stream.elementOffset(element, stringReturns=False)
# Return the offset as an opFrac (float or Fraction) from the offsetMap. highly optimized for speed.
# 

m = stream.Measure(number=1)
m.append(note.Note('C'))
d = note.Note('D')
m.append(d)
m.elementOffset(d)
# 1.0
# If stringReturns is True then returns like ‘highestOffset’ are allowed.
# 

b = bar.Barline()
m.storeAtEnd(b)
m.elementOffset(b)
# 2.0
m.elementOffset(b, stringReturns=True)
# 'highestTime'
# Unlike element.getOffsetBySite(self), this method will NOT follow derivation chains and in fact will raise a sites.SitesException
# 

import copy
p = stream.Part(id='sPart')
p.insert(20, m)
m.getOffsetBySite(p)
# 20.0
p.elementOffset(m)
# 20.0

mCopy = copy.deepcopy(m)
mCopy.number = 10
mCopy.derivation
# <Derivation of <music21.stream.Measure 10 offset=0.0> from
    # <music21.stream.Measure 1 offset=20.0> via '__deepcopy__'>
mCopy.getOffsetBySite(p)
# 20.0
p.elementOffset(mCopy)
# Traceback (most recent call last):
# music21.sites.SitesException: an entry for this object 0x... is not stored in
    # stream <music21.stream.Part sPart>
# Performance note: because it will not follow derivation chains, and does not need to unwrap a weakref, this method should usually be about 3x faster than element.getOffsetBySite(self) – currently 600ns instead of 1.5 microseconds.
# 
# Stream.expandRepeats(copySpanners=True)
# Expand this Stream with repeats. Nested repeats given with Repeat objects, or repeats and sections designated with RepeatExpression objects, are all expanded.
# 
# This method always returns a new Stream, with deepcopies of all contained elements at all levels.
# 
# Uses the Expander object in the repeat module.
# 
# TODO: DOC TEST
# 
# Stream.explode()
# Create a multi-part extraction from a single polyphonic Part.
# 
# Currently just runs voicesToParts() but that will change as part explosion develops, and this method will use our best available quick method for part extraction.
# 
# Stream.extendDuration(objName, *, inPlace=False)
# Given a Stream and an object class name, go through the Stream and find each instance of the desired object. The time between adjacent objects is then assigned to the duration of each object. The last duration of the last object is assigned to extend to the end of the Stream.
# 
# If inPlace is True, this is done in-place; if inPlace is False, this returns a modified deep copy.
# 

stream1 = stream.Stream()
n = note.Note(type='quarter')
n.duration.quarterLength
# 1.0
stream1.repeatInsert(n, [0, 10, 20, 30, 40])

dyn = dynamics.Dynamic('ff')
stream1.insert(15, dyn)
stream1[-1].offset  # offset of last element
# 40.0
stream1.duration.quarterLength  # total duration
# 41.0
len(stream1)
# 6

stream2 = stream1.flat.extendDuration(note.GeneralNote, inPlace=False)
len(stream2)
# 6
stream2[0].duration.quarterLength
# 10.0
# The Dynamic does not affect the second note:
# 

stream2[1].offset
# 10.0
stream2[1].duration.quarterLength
# 10.0

stream2[-1].duration.quarterLength  # or extend to end of stream
# 1.0
stream2.duration.quarterLength
# 41.0
stream2[-1].offset
# 40.0
# Stream.extendDurationAndGetBoundaries(objName, *, inPlace=False)
# DEPRECATED in v.6 – to be removed in v.7
# 
# Extend the Duration of elements specified by objName; then, collect a dictionary for every matched element of objName class, where the matched element is the value and the key is the (start, end) offset value.
# 

from pprint import pprint as pp
s = stream.Stream()
s.insert(3, dynamics.Dynamic('mf'))
s.insert(7, dynamics.Dynamic('f'))
s.insert(12, dynamics.Dynamic('ff'))
pp(s.extendDurationAndGetBoundaries('Dynamic'))
# {(3.0, 7.0): <music21.dynamics.Dynamic mf>,
 # (7.0, 12.0): <music21.dynamics.Dynamic f>,
 # (12.0, 12.0): <music21.dynamics.Dynamic ff>}
# TODO: only allow inPlace=True or delete or something, can’t return two different things
# 
# Stream.extendTies(ignoreRests=False, pitchAttr='nameWithOctave')
# Connect any adjacent pitch space values that are the same with a Tie. Adjacent pitches can be Chords, Notes, or Voices.
# 
# If ignoreRests is True, rests that occur between events will not be considered in matching pitches.
# 
# The pitchAttr determines the pitch attribute that is used for comparison. Any valid pitch attribute name can be used.
# 
# Stream.extractContext(searchElement, before=4.0, after=4.0, maxBefore=None, maxAfter=None, forceOutputClass=None)
# Extracts elements around the given element within (before) quarter notes and (after) quarter notes (default 4), and returns a new Stream.
# 

qn = note.Note(type='quarter')
qtrStream = stream.Stream()
qtrStream.repeatInsert(qn, [0, 1, 2, 3, 4, 5])
hn = note.Note(type='half')
hn.name = 'B-'
qtrStream.append(hn)
qtrStream.repeatInsert(qn, [8, 9, 10, 11])
hnStream = qtrStream.extractContext(hn, 1.0, 1.0)
hnStream.show('text')
# {5.0} <music21.note.Note C>
# {6.0} <music21.note.Note B->
# {8.0} <music21.note.Note C>
# Stream.findConsecutiveNotes(skipRests=False, skipChords=False, skipUnisons=False, skipOctaves=False, skipGaps=False, getOverlaps=False, noNone=False, **keywords)
# Returns a list of consecutive pitched Notes in a Stream.
# 
# A single “None” is placed in the list at any point there is a discontinuity (such as if there is a rest between two pitches), unless the noNone parameter is True.
# 
# How to determine consecutive pitches is a little tricky and there are many options:
# 
# The skipUnisons parameter uses the midi-note value (.ps) to determine unisons, so enharmonic transitions (F# -> Gb) are also skipped if skipUnisons is true. We believe that this is the most common usage. However, because of this, you cannot completely be sure that the x.findConsecutiveNotes() - x.findConsecutiveNotes(skipUnisons=True) will give you the number of P1s in the piece, because there could be d2’s in there as well.
# 
# See test.TestStream.testFindConsecutiveNotes() for usage details.
# 
# This example is adapted from the tutorials/Examples page.
# 

s = converter.parse("tinynotation: 4/4 f8 d'8~ d'8 d'8~ d'4 b'-8 a'-8 a-8")
m = s.measure(1)
m.findConsecutiveNotes(skipUnisons=True, skipOctaves=True,
# ...                        skipRests=True, noNone=True)
# [<music21.note.Note F>, <music21.note.Note D>,
 # <music21.note.Note B->, <music21.note.Note A->]

m.findConsecutiveNotes(skipUnisons=False,
# ...                        skipRests=True, noNone=True)
# [<music21.note.Note F>, <music21.note.Note D>,
 # <music21.note.Note D>, <music21.note.Note D>, <music21.note.Note D>,
 # <music21.note.Note B->, <music21.note.Note A->]
# Stream.findGaps()
# Returns either (1) a Stream containing Elements (that wrap the None object) whose offsets and durations are the length of gaps in the Stream or (2) None if there are no gaps.
# 
# N.B. there may be gaps in the flattened representation of the stream but not in the unflattened. Hence why “isSequence” calls self.flat.isGapless
# 
# Stream.flattenUnnecessaryVoices(*, force=False, inPlace=False)
# If this Stream defines one or more internal voices, do the following:
# 
# If there is more than one voice, and a voice has no elements, remove that voice.
# 
# If there is only one voice left that has elements, place those elements in the parent Stream.
# 
# If force is True, even if there is more than one Voice left, all voices will be flattened.
# 
# Changed in v. 5 – inPlace is default False and a keyword only arg.
# 
# Stream.getClefs(searchActiveSite=False, searchContext=True, returnDefault=True)
# DEPRECATED…
# 
# Collect all Clef objects in this Stream in a list. Optionally search the activeSite Stream and/or contexts.
# 
# If no Clef objects are defined, get a default using bestClef()
# 

a = stream.Stream()
b = clef.AltoClef()
a.insert(0, b)
a.repeatInsert(note.Note('C#'), list(range(10)))
c = a.getClefs()
len(c) == 1
# True
# Stream.getElementAfterElement(element, classList=None)
# Given an element, get the next element. If classList is specified, check to make sure that the element is an instance of the class list
# 

st1 = stream.Stream()
n1 = note.Note('C4')
n2 = note.Note('D4')
r3 = note.Rest()
st1.append([n1, n2, r3])
t2 = st1.getElementAfterElement(n1)
t2 is n2
# True
t3 = st1.getElementAfterElement(t2)
t3 is r3
# True
t4 = st1.getElementAfterElement(t3)
t4

t5 = st1.getElementAfterElement(n1, [note.Rest])
t5
# <music21.note.Rest rest>
t5 is r3
# True
t6 = st1.getElementAfterElement(n1, [note.Rest, note.Note])
t6 is n2
# True

t7 = st1.getElementAfterElement(r3)
t7 is None
# True
# If the element is not in the stream, it will raise a StreamException:
# 
st1.getElementAfterElement(note.Note('C#'))
# Traceback (most recent call last):
# music21.exceptions21.StreamException:
    # cannot find object (<music21.note.Note C#>) in Stream
# Stream.getElementAtOrBefore(offset, classList=None)
# Given an offset, find the element at this offset, or with the offset less than and nearest to.
# 
# Return one element or None if no elements are at or preceded by this offset.
# 
# If the classList parameter is used, it should be a list of class names or strings, and only objects that are instances of these classes or subclasses of these classes will be returned.
# 

stream1 = stream.Stream()
x = note.Note('D4')
x.id = 'x'
y = note.Note('E4')
y.id = 'y'
z = note.Rest()
z.id = 'z'

stream1.insert(20, x)
stream1.insert(10, y)
stream1.insert( 0, z)

b = stream1.getElementAtOrBefore(21)
b.offset, b.id
# (20.0, 'x')

b = stream1.getElementAtOrBefore(19)
b.offset, b.id
# (10.0, 'y')

b = stream1.getElementAtOrBefore(0)
b.offset, b.id
# (0.0, 'z')
b = stream1.getElementAtOrBefore(0.1)
b.offset, b.id
# (0.0, 'z')
# You can give a list of acceptable classes to return, and non-matching elements will be ignored
# 

c = stream1.getElementAtOrBefore(100, [clef.TrebleClef, note.Rest])
c.offset, c.id
# (0.0, 'z')
# Getting an object via getElementAtOrBefore sets the activeSite for that object to the Stream, and thus sets its offset
# 

stream2 = stream.Stream()
stream2.insert(100.5, x)
x.offset
# 100.5
d = stream1.getElementAtOrBefore(20)
d is x
# True
x.activeSite is stream1
# True
x.offset
# 20.0
# If no element is before the offset, returns None
# 

s = stream.Stream()
s.insert(10, note.Note('E'))
print(s.getElementAtOrBefore(9))
# None
# The sort order of returned items is the reverse of the normal sort order, so that, for instance, if there’s a clef and a note at offset 20, getting the object before offset 21 will give you the note, and not the clef, since clefs sort before notes:
# 

clef1 = clef.BassClef()
stream1.insert(20, clef1)
e = stream1.getElementAtOrBefore(21)
e
# <music21.note.Note D>
# Stream.getElementBeforeOffset(offset, classList=None)
# Get element before (and not at) a provided offset.
# 
# If the classList parameter is used, it should be a list of class names or strings, and only objects that are instances of these classes or subclasses of these classes will be returned.
# 

stream1 = stream.Stream()
x = note.Note('D4')
x.id = 'x'
y = note.Note('E4')
y.id = 'y'
z = note.Rest()
z.id = 'z'
stream1.insert(20, x)
stream1.insert(10, y)
stream1.insert( 0, z)

b = stream1.getElementBeforeOffset(21)
b.offset, b.id
# (20.0, 'x')
b = stream1.getElementBeforeOffset(20)
b.offset, b.id
# (10.0, 'y')

b = stream1.getElementBeforeOffset(10)
b.offset, b.id
# (0.0, 'z')

b = stream1.getElementBeforeOffset(0)
b is None
# True
b = stream1.getElementBeforeOffset(0.1)
b.offset, b.id
# (0.0, 'z')

w = note.Note('F4')
w.id = 'w'
stream1.insert( 0, w)
# This should get w because it was inserted last.
# 

b = stream1.getElementBeforeOffset(0.1)
b.offset, b.id
# (0.0, 'w')
# But if we give it a lower priority than z then z will appear first.
# 

w.priority = z.priority - 1
b = stream1.getElementBeforeOffset(0.1)
b.offset, b.id
# (0.0, 'z')
# Stream.getElementById(elementId, classFilter=None)
# Returns the first encountered element for a given id. Return None if no match. Note: this uses the id attribute stored on elements, which may not be the same as id(e).
# 

a = stream.Stream()
ew = note.Note()
a.insert(0, ew)
a[0].id = 'green'
None == a.getElementById(3)
# True
a.getElementById('green').id
# 'green'
a.getElementById('Green').id  # case does not matter
# 'green'
# Getting an element by getElementById changes its activeSite
# 

b = stream.Stream()
b.append(ew)
ew.activeSite is b
# True
ew2 = a.getElementById('green')
ew2 is ew
# True
ew2.activeSite is a
# True
ew.activeSite is a
# True
# Return type
# base.Music21Object
# 
# Stream.getElementsByClass(classFilterList) → music21.stream.iterator.StreamIterator
# Return a StreamIterator that will iterate over Elements that match one or more classes in the classFilterList. A single class can also used for the classFilterList parameter instead of a List.
# 

a = stream.Score()
a.repeatInsert(note.Rest(), list(range(10)))
for x in range(4):
# ...     n = note.Note('G#')
# ...     n.offset = x * 3
# ...     a.insert(n)
found = a.getElementsByClass(note.Note)
found
# <music21.stream.iterator.StreamIterator for Score:0x104f2f400 @:0>

len(found)
# 4
found[0].pitch.accidental.name
# 'sharp'

foundStream = found.stream()
'Score' in foundStream.classes
# True
# Notice that we do not find elements that are in sub-streams of the main Stream. We’ll add 15 more rests in a sub-stream and they won’t be found:
# 

b = stream.Stream()
b.repeatInsert(note.Rest(), list(range(15)))
a.insert(b)
found = a.getElementsByClass(note.Rest)
len(found)
# 10
# To find them either (1) use .flat to get at everything:
# 

found = a.flat.getElementsByClass(note.Rest)
len(found)
# 25
# Or, (2) recurse over the main stream and call .getElementsByClass on each one. Notice that the first subStream is actually the outermost Stream:
# 

totalFound = 0
for subStream in a.recurse(streamsOnly=True, includeSelf=True):
# ...     found = subStream.getElementsByClass(note.Rest)
# ...     totalFound += len(found)
totalFound
# 25
# The class name of the Stream created is the same as the original:
# 

found = a.getElementsByClass(note.Note).stream()
found.__class__.__name__
# 'Score'
# …except if returnStreamSubClass is False, which makes the method return a generic Stream:
# 

found = a.getElementsByClass(note.Rest).stream(returnStreamSubClass=False)
found.__class__.__name__
# 'Stream'
# Make a list from a StreamIterator:
# 

foundList = list(a.flat.getElementsByClass(note.Rest))
len(foundList)
# 25
# Stream.getElementsByGroup(groupFilterList) → music21.stream.iterator.StreamIterator

n1 = note.Note('C')
n1.groups.append('trombone')
n2 = note.Note('D')
n2.groups.append('trombone')
n2.groups.append('tuba')
n3 = note.Note('E')
n3.groups.append('tuba')
s1 = stream.Stream()
s1.append(n1)
s1.append(n2)
s1.append(n3)
tboneSubStream = s1.getElementsByGroup('trombone')
for thisNote in tboneSubStream:
# ...     print(thisNote.name)
# C
# D
tubaSubStream = s1.getElementsByGroup('tuba')
for thisNote in tubaSubStream:
# ...     print(thisNote.name)
# D
# E
# Stream.getElementsByOffset(offsetStart, offsetEnd=None, *, includeEndBoundary=True, mustFinishInSpan=False, mustBeginInSpan=True, includeElementsThatEndAtStart=True, classList=None) → music21.stream.iterator.StreamIterator
# Returns a StreamIterator containing all Music21Objects that are found at a certain offset or within a certain offset time range (given the offsetStart and (optional) offsetEnd values).
# 
# There are several attributes that govern how this range is determined:
# 
# If mustFinishInSpan is True then an event that begins between offsetStart and offsetEnd but which ends after offsetEnd will not be included. The default is False.
# 
# For instance, a half note at offset 2.0 will be found in getElementsByOffset(1.5, 2.5) or getElementsByOffset(1.5, 2.5, mustFinishInSpan=False) but not by getElementsByOffset(1.5, 2.5, mustFinishInSpan=True).
# 
# The includeEndBoundary option determines if an element begun just at the offsetEnd should be included. For instance, the half note at offset 2.0 above would be found by getElementsByOffset(0, 2.0) or by getElementsByOffset(0, 2.0, includeEndBoundary=True) but not by getElementsByOffset(0, 2.0, includeEndBoundary=False).
# 
# Setting includeEndBoundary to False at the same time as mustFinishInSpan is set to True is probably NOT what you want to do unless you want to find things like clefs at the end of the region to display as courtesy clefs.
# 
# The mustBeginInSpan option determines whether notes or other objects that do not begin in the region but are still sounding at the beginning of the region are excluded. The default is True – that is, these notes will not be included. For instance the half note at offset 2.0 from above would not be found by getElementsByOffset(3.0, 3.5) or getElementsByOffset(3.0, 3.5, mustBeginInSpan=True) but it would be found by getElementsByOffset(3.0, 3.5, mustBeginInSpan=False)
# 
# Setting includeElementsThatEndAtStart to False is useful for zeroLength searches that set mustBeginInSpan == False to not catch notes that were playing before the search but that end just before the end of the search type. This setting is ignored for zero-length searches. See the code for allPlayingWhileSounding for a demonstration.
# 
# This chart, and the examples below, demonstrate the various features of getElementsByOffset. It is one of the most complex methods of music21 but also one of the most powerful, so it is worth learning at least the basics.
# 
# ../_images/getElementsByOffset.png

st1 = stream.Stream()
n0 = note.Note('C')
n0.duration.type = 'half'
n0.offset = 0
st1.insert(n0)
n2 = note.Note('D')
n2.duration.type = 'half'
n2.offset = 2
st1.insert(n2)
out1 = st1.getElementsByOffset(2)
len(out1)
# 1
out1[0].step
# 'D'

out2 = st1.getElementsByOffset(1, 3)
len(out2)
# 1
out2[0].step
# 'D'
out3 = st1.getElementsByOffset(1, 3, mustFinishInSpan=True)
len(out3)
# 0
out4 = st1.getElementsByOffset(1, 2)
len(out4)
# 1
out4[0].step
# 'D'
out5 = st1.getElementsByOffset(1, 2, includeEndBoundary=False)
len(out5)
# 0
out6 = st1.getElementsByOffset(1, 2, includeEndBoundary=False, mustBeginInSpan=False)
len(out6)
# 1
out6[0].step
# 'C'
out7 = st1.getElementsByOffset(1, 3, mustBeginInSpan=False)
len(out7)
# 2
[el.step for el in out7]
# ['C', 'D']
# Note, that elements that end at the start offset are included if mustBeginInSpan is False
# 

out8 = st1.getElementsByOffset(2, 4, mustBeginInSpan=False)
len(out8)
# 2
[el.step for el in out8]
# ['C', 'D']
# To change this behavior set includeElementsThatEndAtStart=False
# 

out9 = st1.getElementsByOffset(2, 4,
# ...                     mustBeginInSpan=False, includeElementsThatEndAtStart=False)
len(out9)
# 1
[el.step for el in out9]
# ['D']
# Note how zeroLengthSearches implicitly set includeElementsThatEndAtStart=False. These two are the same:
# 

out1 = st1.getElementsByOffset(2, mustBeginInSpan=False)
out2 = st1.getElementsByOffset(2, 2, mustBeginInSpan=False)
len(out1) == len(out2) == 1
# True
out1[0] is out2[0] is n2
# True
# But this is different:
# 

out3 = st1.getElementsByOffset(2, 2.1, mustBeginInSpan=False)
len(out3)
# 2
out3[0] is n0
# True
# Explicitly setting includeElementsThatEndAtStart=False does not get the first note:
# 

out4 = st1.getElementsByOffset(2, 2.1, mustBeginInSpan=False,
# ...                                includeElementsThatEndAtStart=False)
len(out4)
# 1
out4[0] is n2
# True
# Testing multiple zero-length elements with mustBeginInSpan:
# 

tc = clef.TrebleClef()
ts = meter.TimeSignature('4/4')
ks = key.KeySignature(2)
s = stream.Stream()
s.insert(0.0, tc)
s.insert(0.0, ts)
s.insert(0.0, ks)
len(s.getElementsByOffset(0.0, mustBeginInSpan=True))
# 3
len(s.getElementsByOffset(0.0, mustBeginInSpan=False))
# 3
# Stream.getElementsNotOfClass(classFilterList) → music21.stream.iterator.StreamIterator
# Return a list of all Elements that do not match the one or more classes in the classFilterList.
# 
# In lieu of a list, a single class can be used as the classFilterList parameter.
# 

a = stream.Stream()
a.repeatInsert(note.Rest(), list(range(10)))
for x in range(4):
# ...     n = note.Note('G#')
# ...     n.offset = x * 3
# ...     a.insert(n)
found = a.getElementsNotOfClass(note.Note)
len(found)
# 10

b = stream.Stream()
b.repeatInsert(note.Rest(), list(range(15)))
a.insert(b)
# Here, it gets elements from within a stream this probably should not do this, as it is one layer lower
# 

found = a.flat.getElementsNotOfClass(note.Rest)
len(found)
# 4
found = a.flat.getElementsNotOfClass(note.Note)
len(found)
# 25
# Stream.getInstrument(searchActiveSite=True, returnDefault=True)
# Return the first Instrument found in this Stream.
# 

s = stream.Score()
p1 = stream.Part()
p1.insert(instrument.Violin())
m1p1 = stream.Measure()
m1p1.append(note.Note('g'))
p1.append(m1p1)

p2 = stream.Part()
p2.insert(instrument.Viola())
m1p2 = stream.Measure()
m1p2.append(note.Note('f#'))
p2.append(m1p2)

s.insert(0, p1)
s.insert(0, p2)
p1.getInstrument(returnDefault=False).instrumentName
# 'Violin'
p2.getInstrument(returnDefault=False).instrumentName
# 'Viola'
# Stream.getInstruments(searchActiveSite=True, returnDefault=True, recurse=False)
# Search this stream or activeSite streams for Instrument objects, otherwise return a default Instrument
# 
# Stream.getKeySignatures(searchActiveSite=True, searchContext=True)
# Collect all KeySignature objects in this Stream in a new Stream. Optionally search the activeSite stream and/or contexts.
# 
# If no KeySignature objects are defined, returns an empty Stream
# 
# TO BE DEPRECATED…
# 

a = stream.Stream()
b = key.KeySignature(3)
a.insert(0, b)
a.repeatInsert(note.Note('C#'), list(range(10)))
c = a.getKeySignatures()
len(c) == 1
# True
# Stream.getOverlaps()
# Find any elements that overlap. Overlapping might include elements that have zero-length duration simultaneous.
# 
# This method returns a dictionary, where keys are the start time of the first overlap and value are a list of all objects included in that overlap group.
# 
# This example demonstrates that end-joining overlaps do not count.
# 

a = stream.Stream()
for x in range(4):
# ...     n = note.Note('G#')
# ...     n.duration = duration.Duration('quarter')
# ...     n.offset = x * 1
# ...     a.insert(n)
# ...
d = a.getOverlaps()
len(d)
# 0
# Notes starting at the same time overlap:
# 

a = stream.Stream()
for x in [0, 0, 0, 0, 13, 13, 13]:
# ...     n = note.Note('G#')
# ...     n.duration = duration.Duration('half')
# ...     n.offset = x
# ...     a.insert(n)
# ...
d = a.getOverlaps()
len(d[0])
# 4
len(d[13])
# 3
a = stream.Stream()
for x in [0, 0, 0, 0, 3, 3, 3]:
# ...     n = note.Note('G#')
# ...     n.duration = duration.Duration('whole')
# ...     n.offset = x
# ...     a.insert(n)
# ...
# Default is to not include coincident boundaries
# 

d = a.getOverlaps()
len(d[0])
# 7
# Stream.getTimeSignatures(*, searchContext=True, returnDefault=True, sortByCreationTime=True)
# Collect all TimeSignature objects in this stream. If no TimeSignature objects are defined, get a default (4/4 or whatever is defined in the defaults.py file).
# 

a = stream.Stream()
b = meter.TimeSignature('3/4')
a.insert(b)
a.repeatInsert(note.Note('C#'), list(range(10)))
c = a.getTimeSignatures()
len(c) == 1
# True
# Stream.hasElement(obj)
# Return True if an element, provided as an argument, is contained in this Stream.
# 
# This method is based on object equivalence, not parameter equivalence of different objects.
# 

s = stream.Stream()
n1 = note.Note('g')
n2 = note.Note('g#')
s.append(n1)
s.hasElement(n1)
# True
# Stream.hasElementOfClass(className, forceFlat=False)
# Given a single class name as string, return True or False if an element with the specified class is found.
# 
# Only a single class name can be given.
# 
# Possibly to be deprecated in v.5
# 

s = stream.Stream()
s.append(meter.TimeSignature('5/8'))
s.append(note.Note('d-2'))
s.insert(dynamics.Dynamic('fff'))
s.hasElementOfClass('TimeSignature')
# True
s.hasElementOfClass('Measure')
# False
# Stream.hasMeasures()
# Return a boolean value showing if this Stream contains Measures.
# 

s = stream.Stream()
s.repeatAppend(note.Note(), 8)
s.hasMeasures()
# False
s.makeMeasures(inPlace=True)
len(s.getElementsByClass('Measure'))
# 2
s.hasMeasures()
# True
# Stream.hasPartLikeStreams()
# Return a boolean value showing if this Stream contains any Parts, or Part-like sub-Streams.
# 
# Part-like sub-streams are Streams that contain Measures or Notes. And where no sub-stream begins at an offset besides zero.
# 

s = stream.Score()
s.hasPartLikeStreams()
# False
p1 = stream.Part()
p1.repeatAppend(note.Note(), 8)
s.insert(0, p1)
s.hasPartLikeStreams()
# True
# A stream that has a measure in it is not a part-like stream.
# 

s = stream.Score()
m1 = stream.Measure()
m1.repeatAppend(note.Note(), 4)
s.append(m1)
s.hasPartLikeStreams()
# False
# A stream with a single generic Stream substream at the beginning has part-like Streams…
# 

s = stream.Score()
m1 = stream.Stream()
m1.repeatAppend(note.Note(), 4)
s.append(m1)
s.hasPartLikeStreams()
# True
# Adding another though makes it not part-like.
# 

m2 = stream.Stream()
m2.repeatAppend(note.Note(), 4)
s.append(m2)
s.hasPartLikeStreams()
# False
# Flat objects do not have part-like Streams:
# 

sf = s.flat
sf.hasPartLikeStreams()
# False
# Stream.hasVoices()
# Return a boolean value showing if this Stream contains Voices
# 
# Stream.haveAccidentalsBeenMade()
# If Accidentals.displayStatus is None for all contained pitches, it as assumed that accidentals have not been set for display and/or makeAccidentals has not been run. If any Accidental has displayStatus other than None, this method returns True, regardless of if makeAccidentals has actually been run.
# 
# Stream.index(el)
# Return the first matched index for the specified object.
# 
# Raises a StreamException if cannot be found.
# 

s = stream.Stream()
n1 = note.Note('g')
n2 = note.Note('g#')

s.insert(0, n1)
s.insert(5, n2)
len(s)
# 2
s.index(n1)
# 0
s.index(n2)
# 1

n3 = note.Note('a')
s.index(n3)
# Traceback (most recent call last):
# music21.exceptions21.StreamException: cannot find object (<music21.note.Note A>) in Stream
# Stream.insert(offsetOrItemOrList, itemOrNone=None, ignoreSort=False, setActiveSite=True)
# Inserts an item(s) at the given offset(s).
# 
# If ignoreSort is True then the inserting does not change whether the Stream is sorted or not (much faster if you’re going to be inserting dozens of items that don’t change the sort status)
# 
# The setActiveSite parameter should nearly always be True; only for advanced Stream manipulation would you not change the activeSite after inserting an element.
# 
# Has three forms: in the two argument form, inserts an element at the given offset:
# 

st1 = stream.Stream()
st1.insert(32, note.Note('B-'))
st1.highestOffset
# 32.0
# In the single argument form with an object, inserts the element at its stored offset:
# 

n1 = note.Note('C#')
n1.offset = 30.0
st1 = stream.Stream()
st1.insert(n1)
st2 = stream.Stream()
st2.insert(40.0, n1)
n1.getOffsetBySite(st1)
# 30.0
# In single argument form with a list, the list should contain pairs that alternate offsets and items; the method then, obviously, inserts the items at the specified offsets:
# 

n1 = note.Note('G')
n2 = note.Note('F#')
st3 = stream.Stream()
st3.insert([1.0, n1, 2.0, n2])
n1.getOffsetBySite(st3)
# 1.0
n2.getOffsetBySite(st3)
# 2.0
len(st3)
# 2
# Stream.insertAndShift(offsetOrItemOrList, itemOrNone=None)
# Insert an item at a specified or native offset, and shift any elements found in the Stream to start at the end of the added elements.
# 
# This presently does not shift elements that have durations that extend into the lowest insert position.
# 

st1 = stream.Stream()
st1.insertAndShift(32, note.Note('B'))
st1.highestOffset
# 32.0
st1.insertAndShift(32, note.Note('C'))
st1.highestOffset
# 33.0
st1.show('text', addEndTimes=True)
# {32.0 - 33.0} <music21.note.Note C>
# {33.0 - 34.0} <music21.note.Note B>
# Let’s insert an item at the beginning, note that since the C and B are not affected, they do not shift.
# 

st1.insertAndShift(0, note.Note('D'))
st1.show('text', addEndTimes=True)
# {0.0 - 1.0} <music21.note.Note D>
# {32.0 - 33.0} <music21.note.Note C>
# {33.0 - 34.0} <music21.note.Note B>
# But if we insert something again at the beginning of the stream, everything after the first shifted note begins shifting, so the C and the B shift even though there is a gap there. Normally there’s no gaps in a stream, so this will not be a factor:
# 

st1.insertAndShift(0, note.Note('E'))
st1.show('text', addEndTimes=True)
# {0.0 - 1.0} <music21.note.Note E>
# {1.0 - 2.0} <music21.note.Note D>
# {33.0 - 34.0} <music21.note.Note C>
# {34.0 - 35.0} <music21.note.Note B>
# In the single argument form with an object, inserts the element at its stored offset:
# 

n1 = note.Note('C#')
n1.offset = 30.0
n2 = note.Note('D#')
n2.offset = 30.0
st1 = stream.Stream()
st1.insertAndShift(n1)
st1.insertAndShift(n2)  # will shift offset of n1
n1.getOffsetBySite(st1)
# 31.0
n2.getOffsetBySite(st1)
# 30.0
st1.show('text', addEndTimes=True)
# {30.0 - 31.0} <music21.note.Note D#>
# {31.0 - 32.0} <music21.note.Note C#>

st2 = stream.Stream()
st2.insertAndShift(40.0, n1)
st2.insertAndShift(40.0, n2)
n1.getOffsetBySite(st2)
# 41.0
# In single argument form with a list, the list should contain pairs that alternate offsets and items; the method then, obviously, inserts the items at the specified offsets:
# 

n1 = note.Note('G-')
n2 = note.Note('F-')
st3 = stream.Stream()
st3.insertAndShift([1.0, n1, 2.0, n2])
n1.getOffsetBySite(st3)
# 1.0
n2.getOffsetBySite(st3)
# 2.0
len(st3)
# 2
st3.show('text', addEndTimes=True)
# {1.0 - 2.0} <music21.note.Note G->
# {2.0 - 3.0} <music21.note.Note F->
# N.B. – using this method on a list assumes that you’ll be inserting contiguous objects; you can’t shift things that are separated, as this following FAILED example shows.
# 

n1 = note.Note('G', type='half')
st4 = stream.Stream()
st4.repeatAppend(n1, 3)
st4.insertAndShift([2.0, note.Note('e'), 4.0, note.Note('f')])
st4.show('text')
# {0.0} <music21.note.Note G>
# {2.0} <music21.note.Note E>
# {4.0} <music21.note.Note F>
# {5.0} <music21.note.Note G>
# {7.0} <music21.note.Note G>
# As an FYI, there is no removeAndShift() function, so the opposite of insertAndShift(el) is remove(el, shiftOffsets=True).
# 
# Stream.insertIntoNoteOrChord(offset, noteOrChord, chordsOnly=False)
# Insert a Note or Chord into an offset position in this Stream. If there is another Note or Chord in this position, create a new Note or Chord that combines the pitches of the inserted chord. If there is a Rest in this position, the Rest is replaced by the Note or Chord. The duration of the previously-found chord will remain the same in the new Chord.
# 

n1 = note.Note('D4')
n1.duration.quarterLength = 2.0
r1 = note.Rest()
r1.duration.quarterLength = 2.0
c1 = chord.Chord(['C4', 'E4'])
s = stream.Stream()
s.append(n1)
s.append(r1)
s.append(c1)
s.show('text')
# {0.0} <music21.note.Note D>
# {2.0} <music21.note.Rest rest>
# {4.0} <music21.chord.Chord C4 E4>
# Save the original Stream for later
# 

import copy
s2 = copy.deepcopy(s)
# Notice that the duration of the inserted element is not taken into consideration and the original element is not broken up, as it would be in chordify(). But Chords and Notes are created…
# 

for i in [0.0, 2.0, 4.0]:
# ...     s.insertIntoNoteOrChord(i, note.Note('F#4'))
s.show('text')
# {0.0} <music21.chord.Chord D4 F#4>
# {2.0} <music21.note.Note F#>
# {4.0} <music21.chord.Chord C4 E4 F#4>
# if chordsOnly is set to True then no notes are returned, only chords:
# 

for i in [0.0, 2.0, 4.0]:
# ...     s2.insertIntoNoteOrChord(i, note.Note('F#4'), chordsOnly=True)
s2.show('text')
# {0.0} <music21.chord.Chord D4 F#4>
# {2.0} <music21.chord.Chord F#4>
# {4.0} <music21.chord.Chord C4 E4 F#4>
# Stream.invertDiatonic(inversionNote=<music21.note.Note C>, *, inPlace=False)
# inverts a stream diatonically around the given note (by default, middle C)
# 
# For pieces where the key signature does not change throughout the piece it is MUCH faster than for pieces where the key signature changes.
# 
# Here in this test, we put Ciconia’s Quod Jactatur (a single voice piece that should have a canon solution: see trecento.quodJactatur) into 3 flats (instead of its original 1 flat) in measure 1, but into 5 sharps in measure 2 and then invert around F4, creating a new piece.
# 
# Changed in v. 5 – inPlace is False by default.
# 

qj = corpus.parse('ciconia/quod_jactatur').parts[0].measures(1, 2)
qj.id = 'measureExcerpt'

qj.show('text')
# {0.0} <music21.instrument.Instrument 'P1: MusicXML Part: Grand Piano'>
# {0.0} <music21.stream.Measure 1 offset=0.0>
    # {0.0} <music21.layout.SystemLayout>
    # {0.0} <music21.clef.Treble8vbClef>
    # {0.0} <music21.key.Key of F major>
    # {0.0} <music21.meter.TimeSignature 2/4>
    # {0.0} <music21.note.Note C>
    # {1.5} <music21.note.Note D>
# {2.0} <music21.stream.Measure 2 offset=2.0>
    # {0.0} <music21.note.Note E>
    # {0.5} <music21.note.Note D>
    # {1.0} <music21.note.Note C>
    # {1.5} <music21.note.Note D>

qjFlat = qj.flat
k1 = qjFlat.getElementsByClass(key.KeySignature)[0]
k3flats = key.KeySignature(-3)
qjFlat.replace(k1, k3flats, allDerived=True)
qj.getElementsByClass(stream.Measure)[1].insert(0, key.KeySignature(5))

qj2 = qj.invertDiatonic(note.Note('F4'), inPlace=False)
qj2.show('text')
# {0.0} <music21.instrument.Instrument 'P1: MusicXML Part: Grand Piano'>
# {0.0} <music21.stream.Measure 1 offset=0.0>
    # {0.0} <music21.layout.SystemLayout>
    # {0.0} <music21.clef.Treble8vbClef>
    # {0.0} <music21.key.KeySignature of 3 flats>
    # {0.0} <music21.meter.TimeSignature 2/4>
    # {0.0} <music21.note.Note B->
    # {1.5} <music21.note.Note A->
# {2.0} <music21.stream.Measure 2 offset=2.0>
    # {0.0} <music21.key.KeySignature of 5 sharps>
    # {0.0} <music21.note.Note G#>
    # {0.5} <music21.note.Note A#>
    # {1.0} <music21.note.Note B>
    # {1.5} <music21.note.Note A#>
# Stream.isSequence()
# A stream is a sequence if it has no overlaps.
# 

a = stream.Stream()
for x in [0, 0, 0, 0, 3, 3, 3]:
# ...     n = note.Note('G#')
# ...     n.duration = duration.Duration('whole')
# ...     n.offset = x * 1
# ...     a.insert(n)
# ...
a.isSequence()
# False
# Stream.isTwelveTone()
# Return true if this Stream only employs twelve-tone equal-tempered pitch values.
# 

s = stream.Stream()
s.append(note.Note('G#4'))
s.isTwelveTone()
# True
s.append(note.Note('G~4'))
s.isTwelveTone()
# False
# Stream.isWellFormedNotation()
# Return True if, given the context of this Stream or Stream subclass, contains what appears to be well-formed notation. This often means the formation of Measures, or a Score that contains Part with Measures.
# 

s = corpus.parse('bwv66.6')
s.isWellFormedNotation()
# True
s.parts[0].isWellFormedNotation()
# True
s.parts[0].getElementsByClass('Measure')[0].isWellFormedNotation()
# True

s = stream.Score()
m = stream.Measure()
s.append(m)
s.isWellFormedNotation()
# False
# Stream.lyrics(ignoreBarlines=True, recurse=False, skipTies=False)
# Returns a dict of lists of lyric objects (with the keys being the lyric numbers) found in self. Each list will have an element for each note in the stream (which may be a note.Lyric() or None). By default, this method automatically recurses through measures, but not other container streams.
# 

s = converter.parse('tinynotation: 4/4 a4 b c d   e f g a', makeNotation=False)
someLyrics = ['this', 'is', 'a', 'list', 'of', 'eight', 'lyric', 'words']
for n, lyric in zip(s.notes, someLyrics):
# ...     n.lyric = lyric

s.lyrics()
# {1: [<music21.note.Lyric number=1 syllabic=single text='this'>, ...,
     # <music21.note.Lyric number=1 syllabic=single text='words'>]}

s.notes[3].lyric = None
s.lyrics()[1]
# [<music21.note.Lyric number=1 syllabic=single text='this'>, ..., None, ...,
 # <music21.note.Lyric number=1 syllabic=single text='words'>]
# If ignoreBarlines is True, it will behave as if the elements in measures are all in a flattened stream (note that this is not stream.flat as it does not copy the elements) together without measure containers. This means that even if recurse is False, lyrics() will still essentially recurse through measures.
# 

s.makeMeasures(inPlace=True)
s.lyrics()[1]
# [<music21.note.Lyric number=1 syllabic=single text='this'>, ..., None, ...,
 # <music21.note.Lyric number=1 syllabic=single text='words'>]

list(s.lyrics(ignoreBarlines=False).keys())
# []
# If recurse is True, this method will recurse through all container streams and build a nested list structure mirroring the hierarchy of the stream. Note that if ignoreBarlines is True, measure structure will not be reflected in the hierarchy, although if ignoreBarlines is False, it will.
# 
# Note that streams which do not contain any instance of a lyric number will not appear anywhere in the final list (not as a [] or otherwise).
# 

p = stream.Part(s)
scr = stream.Score()
scr.append(p)

scr.lyrics(ignoreBarlines=False, recurse=True)[1]
# [[[<music21.note.Lyric number=1 syllabic=single text='this'>, <...'is'>, <...'a'>, None],
  # [<...'of'>, <...'eight'>, <...'lyric'>, <...'words'>]]]
# Notice that the measures are nested in the part which is nested in the score.
# 

scr.lyrics(ignoreBarlines=True, recurse=True)[1]
# [[<music21.note.Lyric number=1 syllabic=single text='this'>, <...'is'>, <...'a'>, None,
  # <...'of'>, <...'eight'>, <...'lyric'>, <...'words'>]]
# Notice that this time, the measure structure is ignored.
# 

list(scr.lyrics(ignoreBarlines=True, recurse=False).keys())
# []
# Stream.makeAccidentals(pitchPast=None, pitchPastMeasure=None, useKeySignature=True, alteredPitches=None, searchKeySignatureByContext=False, cautionaryPitchClass=True, cautionaryAll=False, inPlace=True, overrideStatus=False, cautionaryNotImmediateRepeat=True, tiePitchSet=None)
# A method to set and provide accidentals given various conditions and contexts.
# 
# pitchPast is a list of pitches preceding this pitch in this measure.
# 
# pitchPastMeasure is a list of pitches preceding this pitch but in a previous measure.
# 
# If useKeySignature is True, a KeySignature will be searched for in this Stream or this Stream’s defined contexts. An alternative KeySignature can be supplied with this object and used for temporary pitch processing.
# 
# If alteredPitches is a list of modified pitches (Pitches with Accidentals) that can be directly supplied to Accidental processing. These are the same values obtained from a music21.key.KeySignature object using the alteredPitches property.
# 
# If cautionaryPitchClass is True, comparisons to past accidentals are made regardless of register. That is, if a past sharp is found two octaves above a present natural, a natural sign is still displayed.
# 
# If cautionaryAll is True, all accidentals are shown.
# 
# If overrideStatus is True, this method will ignore any current displayStatus stetting found on the Accidental. By default this does not happen. If displayStatus is set to None, the Accidental’s displayStatus is set.
# 
# If cautionaryNotImmediateRepeat is True, cautionary accidentals will be displayed for an altered pitch even if that pitch had already been displayed as altered.
# 
# If tiePitchSet is not None it should be a set of .nameWithOctave strings to determine whether following accidentals should be shown because the last note of the same pitch had a start or continue tie.
# 
# The updateAccidentalDisplay() method is used to determine if an accidental is necessary.
# 
# This will assume that the complete Stream is the context of evaluation. For smaller context ranges, call this on Measure objects.
# 
# If inPlace is True, this is done in-place; if inPlace is False, this returns a modified deep copy.
# 
# TODO: inPlace default should become False TODO: if inPlace is True return None
# 
# Stream.makeBeams(*, inPlace=False)
# Return a new Stream, or modify the Stream in place, with beams applied to all notes.
# 
# See makeBeams().
# 
# Stream.makeChords(minimumWindowSize=0.125, includePostWindow=True, removeRedundantPitches=True, useExactOffsets=False, gatherArticulations=True, gatherExpressions=True, inPlace=False, transferGroupsToPitches=False, makeRests=True)
# TO BE DEPRECATED SOON! Use Chordify instead!
# 
# Gathers simultaneously sounding Note objects into Chord objects, each of which contains all the pitches sounding together.
# 
# If useExactOffsets is True (default=False), then do an exact makeChords using the offsets in the piece. If this parameter is set, then minimumWindowSize is ignored.
# 
# This first example puts a part with three quarter notes (C4, D4, E4) together with a part consisting of a half note (C#5) and a quarter note (E#5) to make two Chords, the first containing the three Pitch objects sounding at the beginning, the second consisting of the two Pitches sounding on offset 2.0 (beat 3):
# 

p1 = stream.Part()
p1.append([note.Note('C4', type='quarter'),
# ...            note.Note('D4', type='quarter'),
# ...            note.Note('E4', type='quarter'),
# ...            note.Note('B2', type='quarter')])
p2 = stream.Part()
p2.append([note.Note('C#5', type='half'),
# ...            note.Note('E#5', type='quarter'),
# ...            chord.Chord(['E4', 'G5', 'C#7'])])
sc1 = stream.Score()
sc1.insert(0, p1)
sc1.insert(0, p2)
scChords = sc1.flat.makeChords()
scChords.show('text')
# {0.0} <music21.chord.Chord C4 C#5 D4>
# {2.0} <music21.chord.Chord E4 E#5>
# {3.0} <music21.chord.Chord B2 E4 G5 C#7>
# The gathering of elements, starting from offset 0.0, uses the minimumWindowSize, in quarter lengths, to collect all Notes that start between 0.0 and the minimum window size (this permits overlaps within a minimum tolerance).
# 
# After collection, the maximum duration of collected elements is found; this duration is then used to set the new starting offset. A possible gap then results between the end of the window and offset specified by the maximum duration; these additional notes are gathered in a second pass if includePostWindow is True.
# 
# The new start offset is shifted to the larger of either the minimum window or the maximum duration found in the collected group. The process is repeated until all offsets are covered.
# 
# Each collection of Notes is formed into a Chord. The Chord is given the longest duration of all constituents, and is inserted at the start offset of the window from which it was gathered.
# 
# Chords can gather both articulations and expressions from found Notes using gatherArticulations and gatherExpressions.
# 
# If transferGroupsToPitches is True, and group defined on the source elements Groups object will be transferred to the Pitch objects contained in the resulting Chord.
# 
# The resulting Stream, if not in-place, can also gather additional objects by placing class names in the collect list. By default, TimeSignature and KeySignature objects are collected.
# 
# Stream.makeImmutable()
# Clean this Stream: for self and all elements, purge all dead locations and remove all non-contained sites. Further, restore all active sites.
# 
# Stream.makeMeasures(meterStream=None, refStreamOrTimeRange=None, searchContext=False, innerBarline=None, finalBarline='final', bestClef=False, inPlace=False)
# Return a new stream (or if inPlace=True change in place) this Stream so that it has internal measures.
# 
# For more details, see makeMeasures().
# 
# Stream.makeMutable(recurse=True)
# Stream.makeNotation(meterStream=None, refStreamOrTimeRange=None, inPlace=False, bestClef=False, **subroutineKeywords)
# This method calls a sequence of Stream methods on this Stream to prepare notation, including creating voices for overlapped regions, Measures if necessary, creating ties, beams, and accidentals.
# 
# If inPlace is True, this is done in-place; if inPlace is False, this returns a modified deep copy.
# 
# makeAccidentalsKeywords can be a dict specifying additional parameters to send to makeAccidentals
# 

s = stream.Stream()
n = note.Note('g')
n.quarterLength = 1.5
s.repeatAppend(n, 10)
sMeasures = s.makeNotation()
len(sMeasures.getElementsByClass('Measure'))
# 4
sMeasures.getElementsByClass('Measure')[-1].rightBarline.type
# 'final'
# Stream.makeRests(refStreamOrTimeRange=None, fillGaps=False, timeRangeFromBarDuration=False, inPlace=True, hideRests=False)
# Calls makeRests().
# 
# Stream.makeTies(meterStream=None, inPlace=False, displayTiedAccidentals=False)
# Calls makeTies().
# 
# Changed in v.4., inPlace=False by default.
# 
# Stream.makeVariantBlocks()
# from music21 import *
# 
# Stream.makeVoices(*, inPlace=False, fillGaps=True)
# If this Stream has overlapping Notes or Chords, this method will isolate all overlaps in unique Voices, and place those Voices in the Stream.
# 

s = stream.Stream()
s.insert(0, note.Note('C4', quarterLength=4))
s.repeatInsert(note.Note('b-4', quarterLength=0.5), [x * 0.5 for x in list(range(8))])
s.makeVoices(inPlace=True)
len(s.voices)
# 2
[n.pitch for n in s.voices[0].notes]
# [<music21.pitch.Pitch C4>]
[str(n.pitch) for n in s.voices[1].notes]
# ['B-4', 'B-4', 'B-4', 'B-4', 'B-4', 'B-4', 'B-4', 'B-4']
# Stream.measure(measureNumber, collect=('Clef', 'TimeSignature', 'Instrument', 'KeySignature'), indicesNotNumbers=False)
# Given a measure number, return a single Measure object if the Measure number exists, otherwise return None.
# 
# This method is distinguished from measures() in that this method returns a single Measure object, not a Stream containing one or more Measure objects.
# 

a = corpus.parse('bach/bwv324.xml')
a.parts[0].measure(3)
# <music21.stream.Measure 3 offset=8.0>
# See measures() for an explanation of collect and indicesNotNumbers
# 
# To get the last measure of a piece, use -1 as a measureNumber – this will turn on indicesNotNumbers if it is off:
# 

a.parts[0].measure(-1)
# <music21.stream.Measure 9 offset=38.0>
# Getting a non-existent measure will return None:
# 

print(a.parts[0].measure(99))
# None
# Stream.measureOffsetMap(classFilterList=None)
# If this Stream contains Measures, provide an OrderedDict whose keys are the offsets of the start of each measure and whose values are a list of references to the Measure objects that start at that offset.
# 
# Even in normal music there may be more than one Measure starting at each offset because each Part might define its own Measure. However, you are unlikely to encounter such things unless you run Score.semiFlat, which retains all the containers found in the score.
# 
# The offsets are always measured relative to the calling Stream (self).
# 
# You can specify a classFilterList argument as a list of classes to find instead of Measures. But the default will of course find Measure objects.
# 
# Example 1: This Bach chorale is in 4/4 without a pickup, so as expected, measures are found every 4 offsets, until the weird recitation in m. 7 which in our edition lasts 10 beats and thus causes a gap in measureOffsetMap from 24.0 to 34.0.
# 
# ../_images/streamMeasureOffsetMapBWV324.png

chorale = corpus.parse('bach/bwv324.xml')
alto = chorale.parts['alto']
altoMeasures = alto.measureOffsetMap()
list(altoMeasures.keys())
# [0.0, 4.0, 8.0, 12.0, 16.0, 20.0, 24.0, 34.0, 38.0]
# altoMeasures is a dictionary (hash) of the measures that are found in the alto part, so we can get the measure beginning on offset 4.0 (measure 2) and display it (though it’s the only measure found at offset 4.0, there might be others as in example 2, so we need to call altoMeasures[4.0][0] to get this measure.):
# 

altoMeasures[4.0]
# [<music21.stream.Measure 2 offset=4.0>]
altoMeasures[4.0][0].show('text')
# {0.0} <music21.note.Note D>
# {1.0} <music21.note.Note D#>
# {2.0} <music21.note.Note E>
# {3.0} <music21.note.Note F#>
# Example 2: How to get all the measures from all parts (not the most efficient way, but it works!). Note that you first need to call semiFlat, which finds all containers (and other elements) nested inside all parts:
# 

choraleSemiFlat = chorale.semiFlat
choraleMeasures = choraleSemiFlat.measureOffsetMap()
choraleMeasures[4.0]
# [<music21.stream.Measure 2 offset=4.0>,
 # <music21.stream.Measure 2 offset=4.0>,
 # <music21.stream.Measure 2 offset=4.0>,
 # <music21.stream.Measure 2 offset=4.0>]
# Stream.measures(numberStart, numberEnd, collect=('Clef', 'TimeSignature', 'Instrument', 'KeySignature'), gatherSpanners=True, indicesNotNumbers=False)
# Get a region of Measures based on a start and end Measure number where the boundary numbers are both included.
# 
# That is, a request for measures 4 through 10 will return 7 Measures, numbers 4 through 10.
# 
# Additionally, any number of associated classes can be gathered from the context and put into the measure. By default we collect the Clef, TimeSignature, KeySignature, and Instrument so that there is enough context to perform. (See getContextByClass() and .previous() for definitions of the context)
# 
# While all elements in the source are the original elements in the extracted region, new Measure objects are created and returned.
# 

bachIn = corpus.parse('bach/bwv66.6')
bachExcerpt = bachIn.parts[0].measures(1, 3)
len(bachExcerpt.getElementsByClass('Measure'))
# 3
# Because bwv66.6 has a pickup measure, and we requested to start at measure 1, this is NOT true:
# 

firstExcerptMeasure = bachExcerpt.getElementsByClass('Measure')[0]
firstBachMeasure = bachIn.parts[0].getElementsByClass('Measure')[0]
firstExcerptMeasure is firstBachMeasure
# False
firstBachMeasure.number
# 0
firstExcerptMeasure.number
# 1
# To get all measures from the beginning, go ahead and always request measure 0 to x, there will be no error if there is not a pickup measure.
# 

bachExcerpt = bachIn.parts[0].measures(0, 3)
excerptNote = bachExcerpt.getElementsByClass('Measure')[0].notes[0]
originalNote = bachIn.parts[0].flat.notes[0]
excerptNote is originalNote
# True
# if indicesNotNumbers is True, then it ignores defined measureNumbers and uses 0-indexed measure objects and half-open range. For instance, if you have a piece that goes “m1, m2, m3, m4, …” (like a standard piece without pickups, then .measures(1, 3, indicesNotNumbers=True) would return measures 2 and 3, because it is interpreted as the slice from object with index 1, which is measure 2 (m1 has index 0) up to but NOT including the object with index 3, which is measure 4. IndicesNotNumbers is like a Python-slice.
# 

bachExcerpt2 = bachIn.parts[0].measures(0, 2, indicesNotNumbers=True)
for m in bachExcerpt2.getElementsByClass('Measure'):
# ...     print(m)
# ...     print(m.number)
# <music21.stream.Measure 0 offset=0.0>
# 0
# <music21.stream.Measure 1 offset=1.0>
# 1
# If numberEnd=None then it is interpreted as the last measure of the stream:
# 

bachExcerpt3 = bachIn.parts[0].measures(7, None)
for m in bachExcerpt3.getElementsByClass('Measure'):
# ...     print(m)
# <music21.stream.Measure 7 offset=0.0>
# <music21.stream.Measure 8 offset=4.0>
# <music21.stream.Measure 9 offset=8.0>
# Note that the offsets in the new stream are shifted so that the first measure in the excerpt begins at 0.0
# 
# The measure elements are the same objects as the original:
# 

lastExcerptMeasure = bachExcerpt3.getElementsByClass('Measure')[-1]
lastOriginalMeasure = bachIn.parts[0].getElementsByClass('Measure')[-1]
lastExcerptMeasure is lastOriginalMeasure
# True
# At the beginning of the Stream returned, before the measures will be some additional objects so that the context is properly preserved:
# 

for thing in bachExcerpt3:
# ...     print(thing)
# P1: Soprano: Instrument 1
# <music21.clef.TrebleClef>
# f# minor
# <music21.meter.TimeSignature 4/4>
# <music21.stream.Measure 7 offset=0.0>
# <music21.stream.Measure 8 offset=4.0>
# <music21.stream.Measure 9 offset=8.0>
# Collecting gets the most recent element in the context of the stream:
# 

bachIn.parts[0].insert(10, key.Key('D-'))
bachExcerpt4 = bachIn.parts[0].measures(7, None)
for thing in bachExcerpt4:
# ...     print(thing)
# P1: Soprano: Instrument 1
# <music21.clef.TrebleClef>
# D- major
# ...
# What is collected is determined by the “collect” iterable. To collect nothing send an empty list:
# 

bachExcerpt5 = bachIn.parts[0].measures(8, None, collect=[])
for thing in bachExcerpt5:
# ...     print(thing)
# <music21.stream.Measure 8 offset=0.0>
# <music21.stream.Measure 9 offset=4.0>
# if gatherSpanners is True then all spanners in the score are gathered and included. (this behavior may change in the future)
# 
# Stream.melodicIntervals(*skipArgs, **skipKeywords)
# Returns a Stream of Interval objects between Notes (and by default, Chords) that follow each other in a stream. the offset of the Interval is the offset of the beginning of the interval (if two notes are adjacent, then this offset is equal to the offset of the second note, but if skipRests is set to True or there is a gap in the Stream, then these two numbers will be different).
# 
# See findConsecutiveNotes() in this class for a discussion of what is meant by default for “consecutive notes”, and which keywords such as skipChords, skipRests, skipUnisons, etc. can be used to change that behavior.
# 
# The interval between a Note and a Chord (or between two chords) is the interval to the first pitch of the Chord (pitches[0]) which is usually the lowest. For more complex interval calculations, run findConsecutiveNotes() and then calculate your own intervals directly.
# 
# Returns an empty Stream if there are not at least two elements found by findConsecutiveNotes.
# 

s1 = converter.parse("tinynotation: 3/4 c4 d' r b b'", makeNotation=False)
s1.show()
# ../_images/streamMelodicIntervals1.png

intervalStream1 = s1.melodicIntervals()
intervalStream1.show('text')
# {1.0} <music21.interval.Interval M9>
# {4.0} <music21.interval.Interval P8>

M9 = intervalStream1[0]
M9.noteStart.nameWithOctave, M9.noteEnd.nameWithOctave
# ('C4', 'D5')
# Using the skip attributes from findConsecutiveNotes(), we can alter which intervals are reported:
# 

intervalStream2 = s1.melodicIntervals(skipRests=True, skipOctaves=True)
intervalStream2.show('text')
# {1.0} <music21.interval.Interval M9>
# {2.0} <music21.interval.Interval m-3>

m3 = intervalStream2[1]
m3.directedNiceName
# 'Descending Minor Third'
# Stream.mergeAttributes(other)
# Merge relevant attributes from the Other stream into this one.
# 

s = stream.Stream()
s.append(note.Note())
s.autoSort = False
s.id = 'hi'
t = stream.Stream()
t.mergeAttributes(s)
t.autoSort
# False
t
# <music21.stream.Stream hi>
len(t)
# 0
# Stream.mergeElements(other, classFilterList=None)
# Given another Stream, store references of each element in the other Stream in this Stream. This does not make copies of any elements, but simply stores all of them in this Stream.
# 
# Optionally, provide a list of classes to exclude with the classFilter list.
# 
# This method provides functionality like a shallow copy, but manages locations properly, only copies elements, and permits filtering by class type.
# 

s1 = stream.Stream()
s2 = stream.Stream()
n1 = note.Note('f#')
n2 = note.Note('g')
s1.append(n1)
s1.append(n2)
s2.mergeElements(s1)
len(s2)
# 2
s1[0] is s2[0]
# True
s1[1] is s2[1]
# True
# Stream.metronomeMarkBoundaries(srcObj=None)
# Return a list of offset start, offset end, MetronomeMark triples for all TempoIndication objects found in this Stream or a Stream provided by srcObj.
# 
# If no MetronomeMarks are found, or an initial region does not have a MetronomeMark, a mark of quarter equal to 120 is provided as default.
# 
# Note that if other TempoIndication objects are defined, they will be converted to MetronomeMarks and returned here
# 

s = stream.Stream()
s.repeatAppend(note.Note(), 8)
s.insert([6, tempo.MetronomeMark(number=240)])
s.metronomeMarkBoundaries()
# [(0.0, 6.0, <music21.tempo.MetronomeMark animato Quarter=120>),
 # (6.0, 8.0, <music21.tempo.MetronomeMark Quarter=240>)]
# Stream.offsetMap(srcObj=None)
# Returns a list where each element is a NamedTuple consisting of the ‘offset’ of each element in a stream, the ‘endTime’ (that is, the offset plus the duration) and the ‘element’ itself. Also contains a ‘voiceIndex’ entry which contains the voice number of the element, or None if there are no voices.
# 

n1 = note.Note(type='quarter')
c1 = clef.AltoClef()
n2 = note.Note(type='half')
s1 = stream.Stream()
s1.append([n1, c1, n2])
om = s1.offsetMap()
om[2].offset
# 1.0
om[2].endTime
# 3.0
om[2].element is n2
# True
om[2].voiceIndex
# Needed for makeMeasures and a few other places
# 
# The Stream source of elements is self by default, unless a srcObj is provided.
# 

s = stream.Stream()
s.repeatAppend(note.Note(), 8)
for om in s.offsetMap():
# ...     om
# OffsetMap(element=<music21.note.Note C>, offset=0.0, endTime=1.0, voiceIndex=None)
# OffsetMap(element=<music21.note.Note C>, offset=1.0, endTime=2.0, voiceIndex=None)
# OffsetMap(element=<music21.note.Note C>, offset=2.0, endTime=3.0, voiceIndex=None)
# OffsetMap(element=<music21.note.Note C>, offset=3.0, endTime=4.0, voiceIndex=None)
# OffsetMap(element=<music21.note.Note C>, offset=4.0, endTime=5.0, voiceIndex=None)
# OffsetMap(element=<music21.note.Note C>, offset=5.0, endTime=6.0, voiceIndex=None)
# OffsetMap(element=<music21.note.Note C>, offset=6.0, endTime=7.0, voiceIndex=None)
# OffsetMap(element=<music21.note.Note C>, offset=7.0, endTime=8.0, voiceIndex=None)
# Stream.playingWhenAttacked(el, elStream=None)
# Given an element (from another Stream) returns the single element in this Stream that is sounding while the given element starts.
# 
# If there are multiple elements sounding at the moment it is attacked, the method returns the first element of the same class as this element, if any. If no element is of the same class, then the first element encountered is returned. For more complex usages, use allPlayingWhileSounding.
# 
# Returns None if no elements fit the bill.
# 
# The optional elStream is the stream in which el is found. If provided, el’s offset in that Stream is used. Otherwise, the current offset in el is used. It is just in case you are paranoid that el.offset might not be what you want, because of some fancy manipulation of el.activeSite
# 

n1 = note.Note('G#')
n2 = note.Note('D#')
s1 = stream.Stream()
s1.insert(20.0, n1)
s1.insert(21.0, n2)

n3 = note.Note('C#')
s2 = stream.Stream()
s2.insert(20.0, n3)
s1.playingWhenAttacked(n3)
# <music21.note.Note G#>

n3.setOffsetBySite(s2, 20.5)
s1.playingWhenAttacked(n3)
# <music21.note.Note G#>

n3.setOffsetBySite(s2, 21.0)
n3.offset
# 21.0
s1.playingWhenAttacked(n3)
# <music21.note.Note D#>
# If there is more than one item at the same time in the other stream then the first item matching the same class is returned, even if another element has a closer offset.
# 

n3.setOffsetBySite(s2, 20.5)
s1.insert(20.5, clef.BassClef())
s1.playingWhenAttacked(n3)
# <music21.note.Note G#>
fc = clef.FClef()  # superclass of BassClef
s2.insert(20.5, fc)
s1.playingWhenAttacked(fc)
# <music21.clef.BassClef>
# But since clefs have zero duration, moving the FClef ever so slightly will find the note instead
# 

fc.setOffsetBySite(s2, 20.6)
s1.playingWhenAttacked(fc)
# <music21.note.Note G#>
# Optionally, specify the site to get the offset from:
# 

n3.setOffsetBySite(s2, 21.0)
n3.setOffsetBySite(None, 100)
n3.activeSite = None
s1.playingWhenAttacked(n3) is None
# True
s1.playingWhenAttacked(n3, s2).name
# 'D#'
# Stream.plot(*args, **keywords)
# Given a method and keyword configuration arguments, create and display a plot.
# 
# Note: plot() requires the Python package matplotlib to be installed.
# 
# For details on arguments this function takes, see User’s Guide, Chapter 22: Graphing.
# 

s = corpus.parse('bach/bwv57.8')
s.plot('pianoroll')
# ../_images/HorizontalBarPitchSpaceOffset.png
# Stream.pop(index)
# Return and remove the object found at the user-specified index value. Index values are those found in elements and are not necessary offset order.
# 

a = stream.Stream()
a.repeatInsert(note.Note('C'), list(range(10)))
junk = a.pop(0)
len(a)
# 9
# Return type
# base.Music21Object
# 
# Stream.quantize(quarterLengthDivisors=None, processOffsets=True, processDurations=True, inPlace=False, recurse=True)
# Quantize time values in this Stream by snapping offsets and/or durations to the nearest multiple of a quarter length value given as one or more divisors of 1 quarter length. The quantized value found closest to a divisor multiple will be used.
# 
# The quarterLengthDivisors provides a flexible way to provide quantization settings. For example, (2,) will snap all events to eighth note grid. (4, 3) will snap events to sixteenth notes and eighth note triplets, whichever is closer. (4, 6) will snap events to sixteenth notes and sixteenth note triplets. If quarterLengthDivisors is not specified then defaults.quantizationQuarterLengthDivisors is used. The default is (4, 3).
# 
# processOffsets determines whether the Offsets are quantized.
# 
# processDurations determines whether the Durations are quantized.
# 
# Both are set to True by default. Setting both to False does nothing to the Stream.
# 
# if inPlace is True then the quantization is done on the Stream itself. If False (default) then a new quantized Stream of the same class is returned.
# 
# If recurse is True then all substreams are also quantized. If False (TODO: MAKE default) then only the highest level of the Stream is quantized.
# 

n = note.Note()
n.quarterLength = 0.49
s = stream.Stream()
s.repeatInsert(n, [0.1, 0.49, 0.9])
nShort = note.Note()
nShort.quarterLength = 0.26
s.repeatInsert(nShort, [1.49, 1.76])

s.quantize([4], processOffsets=True, processDurations=True, inPlace=True)
[e.offset for e in s]
# [0.0, 0.5, 1.0, 1.5, 1.75]
[e.duration.quarterLength for e in s]
# [0.5, 0.5, 0.5, 0.25, 0.25]
# The error in quantization is set in the editorial attribute for the note in two places .offsetQuantizationError and .quarterLengthQuantizationError
# 

[e.editorial.offsetQuantizationError for e in s.notes]
# [0.1, -0.01, -0.1, -0.01, 0.01]
[e.editorial.quarterLengthQuantizationError for e in s.notes]
# [-0.01, -0.01, -0.01, 0.01, 0.01]
# with default quarterLengthDivisors…
# 

s = stream.Stream()
s.repeatInsert(n, [0.1, 0.49, 0.9])
nShort = note.Note()
nShort.quarterLength = 0.26
s.repeatInsert(nShort, [1.49, 1.76])
t = s.quantize(processOffsets=True, processDurations=True, inPlace=False)
[e.offset for e in t]
# [0.0, 0.5, 1.0, 1.5, 1.75]
[e.duration.quarterLength for e in t]
# [0.5, 0.5, 0.5, 0.25, 0.25]
# Stream.recurse(*, streamsOnly=False, restoreActiveSites=True, classFilter=(), skipSelf=True, includeSelf=None)
# Returns an iterator that iterates over a list of Music21Objects contained in the Stream, starting with self (unless skipSelf is True), continuing with self’s elements, and whenever finding a Stream subclass in self, that Stream subclass’s elements.
# 
# Here’s an example. Let’s create a simple score.
# 

s = stream.Score(id='mainScore')
p0 = stream.Part(id='part0')
p1 = stream.Part(id='part1')

m01 = stream.Measure(number=1)
m01.append(note.Note('C', type='whole'))
m02 = stream.Measure(number=2)
m02.append(note.Note('D', type='whole'))
m11 = stream.Measure(number=1)
m11.append(note.Note('E', type='whole'))
m12 = stream.Measure(number=2)
m12.append(note.Note('F', type='whole'))

p0.append([m01, m02])
p1.append([m11, m12])

s.insert(0, p0)
s.insert(0, p1)
s.show('text')
# {0.0} <music21.stream.Part part0>
    # {0.0} <music21.stream.Measure 1 offset=0.0>
        # {0.0} <music21.note.Note C>
    # {4.0} <music21.stream.Measure 2 offset=4.0>
        # {0.0} <music21.note.Note D>
# {0.0} <music21.stream.Part part1>
    # {0.0} <music21.stream.Measure 1 offset=0.0>
        # {0.0} <music21.note.Note E>
    # {4.0} <music21.stream.Measure 2 offset=4.0>
        # {0.0} <music21.note.Note F>
# Now we could assign the .recurse() method to something, but that won’t have much effect:
# 

sRecurse = s.recurse()
sRecurse
# <music21.stream.iterator.RecursiveIterator for Score:mainScore @:0>
# So, that’s not how we use .recurse(). Instead use it in a for loop:
# 

for el in s.recurse(includeSelf=True):
# ...     tup = (el, el.offset, el.activeSite)
# ...     print(tup)
# (<music21.stream.Score mainScore>, 0.0, None)
# (<music21.stream.Part part0>, 0.0, <music21.stream.Score mainScore>)
# (<music21.stream.Measure 1 offset=0.0>, 0.0, <music21.stream.Part part0>)
# (<music21.note.Note C>, 0.0, <music21.stream.Measure 1 offset=0.0>)
# (<music21.stream.Measure 2 offset=4.0>, 4.0, <music21.stream.Part part0>)
# (<music21.note.Note D>, 0.0, <music21.stream.Measure 2 offset=4.0>)
# (<music21.stream.Part part1>, 0.0, <music21.stream.Score mainScore>)
# (<music21.stream.Measure 1 offset=0.0>, 0.0, <music21.stream.Part part1>)
# (<music21.note.Note E>, 0.0, <music21.stream.Measure 1 offset=0.0>)
# (<music21.stream.Measure 2 offset=4.0>, 4.0, <music21.stream.Part part1>)
# (<music21.note.Note F>, 0.0, <music21.stream.Measure 2 offset=4.0>)
# Notice that like calling .show(‘text’), the offsets are relative to their containers.
# 
# Compare the difference between putting classFilter=’Note’ and .flat.notes:
# 

for el in s.recurse(classFilter='Note'):
# ...     tup = (el, el.offset, el.activeSite)
# ...     print(tup)
# (<music21.note.Note C>, 0.0, <music21.stream.Measure 1 offset=0.0>)
# (<music21.note.Note D>, 0.0, <music21.stream.Measure 2 offset=4.0>)
# (<music21.note.Note E>, 0.0, <music21.stream.Measure 1 offset=0.0>)
# (<music21.note.Note F>, 0.0, <music21.stream.Measure 2 offset=4.0>)

for el in s.flat.notes:
# ...     tup = (el, el.offset, el.activeSite)
# ...     print(tup)
# (<music21.note.Note C>, 0.0, <music21.stream.Score mainScore_flat>)
# (<music21.note.Note E>, 0.0, <music21.stream.Score mainScore_flat>)
# (<music21.note.Note D>, 4.0, <music21.stream.Score mainScore_flat>)
# (<music21.note.Note F>, 4.0, <music21.stream.Score mainScore_flat>)
# If you don’t need correct offsets or activeSites, set restoreActiveSites to False. Then the last offset/activeSite will be used. It’s a bit of a speedup, but leads to some bad code, so use it only in highly optimized situations.
# 
# We’ll also test using multiple classes here… the Stream given is the same as the s.flat.notes stream.
# 

for el in s.recurse(classFilter=('Note', 'Rest'), restoreActiveSites=False):
# ...     tup = (el, el.offset, el.activeSite)
# ...     print(tup)
# (<music21.note.Note C>, 0.0, <music21.stream.Score mainScore_flat>)
# (<music21.note.Note D>, 4.0, <music21.stream.Score mainScore_flat>)
# (<music21.note.Note E>, 0.0, <music21.stream.Score mainScore_flat>)
# (<music21.note.Note F>, 4.0, <music21.stream.Score mainScore_flat>)
# So, this is pretty unreliable so don’t use it unless the tiny speedup is worth it.
# 
# The other two attributes are pretty self-explanatory: streamsOnly will put only Streams in, while includeSelf will add the initial stream from recursion. If the inclusion or exclusion of self is important to you, put it in explicitly.
# 

for el in s.recurse(includeSelf=False, streamsOnly=True):
# ...     tup = (el, el.offset, el.activeSite)
# ...     print(tup)
# (<music21.stream.Part part0>, 0.0, <music21.stream.Score mainScore>)
# (<music21.stream.Measure 1 offset=0.0>, 0.0, <music21.stream.Part part0>)
# (<music21.stream.Measure 2 offset=4.0>, 4.0, <music21.stream.Part part0>)
# (<music21.stream.Part part1>, 0.0, <music21.stream.Score mainScore>)
# (<music21.stream.Measure 1 offset=0.0>, 0.0, <music21.stream.Part part1>)
# (<music21.stream.Measure 2 offset=4.0>, 4.0, <music21.stream.Part part1>)
# Warning
# 
# Remember that like all iterators, it is dangerous to alter the components of the Stream being iterated over during iteration. if you need to edit while recursing, list(s.recurse()) is safer.
# 
# Changed in v5.5 – skipSelf is True as promised. All attributes are keyword only. includeSelf is added and now preferred over skipSelf. skipSelf will be removed in or after 2022.
# 
# Stream.remove(targetOrList, *, shiftOffsets=False, recurse=False)
# Remove an object from this Stream. Additionally, this Stream is removed from the object’s sites in Sites.
# 
# If a list of objects is passed, they will all be removed. If shiftOffsets is True, then offsets will be corrected after object removal. It is more efficient to pass a list of objects than to call remove on each object individually if shiftOffsets is True.
# 

import copy
s = stream.Stream()
n1 = note.Note('g')
n2 = note.Note('g#')
# Copies of an object are not the same as the object
# 

n3 = copy.deepcopy(n2)
s.insert(10, n1)
s.insert(5, n2)
s.remove(n1)
len(s)
# 1
s.insert(20, n3)
s.remove(n3)
[e for e in s] == [n2]
# True
# No error is raised if the target is not found.
# 

s.remove(n3)

s2 = stream.Stream()
c = clef.TrebleClef()
n1, n2, n3, n4 = note.Note('a'), note.Note('b'), note.Note('c'), note.Note('d')
n5, n6, n7, n8 = note.Note('e'), note.Note('f'), note.Note('g'), note.Note('a')
s2.insert(0.0, c)
s2.append([n1, n2, n3, n4, n5, n6, n7, n8])
s2.remove(n1, shiftOffsets=True)
s2.show('text')
# {0.0} <music21.clef.TrebleClef>
# {0.0} <music21.note.Note B>
# {1.0} <music21.note.Note C>
# {2.0} <music21.note.Note D>
# {3.0} <music21.note.Note E>
# {4.0} <music21.note.Note F>
# {5.0} <music21.note.Note G>
# {6.0} <music21.note.Note A>

s2.remove([n3, n6, n4], shiftOffsets=True)
s2.show('text')
# {0.0} <music21.clef.TrebleClef>
# {0.0} <music21.note.Note B>
# {1.0} <music21.note.Note E>
# {2.0} <music21.note.Note G>
# {3.0} <music21.note.Note A>
# With the recurse=True parameter, we can remove elements deeply nested. However, shiftOffsets does not work with recurse=True yet.
# 

p1 = stream.Part()
m1 = stream.Measure(number=1)
c = clef.BassClef()
m1.insert(0, c)
m1.append(note.Note(type='whole'))
p1.append(m1)
m2 = stream.Measure(number=2)
n2 = note.Note('D', type='half')
m2.append(n2)
n3 = note.Note(type='half')
m2.append(n3)
p1.append(m2)
p1.show('text')
# {0.0} <music21.stream.Measure 1 offset=0.0>
    # {0.0} <music21.clef.BassClef>
    # {0.0} <music21.note.Note C>
# {4.0} <music21.stream.Measure 2 offset=4.0>
    # {0.0} <music21.note.Note D>
    # {2.0} <music21.note.Note C>
# Without recurse=True:
# 

p1.remove(n2)
p1.show('text')
# {0.0} <music21.stream.Measure 1 offset=0.0>
    # {0.0} <music21.clef.BassClef>
    # {0.0} <music21.note.Note C>
# {4.0} <music21.stream.Measure 2 offset=4.0>
    # {0.0} <music21.note.Note D>
    # {2.0} <music21.note.Note C>
# With recurse=True:
# 

p1.remove(n2, recurse=True)
p1.show('text')
# {0.0} <music21.stream.Measure 1 offset=0.0>
    # {0.0} <music21.clef.BassClef>
    # {0.0} <music21.note.Note C>
# {4.0} <music21.stream.Measure 2 offset=4.0>
    # {2.0} <music21.note.Note C>
# With recurse=True and a list to remove:
# 

p1.remove([c, n3], recurse=True)
p1.show('text')
# {0.0} <music21.stream.Measure 1 offset=0.0>
    # {0.0} <music21.note.Note C>
# {4.0} <music21.stream.Measure 2 offset=4.0>
# <BLANKLINE>
# Changed in v5.3 – firstMatchOnly removed – impossible to have element in stream twice. recurse and shiftOffsets changed to keywordOnly arguments
# 
# Stream.removeByClass(classFilterList)
# Remove all elements from the Stream based on one or more classes given in a list.
# 

s = stream.Stream()
s.append(meter.TimeSignature('4/4'))
s.repeatAppend(note.Note('C'), 8)
len(s)
# 9
s.removeByClass('GeneralNote')
len(s)
# 1
len(s.notes)
# 0
# Test that removing from end elements works.
# 

s = stream.Measure()
s.append(meter.TimeSignature('4/4'))
s.repeatAppend(note.Note('C'), 4)
s.rightBarline = bar.Barline('final')
len(s)
# 6
s.removeByClass('Barline')
len(s)
# 5
# Stream.removeByNotOfClass(classFilterList)
# Remove all elements not of the specified class or subclass in the Steam in place.
# 

s = stream.Stream()
s.append(meter.TimeSignature('4/4'))
s.repeatAppend(note.Note('C'), 8)
len(s)
# 9
s.removeByNotOfClass('TimeSignature')
len(s)
# 1
len(s.notes)
# 0
# Stream.repeatAppend(item, numberOfTimes)
# Given an object and a number, run append that many times on a deepcopy of the object. numberOfTimes should of course be a positive integer.
# 

a = stream.Stream()
n = note.Note('D--')
n.duration.type = 'whole'
a.repeatAppend(n, 10)
a.show('text')
# {0.0} <music21.note.Note D-->
# {4.0} <music21.note.Note D-->
# {8.0} <music21.note.Note D-->
# {12.0} <music21.note.Note D-->
# ...
# {36.0} <music21.note.Note D-->

a.duration.quarterLength
# 40.0
a[9].offset
# 36.0
# Stream.repeatInsert(item, offsets)
# Given an object, create a deep copy of each object at each positions specified by the offset list:
# 

a = stream.Stream()
n = note.Note('G-')
n.quarterLength = 1

a.repeatInsert(n, [0, 2, 3, 4, 4.5, 5, 6, 7, 8, 9, 10, 11, 12])
len(a)
# 13
a[10].offset
# 10.0
# Stream.replace(target: music21.base.Music21Object, replacement: music21.base.Music21Object, *, recurse: bool = False, allDerived: bool = True) → None
# Given a target object, replace it with the supplied replacement object.
# 
# Does nothing if target cannot be found.
# 
# If allDerived is True (as it is by default), all sites (stream) that this this stream derives from and also have a reference for the replacement will be similarly changed. This is useful for altering both a flat and nested representation.
# 

cSharp = note.Note('C#4')
s = stream.Stream()
s.insert(0, cSharp)
dFlat = note.Note('D-4')
s.replace(cSharp, dFlat)
s.show('t')
# {0.0} <music21.note.Note D->
# If allDerived is True then all streams that this stream comes from get changed (but not non-derived streams)
# 

otherStream = stream.Stream()
otherStream.insert(0, dFlat)
f = note.Note('F4')
sf = s.flat
sf is not s
# True
sf.replace(dFlat, f, allDerived=True)
sf[0] is f
# True
s[0] is f
# True
otherStream[0] is dFlat
# True
# Note that it does not work the other way: if we made the replacement on s then sf, the flattened representation, would not be changed, since s does not derive from sf but vice-versa.
# 
# With recurse=True, a stream can replace an element that is further down in the hierarchy. First let’s set up a nested score:
# 

s = stream.Score()
p = stream.Part(id='part1')
s.append(p)
m = stream.Measure()
p.append(m)
cSharp = note.Note('C#4')
m.append(cSharp)
s.show('text')
# {0.0} <music21.stream.Part part1>
    # {0.0} <music21.stream.Measure 0 offset=0.0>
        # {0.0} <music21.note.Note C#>
# Now make a deep-nested replacement
# 

dFlat = note.Note('D-4')
s.replace(cSharp, dFlat, recurse=True)
s.show('text')
# {0.0} <music21.stream.Part part1>
    # {0.0} <music21.stream.Measure 0 offset=0.0>
        # {0.0} <music21.note.Note D->
# Changed by v.5:
# 
# allTargetSites RENAMED to allDerived – only searches in derivation chain.
# 
# Changed in v5.3 – firstMatchOnly removed – impossible to have element in stream twice. recurse and shiftOffsets changed to keywordOnly arguments
# 
# Changed in v6 – recurse works
# 
# Stream.restoreActiveSites()
# Restore all active sites for all elements from this Stream downward.
# 
# Stream.scaleDurations(amountToScale, *, inPlace=False)
# Scale all durations by a provided scalar. Offsets are not modified.
# 
# To augment or diminish a Stream, see the augmentOrDiminish() method.
# 
# We do not retain durations in any circumstance; if inPlace=True, two deepcopies are done which can be quite slow.
# 
# Stream.scaleOffsets(amountToScale, *, anchorZero='lowest', anchorZeroRecurse=None, inPlace=False)
# Scale all offsets by a multiplication factor given in amountToScale. Durations are not altered.
# 
# To augment or diminish a Stream, see the augmentOrDiminish() method.
# 
# The anchorZero parameter determines if and/or where the zero offset is established for the set of offsets in this Stream before processing. Offsets are shifted to make either the lower or upper values the new zero; then offsets are scaled; then the shifts are removed. Accepted values are None (no offset shifting), “lowest”, or “highest”.
# 
# The anchorZeroRecurse parameter determines the anchorZero for all embedded Streams, and Streams embedded within those Streams. If the lowest offset in an embedded Stream is non-zero, setting this value to None will a the space between the start of that Stream and the first element to be scaled. If the lowest offset in an embedded Stream is non-zero, setting this value to ‘lowest’ will not alter the space between the start of that Stream and the first element to be scaled.
# 
# To shift all the elements in a Stream, see the shiftElements() method.
# 
# Changed in v.5 – inPlace is default False, and anchorZero, anchorZeroRecurse and inPlace are keyword only arguments.
# 
# Stream.setDerivationMethod(derivationMethod, recurse=False)
# Sets the .derivation.method for each element in the Stream if it has a .derivation object.
# 

import copy
s = converter.parse('tinyNotation: 2/4 c2 d e f')
s2 = copy.deepcopy(s)
s2.recurse().notes[-1].derivation
# <Derivation of <music21.note.Note F> from <music21.note.Note F> via '__deepcopy__'>
s2.setDerivationMethod('exampleCopy', recurse=True)
s2.recurse().notes[-1].derivation
# <Derivation of <music21.note.Note F> from <music21.note.Note F> via 'exampleCopy'>
# Without recurse:
# 

s = converter.parse('tinyNotation: 2/4 c2 d e f')
s2 = copy.deepcopy(s)
s2.setDerivationMethod('exampleCopy')
s2.recurse().notes[-1].derivation
# <Derivation of <music21.note.Note F> from <music21.note.Note F> via '__deepcopy__'>
# Stream.setElementOffset(element, offset, *, addElement=False, setActiveSite=True)
# Sets the Offset for an element, very quickly.
# 

s = stream.Stream()
s.id = 'Stream1'
n = note.Note('B-4')
s.insert(10, n)
n.offset
# 10.0
s.setElementOffset(n, 20.0)
n.offset
# 20.0
n.getOffsetBySite(s)
# 20.0
# If the element is not in the Stream, raises a StreamException:
# 

n2 = note.Note('D')
s.setElementOffset(n2, 30.0)
# Traceback (most recent call last):
# music21.exceptions21.StreamException: Cannot set the offset for element
    # <music21.note.Note D>, not in Stream <music21.stream.Stream Stream1>.
# …unless addElement is explicitly set to True (this is a core function that should NOT be used in normal situations. it is used by .insert() and .append() and other core functions; other things must also be done to properly add an element, such as append sites.)
# 

n2 = note.Note('D')
s.setElementOffset(n2, 30.0, addElement=True)
# Changed in v5.5 – also sets .activeSite for the element unless setActiveSite is False
# 
# Stream.shiftElements(offset, startOffset=None, endOffset=None, classFilterList=None)
# Add the given offset value to every offset of the objects found in the Stream. Objects that are specifically placed at the end of the Stream via .storeAtEnd() (such as right barlines) are not affected.
# 
# If startOffset is given then all elements before that offset will be shifted. If endOffset is given then all elements at or after this offset will be shifted
# 

a = stream.Stream()
a.repeatInsert(note.Note('C'), list(range(10)))
a.shiftElements(30)
a.lowestOffset
# 30.0
a.shiftElements(-10)
a.lowestOffset
# 20.0
# Use shiftElements to move elements after a change in duration:
# 

st2 = stream.Stream()
st2.insert(0, note.Note('D4', type='whole'))
st2.repeatInsert(note.Note('C4'), list(range(4, 8)))
st2.show('text')
# {0.0} <music21.note.Note D>
# {4.0} <music21.note.Note C>
# {5.0} <music21.note.Note C>
# {6.0} <music21.note.Note C>
# {7.0} <music21.note.Note C>
# Now make the first note a dotted whole note and shift the rest by two quarters…
# 

firstNote = st2[0]
firstNoteOldQL = firstNote.quarterLength
firstNote.duration.dots = 1
firstNoteNewQL = firstNote.quarterLength
shiftAmount = firstNoteNewQL - firstNoteOldQL
shiftAmount
# 2.0

st2.shiftElements(shiftAmount, startOffset=4.0)
st2.show('text')
# {0.0} <music21.note.Note D>
# {6.0} <music21.note.Note C>
# {7.0} <music21.note.Note C>
# {8.0} <music21.note.Note C>
# {9.0} <music21.note.Note C>
# A class filter list may be given. It must be an iterable.
# 

st2.insert(7.5, key.Key('F'))
st2.shiftElements(2/3, startOffset=6.0, endOffset=8.0,
# ...                   classFilterList=[note.Note])
st2.show('text')
# {0.0} <music21.note.Note D>
# {6.6667} <music21.note.Note C>
# {7.5} <music21.key.Key of F major>
# {7.6667} <music21.note.Note C>
# {8.0} <music21.note.Note C>
# {9.0} <music21.note.Note C>
# Stream.show(*args, **kwargs)
# Displays an object in a format provided by the fmt argument or, if not provided, the format set in the user’s Environment
# 
# Valid formats include (but are not limited to)::
# musicxml text midi lily (or lilypond) lily.png lily.pdf lily.svg braille vexflow musicxml.png
# 
# N.B. score.write(‘lily’) returns a bare lilypond file, score.show(‘lily’) runs it through lilypond and displays it as a png.
# 
# Stream.showVariantAsOssialikePart(containedPart, variantGroups, *, inPlace=False)
# Takes a part within the score and a list of variant groups within that part. Puts the variant object in a part surrounded by hidden rests to mimic the appearance of an ossia despite limited musicXML support for ossia staves. Note that this will ignore variants with .lengthType ‘elongation’ and ‘deletion’ as there is no good way to represent ossia staves like those by this method.
# 

sPartStr = 'd4 e4 f4 g4   a2 b-4 a4    g4 a8 g8 f4 e4    d2 a2 '
v1Str =    '              a2. b-8 a8 '
v2Str =    '                                             d4 f4 a2 '

sPartStr += "d4 e4 f4 g4    a2 b-4 a4    g4 a8 b-8 c'4 c4    f1"

sPartStream = converter.parse('tinynotation: 4/4 ' + sPartStr)
sPartStream.makeMeasures(inPlace=True)  # maybe not necessary?
v1stream = converter.parse('tinynotation: 4/4 ' + v1Str)
v2stream = converter.parse('tinynotation: 4/4 ' + v2Str)

v1 = variant.Variant()
v1measure = stream.Measure()
v1.insert(0.0, v1measure)
for e in v1stream.notesAndRests:
# ...    v1measure.insert(e.offset, e)

v2 = variant.Variant()
v2measure = stream.Measure()
v2.insert(0.0, v2measure)
for e in v2stream.notesAndRests:
# ...    v2measure.insert(e.offset, e)

v3 = variant.Variant()
v2.replacementDuration = 4.0
v3.replacementDuration = 4.0
v1.groups = ['variant1']
v2.groups = ['variant2']
v3.groups = ['variant3']

sPart = stream.Part()
for e in sPartStream:
# ...    sPart.insert(e.offset, e)

sPart.insert(4.0, v1)
sPart.insert(12.0, v2)
sPart.insert(20.0, v3)  # This is a deletion variant and will be skipped
s = stream.Score()
s.insert(0.0, sPart)
streamWithOssia = s.showVariantAsOssialikePart(sPart,
# ...          ['variant1', 'variant2', 'variant3'], inPlace=False)
streamWithOssia.show()
# Stream.simultaneousAttacks(stream2)
# returns an ordered list of offsets where elements are started (attacked) at the same time in both self and stream2.
# 
# In this example, we create one stream of Qtr, Half, Qtr, and one of Half, Qtr, Qtr. There are simultaneous attacks at offset 0.0 (the beginning) and at offset 3.0, but not at 1.0 or 2.0:
# 

st1 = stream.Stream()
st2 = stream.Stream()
st1.append([note.Note(type='quarter'),
# ...             note.Note(type='half'),
# ...             note.Note(type='quarter')])
st2.append([note.Note(type='half'),
# ...             note.Note(type='quarter'),
# ...             note.Note(type='quarter')])
print(st1.simultaneousAttacks(st2))
# [0.0, 3.0]
# Stream.sliceAtOffsets(offsetList, target=None, addTies=True, inPlace=False, displayTiedAccidentals=False)
# Given a list of quarter lengths, slice and optionally tie all Music21Objects crossing these points.
# 

s = stream.Stream()
n = note.Note()
n.duration.type = 'whole'
s.append(n)
post = s.sliceAtOffsets([1, 2, 3], inPlace=True)
[(e.offset, e.quarterLength) for e in s]
# [(0.0, 1.0), (1.0, 1.0), (2.0, 1.0), (3.0, 1.0)]
# Stream.sliceByBeat(target=None, addTies=True, inPlace=False, displayTiedAccidentals=False)
# Slice all elements in the Stream that have a Duration at the offsets determined to be the beat from the local TimeSignature.
# 
# TODO: return None if inPlace is True
# 
# Stream.sliceByGreatestDivisor(*, addTies=True, inPlace=False)
# Slice all Duration objects on all Notes and Rests of this Stream. Duration are sliced according to the approximate GCD found in all durations.
# 
# Stream.sliceByQuarterLengths(quarterLengthList, *, target=None, addTies=True, inPlace=False)
# Slice all Duration objects on all Notes and Rests of this Stream. Duration are sliced according to values provided in quarterLengthList list. If the sum of these values is less than the Duration, the values are accumulated in a loop to try to fill the Duration. If a match cannot be found, an Exception is raised.
# 
# If target is None, the entire Stream is processed. Otherwise, only the element specified is manipulated.
# 
# Stream.sort(force=False)
# Sort this Stream in place by offset, then priority, then standard class sort order (e.g., Clefs before KeySignatures before TimeSignatures).
# 
# Note that Streams automatically sort themselves unless autoSort is set to False (as in the example below)
# 
# If force is True, a sort will be attempted regardless of any other parameters.
# 

n1 = note.Note('a')
n2 = note.Note('b')
s = stream.Stream()
s.autoSort = False
s.insert(100, n2)
s.insert(0, n1)  # now a has a lower offset by higher index
[n.name for n in s]
# ['B', 'A']
s.sort()
[n.name for n in s]
# ['A', 'B']
# Stream.splitAtQuarterLength(quarterLength, retainOrigin=True, addTies=True, displayTiedAccidentals=False, searchContext=True)
# This method overrides the method on Music21Object to provide similar functionality for Streams.
# 
# Most arguments are passed to Music21Object.splitAtQuarterLength.
# 
# Stream.splitByClass(classObj, fx)
# Given a stream, get all objects of type classObj and divide them into two new streams depending on the results of fx. Fx should be a lambda or other function on elements. All elements where fx returns True go in the first stream. All other elements are put in the second stream.
# 
# If classObj is None then all elements are returned. ClassObj can also be a list of classes.
# 
# In this example, we will create 50 notes from midi note 30 (two octaves and a tritone below middle C) to midi note 80 (an octave and a minor sixth above middle C) and add them to a Stream. We then create a lambda function to split between those notes below middle C (midi note 60) and those above (google “lambda functions in Python” for more information on what these powerful tools are).
# 

stream1 = stream.Stream()
for x in range(30, 81):
# ...     n = note.Note()
# ...     n.pitch.midi = x
# ...     stream1.append(n)
fx = lambda n: n.pitch.midi < 60
b, c = stream1.splitByClass(note.Note, fx)
# Stream b now contains all the notes below middle C, that is, 30 notes, beginning with F#1 and ending with B3 while Stream c has the 21 notes from C4 to A-5:
# 

len(b)
# 30
(b[0].nameWithOctave, b[-1].nameWithOctave)
# ('F#1', 'B3')
len(c)
# 21
(c[0].nameWithOctave, c[-1].nameWithOctave)
# ('C4', 'G#5')
# Stream.storeAtEnd(itemOrList, ignoreSort=False)
# Inserts an item or items at the end of the Stream, stored in the special box (called _endElements).
# 
# This method is useful for putting things such as right bar lines or courtesy clefs that should always be at the end of a Stream no matter what else is appended to it
# 
# As sorting is done only by priority and class, it cannot avoid setting isSorted to False.
# 

s = stream.Stream()
b = bar.Repeat()
s.storeAtEnd(b)
b in s
# True
s.elementOffset(b)
# 0.0
s.elementOffset(b, stringReturns=True)
# 'highestTime'
# Only elements of zero duration can be stored. Otherwise a StreamException is raised.
# 
# Stream.stripTies(inPlace=False, matchByPitch=False, retainContainers=False)
# Find all notes that are tied; remove all tied notes, then make the first of the tied notes have a duration equal to that of all tied constituents. Lastly, remove the formerly-tied notes.
# 
# This method can be used on Stream and Stream subclasses. When used on a Score, Parts and Measures are retained.
# 
# If retainContainers is False (by default), this method only returns Note objects; Measures and other structures are stripped from the Stream. Set retainContainers to True to remove ties from a Part Stream that contains Measure Streams, and get back a multi-Measure structure.
# 
# Presently, this only works if tied notes are sequential; ultimately this will need to look at .to and .from attributes (if they exist)
# 
# In some cases (under makeMeasures()) a continuation note will not have a Tie object with a stop attribute set. In that case, we need to look for sequential notes with matching pitches. The matchByPitch option can be used to use this technique.
# 
# Note that inPlace=True on a Stream with substreams currently has buggy behavior. Use inPlace=False for now.
# 
# TODO: Fix this.
# 

a = stream.Stream()
n = note.Note()
n.quarterLength = 6
a.append(n)
m = a.makeMeasures()
m.makeTies(inPlace=True)
len(m.flat.notes)
# 2

m = m.stripTies()
len(m.flat.notes)
# 1
# Stream.template(fillWithRests=True, removeClasses=None, retainVoices=True)
# Return a new Stream based on this one, but without the notes and other elements but keeping instruments, clefs, keys, etc.
# 
# Classes to remove are specified in removeClasses.
# 
# If this Stream contains measures, return a new Stream with new Measures populated with the same characteristics of those found in this Stream.
# 

b = corpus.parse('bwv66.6')
sopr = b.parts[0]
soprEmpty = sopr.template()
soprEmpty.show('text')
# {0.0} <music21.instrument.Instrument 'P1: Soprano: Instrument 1'>
# {0.0} <music21.stream.Measure 0 offset=0.0>
    # {0.0} <music21.clef.TrebleClef>
    # {0.0} <music21.key.Key of f# minor>
    # {0.0} <music21.meter.TimeSignature 4/4>
    # {0.0} <music21.note.Rest rest>
# {1.0} <music21.stream.Measure 1 offset=1.0>
    # {0.0} <music21.note.Rest rest>
# {5.0} <music21.stream.Measure 2 offset=5.0>
    # {0.0} <music21.note.Rest rest>
# {9.0} <music21.stream.Measure 3 offset=9.0>
    # {0.0} <music21.layout.SystemLayout>
    # {0.0} <music21.note.Rest rest>
# {13.0} <music21.stream.Measure 4 offset=13.0>
# ...
# Really make empty with fillWithRests=False
# 

alto = b.parts[1]
altoEmpty = alto.template(fillWithRests=False)
altoEmpty.show('text')
# {0.0} <music21.instrument.Instrument 'P2: Alto: Instrument 2'>
# {0.0} <music21.stream.Measure 0 offset=0.0>
    # {0.0} <music21.clef.TrebleClef>
    # {0.0} <music21.key.Key of f# minor>
    # {0.0} <music21.meter.TimeSignature 4/4>
# {1.0} <music21.stream.Measure 1 offset=1.0>
# <BLANKLINE>
# {5.0} <music21.stream.Measure 2 offset=5.0>
# <BLANKLINE>
# {9.0} <music21.stream.Measure 3 offset=9.0>
    # {0.0} <music21.layout.SystemLayout>
# ...
# removeClasses can be a list or set of classes to remove. By default it is [‘GeneralNote’, ‘Dynamic’, ‘Expression’]
# 

tenor = b.parts[2]
tenorNoClefsSignatures = tenor.template(fillWithRests=False,
# ...       removeClasses=['Clef', 'KeySignature', 'TimeSignature', 'Instrument'])
tenorNoClefsSignatures.show('text')
# {0.0} <music21.stream.Measure 0 offset=0.0>
    # {0.0} <music21.note.Note A>
    # {0.5} <music21.note.Note B>
# {1.0} <music21.stream.Measure 1 offset=1.0>
    # {0.0} <music21.note.Note C#>
    # {1.0} <music21.note.Note B>
    # {2.0} <music21.note.Note A>
    # {3.0} <music21.note.Note B>
# {5.0} <music21.stream.Measure 2 offset=5.0>
# ...
# Setting removeClasses to True removes everything that is not a Stream:
# 

bass = b.parts[3]
bassEmpty = bass.template(fillWithRests=False, removeClasses=True)
bassEmpty.show('text')
# {0.0} <music21.stream.Measure 0 offset=0.0>
# <BLANKLINE>
# {1.0} <music21.stream.Measure 1 offset=1.0>
# <BLANKLINE>
# {5.0} <music21.stream.Measure 2 offset=5.0>
# <BLANKLINE>
# {9.0} <music21.stream.Measure 3 offset=9.0>
# <BLANKLINE>
# {13.0} <music21.stream.Measure 4 offset=13.0>
# <BLANKLINE>
# ...
# On the whole score:
# 

b.template().show('text')
# {0.0} <music21.metadata.Metadata object at 0x106151940>
# {0.0} <music21.stream.Part Soprano>
    # {0.0} <music21.instrument.Instrument 'P1: Soprano: Instrument 1'>
    # {0.0} <music21.stream.Measure 0 offset=0.0>
        # {0.0} <music21.clef.TrebleClef>
        # {0.0} <music21.key.Key of f# minor>
        # {0.0} <music21.meter.TimeSignature 4/4>
        # {0.0} <music21.note.Rest rest>
    # {1.0} <music21.stream.Measure 1 offset=1.0>
        # {0.0} <music21.note.Rest rest>
        # ...
    # {33.0} <music21.stream.Measure 9 offset=33.0>
        # {0.0} <music21.note.Rest rest>
        # {3.0} <music21.bar.Barline type=final>
# {0.0} <music21.stream.Part Alto>
    # {0.0} <music21.instrument.Instrument 'P2: Alto: Instrument 2'>
    # {0.0} <music21.stream.Measure 0 offset=0.0>
        # {0.0} <music21.clef.TrebleClef>
        # {0.0} <music21.key.Key of f# minor>
        # {0.0} <music21.meter.TimeSignature 4/4>
        # {0.0} <music21.note.Rest rest>
    # {1.0} <music21.stream.Measure 1 offset=1.0>
        # {0.0} <music21.note.Rest rest>
    # ...
    # {33.0} <music21.stream.Measure 9 offset=33.0>
        # {0.0} <music21.note.Rest rest>
        # {3.0} <music21.bar.Barline type=final>
# {0.0} <music21.layout.StaffGroup ...>
# If retainVoices is False (default True) then Voice streams are treated differently from all other Streams and are removed. All elements in the voice are removed even if they do not match the classList:
# 

p = stream.Part(id='part0')
m1 = stream.Measure(number=1)
v1 = stream.Voice(id='voice1')
v1.insert(0, note.Note('E', quarterLength=4.0))
v2 = stream.Voice(id='voice2')
v2.insert(0, note.Note('G', quarterLength=2.0))
m1.insert(0, v1)
m1.insert(0, v2)
m2 = stream.Measure(number=2)
m2.insert(0, note.Note('D', quarterLength=4.0))
p.append([m1, m2])
pt = p.template(retainVoices=False)
pt.show('text')
# {0.0} <music21.stream.Measure 1 offset=0.0>
    # {0.0} <music21.note.Rest rest>
# {4.0} <music21.stream.Measure 2 offset=4.0>
    # {0.0} <music21.note.Rest rest>
pt[0][0].quarterLength
# 4.0
# Developer note – if you just want a copy of a Score with new Part and Measure objects, but you don’t care that the notes, etc. inside are the same objects as the original (i.e., you do not plan to manipulate them, or you want the manipulations to return to the original objects), using .template() is several times faster than a deepcopy of the stream (about 4x faster on bwv66.6)
# 
# Stream.toSoundingPitch(*, inPlace=False)
# If not at sounding pitch, transpose all Pitch elements to sounding pitch. The atSoundingPitch property is used to determine if transposition is necessary.
# 
# Affected by the presence of Instruments and by Ottava spanners
# 
# v2.0.10 changes – inPlace is False; v. 5 returns None if inPlace=True
# 

sc = stream.Score()
p = stream.Part(id='barisax')
p.append(instrument.BaritoneSaxophone())
m = stream.Measure(number=1)
m.append(note.Note('A4'))
p.append(m)
sc.append(p)
sc.atSoundingPitch = False

scSounding = sc.toSoundingPitch()
scSounding.show('text')
# {0.0} <music21.stream.Part barisax>
    # {0.0} <music21.instrument.BaritoneSaxophone 'Baritone Saxophone'>
    # {0.0} <music21.stream.Measure 1 offset=0.0>
        # {0.0} <music21.note.Note C>

scSounding.atSoundingPitch
# True
scSounding.parts[0].atSoundingPitch
# True
scSounding.recurse().notes[0].nameWithOctave
# 'C3'
# Stream.toWrittenPitch(*, inPlace=False)
# If not at written pitch, transpose all Pitch elements to written pitch. The atSoundingPitch property is used to determine if transposition is necessary.
# 
# music21 v.3 changes – inPlace=False, v. 5 – returns None if inPlace=True
# 

sc = stream.Score()
p = stream.Part(id='baritoneSax')
p.append(instrument.BaritoneSaxophone())
m = stream.Measure(number=1)
m.append(note.Note('C3'))
p.append(m)
sc.append(p)
sc.atSoundingPitch = True
scWritten = sc.toWrittenPitch()
scWritten.show('text')
# {0.0} <music21.stream.Part baritoneSax>
    # {0.0} <music21.instrument.BaritoneSaxophone 'Baritone Saxophone'>
    # {0.0} <music21.stream.Measure 1 offset=0.0>
        # {0.0} <music21.note.Note A>
scWritten.atSoundingPitch
# False
scWritten.parts[0].atSoundingPitch
# False
scWritten.recurse().notes[0].nameWithOctave
# 'A4'
# Stream.transferOffsetToElements()
# Transfer the offset of this stream to all internal elements; then set the offset of this stream to zero.
# 

a = stream.Stream()
a.repeatInsert(note.Note('C'), list(range(10)))
a.offset = 30
a.transferOffsetToElements()
a.lowestOffset
# 30.0
a.offset
# 0.0
a.offset = 20
a.transferOffsetToElements()
a.lowestOffset
# 50.0
# Stream.transpose(value, inPlace=False, recurse=True, classFilterList=None)
# Transpose all specified classes in the Stream by the user-provided value. If the value is an integer, the transposition is treated in half steps. If the value is a string, any Interval string specification can be provided.
# 
# returns a new Stream by default, but if the optional “inPlace” key is set to True then it modifies pitches in place.
# 
# TODO: for generic interval set accidental by key signature.
# 

aInterval = interval.Interval('d5')

aStream = corpus.parse('bach/bwv324.xml')
part = aStream.parts[0]
[str(p) for p in aStream.parts[0].pitches[:10]]
# ['B4', 'D5', 'B4', 'B4', 'B4', 'B4', 'C5', 'B4', 'A4', 'A4']

bStream = aStream.parts[0].flat.transpose('d5')
[str(p) for p in bStream.pitches[:10]]
# ['F5', 'A-5', 'F5', 'F5', 'F5', 'F5', 'G-5', 'F5', 'E-5', 'E-5']
# Test that aStream hasn’t been changed:
# 

[str(p) for p in aStream.parts[0].pitches[:10]]
# ['B4', 'D5', 'B4', 'B4', 'B4', 'B4', 'C5', 'B4', 'A4', 'A4']

cStream = bStream.flat.transpose('a4')
[str(p) for p in cStream.pitches[:10]]
# ['B5', 'D6', 'B5', 'B5', 'B5', 'B5', 'C6', 'B5', 'A5', 'A5']

cStream.flat.transpose(aInterval, inPlace=True)
[str(p) for p in cStream.pitches[:10]]
# ['F6', 'A-6', 'F6', 'F6', 'F6', 'F6', 'G-6', 'F6', 'E-6', 'E-6']
# Stream.voicesToParts(*, separateById=False)
# If this Stream defines one or more voices, extract each into a Part, returning a Score.
# 
# If this Stream has no voices, return the Stream as a Part within a Score.
# 

c = corpus.parse('demos/two-voices')
c.show('t')
# {0.0} <music21.text.TextBox 'Music21 Fr...'>
# {0.0} <music21.text.TextBox 'Music21'>
# {0.0} <music21.metadata.Metadata object at 0x109ce1630>
# {0.0} <music21.stream.Part Piano>
    # {0.0} <music21.instrument.Instrument 'P1: Piano: '>
    # {0.0} <music21.stream.Measure 1 offset=0.0>
        # {0.0} <music21.layout.PageLayout>
        # {0.0} <music21.layout.SystemLayout>
        # ...
        # {0.0} <music21.clef.BassClef>
        # {0.0} <music21.key.Key of D major>
        # {0.0} <music21.meter.TimeSignature 4/4>
        # {0.0} <music21.stream.Voice 3>
            # {0.0} <music21.note.Note E>
            # ...
            # {3.0} <music21.note.Rest rest>
        # {0.0} <music21.stream.Voice 4>
            # {0.0} <music21.note.Note F#>
            # ...
            # {3.5} <music21.note.Note B>
    # {4.0} <music21.stream.Measure 2 offset=4.0>
        # {0.0} <music21.stream.Voice 3>
            # {0.0} <music21.note.Note E>
            # ...
            # {3.0} <music21.note.Rest rest>
        # {0.0} <music21.stream.Voice 4>
            # {0.0} <music21.note.Note E>
            # ...
            # {3.5} <music21.note.Note A>
    # {8.0} <music21.stream.Measure 3 offset=8.0>
        # {0.0} <music21.note.Rest rest>
        # {4.0} <music21.bar.Barline type=final>
# {0.0} <music21.layout.ScoreLayout>

ce = c.voicesToParts()
ce.show('t')
# {0.0} <music21.stream.Part Piano-v0>
    # {0.0} <music21.stream.Measure 1 offset=0.0>
        # {0.0} <music21.clef.TrebleClef>
        # {0.0} <music21.key.Key of D major>
        # {0.0} <music21.meter.TimeSignature 4/4>
        # {0.0} <music21.note.Note E>
        # ...
        # {3.0} <music21.note.Rest rest>
    # {4.0} <music21.stream.Measure 2 offset=4.0>
        # {0.0} <music21.note.Note E>
        # ...
        # {3.0} <music21.note.Rest rest>
    # {8.0} <music21.stream.Measure 3 offset=8.0>
        # {0.0} <music21.note.Rest rest>
        # {4.0} <music21.bar.Barline type=final>
# {0.0} <music21.stream.Part Piano-v1>
    # {0.0} <music21.stream.Measure 1 offset=0.0>
        # {0.0} <music21.clef.BassClef>
        # {0.0} <music21.key.Key of D major>
        # ...
        # {3.5} <music21.note.Note B>
    # {4.0} <music21.stream.Measure 2 offset=4.0>
        # {0.0} <music21.note.Note E>
        # ...
        # {3.5} <music21.note.Note A>
    # {8.0} <music21.stream.Measure 3 offset=8.0>
# <BLANKLINE>
# If separateById is True then all voices with the same id will be connected to the same Part, regardless of order they appear in the measure.
# 
# Compare the previous output:
# 

p0pitches = ce.parts[0].pitches
p1pitches = ce.parts[1].pitches
' '.join([p.nameWithOctave for p in p0pitches])
# 'E4 D#4 D#4 E4 F#4 E4 B3 B3 E4 E4'
' '.join([p.nameWithOctave for p in p1pitches])
# 'F#2 F#3 E3 E2 D#2 D#3 B2 B3 E2 E3 D3 D2 C#2 C#3 A2 A3'
# Swap voice ids in first measure:
# 

m0 = c.parts[0].getElementsByClass('Measure')[0]
m0.voices[0].id, m0.voices[1].id
# ('3', '4')
m0.voices[0].id = '4'
m0.voices[1].id = '3'
# Now run voicesToParts with separateById=True
# 

ce = c.voicesToParts(separateById=True)
p0pitches = ce.parts[0].pitches
p1pitches = ce.parts[1].pitches
' '.join([p.nameWithOctave for p in p0pitches])
# 'E4 D#4 D#4 E4 F#4 E2 E3 D3 D2 C#2 C#3 A2 A3'
' '.join([p.nameWithOctave for p in p1pitches])
# 'F#2 F#3 E3 E2 D#2 D#3 B2 B3 E4 B3 B3 E4 E4'
# Note that the second and subsequent measure’s pitches were changed not the first, because separateById aligns the voices according to order first encountered, not by sorting the Ids.
# 
# Stream.write(*args, **kwargs)
# Write out a file of music notation (or an image, etc.) in a given format. If fp is specified as a file path then the file will be placed there. If it is not given then a temporary file will be created.
# 
# If fmt is not given then the default of your Environment’s ‘writeFormat’ will be used. For most people that is musicxml.
# 
# Returns the full path to the file.
# 
# Methods inherited from StreamCoreMixin:
# 
# asTimespans()
# 
# asTree()
# 
# coreAppend()
# 
# coreElementsChanged()
# 
# coreGatherMissingSpanners()
# 
# coreGetElementByMemoryLocation()
# 
# coreGuardBeforeAddElement()
# 
# coreHasElementByMemoryLocation()
# 
# coreInsert()
# 
# coreSelfActiveSite()
# 
# coreStoreAtEnd()
# 
# Methods inherited from Music21Object:
# 
# containerHierarchy()
# 
# contextSites()
# 
# getAllContextsByClass()
# 
# getContextByClass()
# 
# getOffsetBySite()
# 
# getOffsetInHierarchy()
# 
# getSpannerSites()
# 
# informSites()
# 
# next()
# 
# previous()
# 
# purgeLocations()
# 
# purgeOrphans()
# 
# setOffsetBySite()
# 
# sortTuple()
# 
# splitAtDurations()
# 
# splitByQuarterLengths()
# 
# Methods inherited from ProtoM21Object:
# 
# isClassOrSubclass()
# 
# Stream instance variables
# 
# Stream.autoSort
# Boolean describing whether the Stream is automatically sorted by offset whenever necessary.
# 
# Stream.definesExplicitPageBreaks
# Boolean that says whether all page breaks in the piece are explicitly defined. Only used on musicxml output (maps to the musicxml <supports attribute=”new-page”> tag) and only if this is the outermost Stream being shown
# 
# Stream.definesExplicitSystemBreaks
# Boolean that says whether all system breaks in the piece are explicitly defined. Only used on musicxml output (maps to the musicxml <supports attribute=”new-system”> tag) and only if this is the outermost Stream being shown
# 
# Stream.isFlat
# Boolean describing whether this Stream contains embedded sub-Streams or Stream subclasses (not flat).
# 
# Stream.isSorted
# Boolean describing whether the Stream is sorted or not.
# 
# Stream.recursionType
# Class variable:
# 
# String of (‘elementsFirst’ (default), ‘flatten’, ‘elementsOnly) that decides whether the stream likely holds relevant contexts for the elements in it.
# 
# Define this for a stream class, not an individual object.
# 
# see contextSites()
# 
# Instance variables inherited from Music21Object:
# 
# classSortOrder
# 
# groups
# 
# id
# 
# isStream
# 
# Measure
# class music21.stream.Measure(*args, **keywords)
# A representation of a Measure organized as a Stream.
# 
# All properties of a Measure that are Music21 objects are found as part of the Stream’s elements.
# 
# Measure number can be explicitly set with the number keyword:
# 

m4 = stream.Measure(number=4)
m4
# <music21.stream.Measure 4 offset=0.0>
m4.number
# 4
# If passed a single integer as an argument, assumes that this int is the measure number.
# 

m5 = stream.Measure(5)
m5
# <music21.stream.Measure 5 offset=0.0>
# Number can also be a string if there is a suffix:
# 

m4 = stream.Measure(number='4a')
m4
# <music21.stream.Measure 4a offset=0.0>
m4.numberSuffix
# 'a'
# Though they have all the features of general streams, Measures have specific attributes that allow for setting their number and numberSuffix, keep track of whether they have a different clef or key or timeSignature than previous measures, allow for padding (and pickups), and can be found as a “measure slice” within a score and parts.
# 
# Measure bases
# 
# Stream
# 
# StreamCoreMixin
# 
# Music21Object
# 
# ProtoM21Object
# 
# Measure read-only properties
# 
# Measure.barDuration
# Return the bar duration, or the Duration specified by the TimeSignature, regardless of what elements are found in this Measure or the highest time. TimeSignature is found first within the Measure, or within a context based search.
# 
# To get the duration of the total length of elements, just use the .duration property.
# 
# Here we create a 3/4 measure and “over-stuff” it with five quarter notes. barDuration still gives a duration of 3.0, or a dotted quarter note, while .duration gives a whole note tied to a quarter.
# 

m = stream.Measure()
m.timeSignature = meter.TimeSignature('3/4')
m.barDuration
# <music21.duration.Duration 3.0>
m.repeatAppend(note.Note(type='quarter'), 5)
m.barDuration
# <music21.duration.Duration 3.0>
m.duration
# <music21.duration.Duration 5.0>
# The objects returned by barDuration and duration are full Duration objects, will all the relevant properties:
# 

m.barDuration.fullName
# 'Dotted Half'
m.duration.fullName
# 'Whole tied to Quarter (5 total QL)'
# Read-only properties inherited from Stream:
# 
# beat
# 
# beatDuration
# 
# beatStr
# 
# beatStrength
# 
# flat
# 
# highestOffset
# 
# highestTime
# 
# isGapless
# 
# iter
# 
# lowestOffset
# 
# notes
# 
# notesAndRests
# 
# pitches
# 
# secondsMap
# 
# semiFlat
# 
# sorted
# 
# spanners
# 
# variants
# 
# voices
# 
# Read-only properties inherited from StreamCoreMixin:
# 
# spannerBundle
# 
# Read-only properties inherited from Music21Object:
# 
# hasEditorialInformation
# 
# hasStyleInformation
# 
# measureNumber
# 
# Read-only properties inherited from ProtoM21Object:
# 
# classSet
# 
# classes
# 
# Measure read/write properties
# 
# Measure.leftBarline
# Get or set the left barline, or the Barline object found at offset zero of the Measure. Can be set either with a string representing barline style or a bar.Barline() object or None. Note that not all bars have barline objects here – regular barlines don’t need them.
# 
# Measure.rightBarline
# Get or set the right barline, or the Barline object found at the offset equal to the bar duration.
# 

b = bar.Barline('final')
m = stream.Measure()
print(m.rightBarline)
# None
m.rightBarline = b
m.rightBarline.type
# 'final'
# A string can also be used instead:
# 

c = converter.parse('tinynotation: 3/8 C8 D E F G A B4.')
c.measure(1).rightBarline = 'light-light'
c.measure(3).rightBarline = 'light-heavy'
c.show()
# ../_images/stream_barline_demo.png
# Read/write properties inherited from Stream:
# 
# atSoundingPitch
# 
# clef
# 
# duration
# 
# elements
# 
# finalBarline
# 
# keySignature
# 
# metadata
# 
# seconds
# 
# timeSignature
# 
# Read/write properties inherited from Music21Object:
# 
# activeSite
# 
# derivation
# 
# editorial
# 
# offset
# 
# priority
# 
# quarterLength
# 
# style
# 
# Measure methods
# 
# Measure.barDurationProportion(barDuration=None)
# Return a floating point value greater than 0 showing the proportion of the bar duration that is filled based on the highest time of all elements. 0.0 is empty, 1.0 is filled; 1.5 specifies of an overflow of half.
# 
# Bar duration refers to the duration of the Measure as suggested by the TimeSignature. This value cannot be determined without a TimeSignature.
# 
# An already-obtained Duration object can be supplied with the barDuration optional argument.
# 

import copy
m = stream.Measure()
m.timeSignature = meter.TimeSignature('3/4')
n = note.Note()
n.quarterLength = 1
m.append(copy.deepcopy(n))
m.barDurationProportion()
# Fraction(1, 3)
m.append(copy.deepcopy(n))
m.barDurationProportion()
# Fraction(2, 3)
m.append(copy.deepcopy(n))
m.barDurationProportion()
# 1.0
m.append(copy.deepcopy(n))
m.barDurationProportion()
# Fraction(4, 3)
# Measure.bestTimeSignature()
# Given a Measure with elements in it, get a TimeSignature that contains all elements. Calls meter.bestTimeSignature(self)
# 
# Note: this does not yet accommodate triplets.
# 
# We create a simple stream that should be in 3/4
# 

s = converter.parse('C4 D4 E8 F8', format='tinyNotation', makeNotation=False)
m = stream.Measure()
for el in s:
# ...     m.insert(el.offset, el)
# But there is no TimeSignature!
# 

m.show('text')
# {0.0} <music21.note.Note C>
# {1.0} <music21.note.Note D>
# {2.0} <music21.note.Note E>
# {2.5} <music21.note.Note F>
# So, we get the best Time Signature and put it in the Stream.
# 

ts = m.bestTimeSignature()
ts
# <music21.meter.TimeSignature 3/4>
m.timeSignature = ts
m.show('text')
# {0.0} <music21.meter.TimeSignature 3/4>
# {0.0} <music21.note.Note C>
# {1.0} <music21.note.Note D>
# {2.0} <music21.note.Note E>
# {2.5} <music21.note.Note F>
# For further details about complex time signatures, etc. see meter.bestTimeSignature()
# 
# Measure.makeNotation(inPlace=False, **subroutineKeywords)
# This method calls a sequence of Stream methods on this Measure to prepare notation.
# 
# If inPlace is True, this is done in-place; if inPlace is False, this returns a modified deep copy.
# 

m = stream.Measure()
n1 = note.Note('g#')
n2 = note.Note('g')
m.append([n1, n2])
m.makeNotation(inPlace=True)
m.notes[1].pitch.accidental
# <accidental natural>
# Measure.measureNumberWithSuffix()
# Return the measure .number with the .numberSuffix as a string.
# 

m = stream.Measure()
m.number = 4
m.numberSuffix = 'A'
m.measureNumberWithSuffix()
# '4A'
# Test that it works as musicxml
# 

xml = musicxml.m21ToXml.GeneralObjectExporter().parse(m)
print(xml.decode('utf-8'))
# <?xml version="1.0"...?>
# ...
# <part id="...">
    # <!--========================= Measure 4 ==========================-->
    # <measure number="4A">
# ...
# Test round tripping:
# 

s2 = converter.parseData(xml)
print(s2.semiFlat.getElementsByClass('Measure')[0].measureNumberWithSuffix())
# 4A
# Note that we use print here because in parsing the data will become a unicode string.
# 
# Measure.mergeAttributes(other)
# Given another Measure, configure all non-element attributes of this Measure with the attributes of the other Measure. No elements will be changed or copied.
# 
# This method is necessary because Measures, unlike some Streams, have attributes independent of any stored elements.
# 
# Overrides base.Music21Object.mergeAttributes
# 

m1 = stream.Measure()
m1.id = 'MyMeasure'
m1.clefIsNew = True
m1.number = 2
m1.numberSuffix = 'b'
m1.layoutWidth = 200

m2 = stream.Measure()
m2.mergeAttributes(m1)
m2.layoutWidth
# 200
m2.id
# 'MyMeasure'
m2
# <music21.stream.Measure 2b offset=0.0>
# Try with not another Measure…
# 

m3 = stream.Stream()
m3.id = 'hello'
m2.mergeAttributes(m3)
m2.id
# 'hello'
m2.layoutWidth
# 200
# Measure.padAsAnacrusis(useGaps=True, useInitialRests=False)
# Given an incompletely filled Measure, adjust the paddingLeft value to to represent contained events as shifted to fill the right-most duration of the bar.
# 
# Calling this method will overwrite any previously set paddingLeft value, based on the current TimeSignature-derived barDuration attribute.
# 

m = stream.Measure()
m.timeSignature = meter.TimeSignature('3/4')
n = note.Note()
n.quarterLength = 1.0
m.append(n)
m.padAsAnacrusis()
m.paddingLeft
# 2.0

m.timeSignature = meter.TimeSignature('5/4')
m.padAsAnacrusis()
m.paddingLeft
# 4.0
# Empty space at the beginning of the measure will not be taken in account:
# 

m = stream.Measure()
m.timeSignature = meter.TimeSignature('3/4')
n = note.Note(type='quarter')
m.insert(2.0, n)
m.padAsAnacrusis()
m.paddingLeft
# 0
# If useInitialRests is True, then rests at the beginning of the measure are removed. This is especially useful for formats that don’t give a way to specify a pickup measure (such as tinynotation) or software that generates incorrect opening measures. So, to fix the problem before, put a rest at the beginning and call useInitialRests:
# 

r = note.Rest(type='half')
m.insert(0, r)
m.padAsAnacrusis(useInitialRests=True)
m.paddingLeft
# 2.0
# And the rest is gone!
# 

m.show('text')
# {0.0} <music21.meter.TimeSignature 3/4>
# {0.0} <music21.note.Note C>
# Only initial rests count for useInitialRests:
# 

m = stream.Measure()
m.timeSignature = meter.TimeSignature('3/4')
m.append(note.Rest(type='eighth'))
m.append(note.Rest(type='eighth'))
m.append(note.Note('C4', type='quarter'))
m.append(note.Rest(type='eighth'))
m.append(note.Note('D4', type='eighth'))
m.show('text')
# {0.0} <music21.meter.TimeSignature 3/4>
# {0.0} <music21.note.Rest rest>
# {0.5} <music21.note.Rest rest>
# {1.0} <music21.note.Note C>
# {2.0} <music21.note.Rest rest>
# {2.5} <music21.note.Note D>
m.padAsAnacrusis(useInitialRests=True)
m.paddingLeft
# 1.0
m.show('text')
# {0.0} <music21.meter.TimeSignature 3/4>
# {0.0} <music21.note.Note C>
# {1.0} <music21.note.Rest rest>
# {1.5} <music21.note.Note D>
# Methods inherited from Stream:
# 
# activateVariants()
# 
# addGroupForElements()
# 
# allPlayingWhileSounding()
# 
# analyze()
# 
# append()
# 
# attachIntervalsBetweenStreams()
# 
# attachMelodicIntervals()
# 
# augmentOrDiminish()
# 
# beatAndMeasureFromOffset()
# 
# chordify()
# 
# clear()
# 
# cloneEmpty()
# 
# containerInHierarchy()
# 
# elementOffset()
# 
# expandRepeats()
# 
# explode()
# 
# extendDuration()
# 
# extendDurationAndGetBoundaries()
# 
# extendTies()
# 
# extractContext()
# 
# findConsecutiveNotes()
# 
# findGaps()
# 
# flattenUnnecessaryVoices()
# 
# getClefs()
# 
# getElementAfterElement()
# 
# getElementAtOrBefore()
# 
# getElementBeforeOffset()
# 
# getElementById()
# 
# getElementsByClass()
# 
# getElementsByGroup()
# 
# getElementsByOffset()
# 
# getElementsNotOfClass()
# 
# getInstrument()
# 
# getInstruments()
# 
# getKeySignatures()
# 
# getOverlaps()
# 
# getTimeSignatures()
# 
# hasElement()
# 
# hasElementOfClass()
# 
# hasMeasures()
# 
# hasPartLikeStreams()
# 
# hasVoices()
# 
# haveAccidentalsBeenMade()
# 
# index()
# 
# insert()
# 
# insertAndShift()
# 
# insertIntoNoteOrChord()
# 
# invertDiatonic()
# 
# isSequence()
# 
# isTwelveTone()
# 
# isWellFormedNotation()
# 
# lyrics()
# 
# makeAccidentals()
# 
# makeBeams()
# 
# makeChords()
# 
# makeImmutable()
# 
# makeMeasures()
# 
# makeMutable()
# 
# makeRests()
# 
# makeTies()
# 
# makeVariantBlocks()
# 
# makeVoices()
# 
# measure()
# 
# measureOffsetMap()
# 
# measures()
# 
# melodicIntervals()
# 
# mergeElements()
# 
# metronomeMarkBoundaries()
# 
# offsetMap()
# 
# playingWhenAttacked()
# 
# plot()
# 
# pop()
# 
# quantize()
# 
# recurse()
# 
# remove()
# 
# removeByClass()
# 
# removeByNotOfClass()
# 
# repeatAppend()
# 
# repeatInsert()
# 
# replace()
# 
# restoreActiveSites()
# 
# scaleDurations()
# 
# scaleOffsets()
# 
# setDerivationMethod()
# 
# setElementOffset()
# 
# shiftElements()
# 
# show()
# 
# showVariantAsOssialikePart()
# 
# simultaneousAttacks()
# 
# sliceAtOffsets()
# 
# sliceByBeat()
# 
# sliceByGreatestDivisor()
# 
# sliceByQuarterLengths()
# 
# sort()
# 
# splitAtQuarterLength()
# 
# splitByClass()
# 
# storeAtEnd()
# 
# stripTies()
# 
# template()
# 
# toSoundingPitch()
# 
# toWrittenPitch()
# 
# transferOffsetToElements()
# 
# transpose()
# 
# voicesToParts()
# 
# write()
# 
# Methods inherited from StreamCoreMixin:
# 
# asTimespans()
# 
# asTree()
# 
# coreAppend()
# 
# coreElementsChanged()
# 
# coreGatherMissingSpanners()
# 
# coreGetElementByMemoryLocation()
# 
# coreGuardBeforeAddElement()
# 
# coreHasElementByMemoryLocation()
# 
# coreInsert()
# 
# coreSelfActiveSite()
# 
# coreStoreAtEnd()
# 
# Methods inherited from Music21Object:
# 
# containerHierarchy()
# 
# contextSites()
# 
# getAllContextsByClass()
# 
# getContextByClass()
# 
# getOffsetBySite()
# 
# getOffsetInHierarchy()
# 
# getSpannerSites()
# 
# informSites()
# 
# next()
# 
# previous()
# 
# purgeLocations()
# 
# purgeOrphans()
# 
# setOffsetBySite()
# 
# sortTuple()
# 
# splitAtDurations()
# 
# splitByQuarterLengths()
# 
# Methods inherited from ProtoM21Object:
# 
# isClassOrSubclass()
# 
# Measure instance variables
# 
# Measure.clefIsNew
# Boolean describing if the Clef is different than the previous Measure.
# 
# Measure.keyIsNew
# Boolean describing if KeySignature is different than the previous Measure.
# 
# Measure.layoutWidth
# A suggestion for layout width, though most rendering systems do not support this designation. Use SystemLayout objects instead.
# 
# Measure.number
# A number representing the displayed or shown Measure number as presented in a written Score.
# 
# Measure.numberSuffix
# If a Measure number has a string annotation, such as “a” or similar, this string is stored here. Note that in MusicXML, such suffixes often appear as prefixes to measure numbers. In music21 (like most measure numbering systems), these numbers appear as suffixes.
# 
# Measure.paddingLeft
# defines empty space at the front of the measure for purposes of determining beat, etc for pickup/anacrusis bars. In 4/4, a measure with a one-beat pickup note will have a paddingLeft of 3.0. (The name comes from the CSS graphical term for the amount of padding on the left side of a region.)
# 
# Measure.paddingRight
# defines empty space at the end of the measure for purposes of determining whether or not a measure is filled. In 4/4, a piece beginning a one-beat pickup note will often have a final measure of three beats, instead of four. The final measure should have a paddingRight of 1.0. (The name comes from the CSS graphical term for the amount of padding on the right side of a region.)
# 
# Measure.timeSignatureIsNew
# Boolean describing if the TimeSignature is different than the previous Measure.
# 
# Instance variables inherited from Stream:
# 
# autoSort
# 
# definesExplicitPageBreaks
# 
# definesExplicitSystemBreaks
# 
# isFlat
# 
# isSorted
# 
# recursionType
# 
# Instance variables inherited from Music21Object:
# 
# classSortOrder
# 
# groups
# 
# id
# 
# isStream
# 
# Part
# class music21.stream.Part(*args, **keywords)
# A Stream subclass for designating music that is considered a single part.
# 
# When put into a Score object, Part objects are all collected in the Score.parts call. Otherwise they mostly work like generic Streams.
# 
# Generally the hierarchy goes: Score > Part > Measure > Voice, but you are not required to stick to this.
# 
# Part groupings (piano braces, etc.) are found in the music21.layout module in the StaffGroup Spanner object.
# 
# Part bases
# 
# Stream
# 
# StreamCoreMixin
# 
# Music21Object
# 
# ProtoM21Object
# 
# Part read-only properties
# 
# Read-only properties inherited from Stream:
# 
# beat
# 
# beatDuration
# 
# beatStr
# 
# beatStrength
# 
# flat
# 
# highestOffset
# 
# highestTime
# 
# isGapless
# 
# iter
# 
# lowestOffset
# 
# notes
# 
# notesAndRests
# 
# pitches
# 
# secondsMap
# 
# semiFlat
# 
# sorted
# 
# spanners
# 
# variants
# 
# voices
# 
# Read-only properties inherited from StreamCoreMixin:
# 
# spannerBundle
# 
# Read-only properties inherited from Music21Object:
# 
# hasEditorialInformation
# 
# hasStyleInformation
# 
# measureNumber
# 
# Read-only properties inherited from ProtoM21Object:
# 
# classSet
# 
# classes
# 
# Part read/write properties
# 
# Part.partAbbreviation
# Gets or sets a string representing the abbreviated name of this part as a whole (not counting instrument changes, etc.).
# 
# It can be set explicitly (or set on parsing) or it can take its name from the first Instrument object encountered in the stream (or within a substream), first checking its .partAbbreviation, then checking its .instrumentAbbreviation
# 
# Can also return None.
# 

p = stream.Part()
p.partAbbreviation is None
# True
cl = instrument.Clarinet()
p.insert(0, cl)
p.partAbbreviation
# 'Cl'
p.remove(cl)
p.partAbbreviation is None
# True
p.insert(0, instrument.Flute())
p.partAbbreviation
# 'Fl'
p.partAbbreviation = 'Rd 1'
p.partAbbreviation
# 'Rd 1'
# Note that changing an instrument’s .partAbbreviation or .instrumentAbbreviation while it is already in the Stream will not automatically update this unless .coreElementsChanged() is called or this Stream’s elements are otherwise altered. This is because the value is cached so that O(n) searches through the Stream do not need to be done every time.
# 
# Part.partName
# Gets or sets a string representing the name of this part as a whole (not counting instrument changes, etc.).
# 
# It can be set explicitly (or set on parsing) or it can take its name from the first Instrument object encountered in the stream (or within a substream), first checking its .partName, then checking its .instrumentName
# 
# Can also return None.
# 

p = stream.Part()
p.partName is None
# True
cl = instrument.Clarinet()
p.insert(0, cl)
p.partName
# 'Clarinet'
p.remove(cl)
p.partName is None
# True
p.insert(0, instrument.Flute())
p.partName
# 'Flute'
p.partName = 'Reed 1'
p.partName
# 'Reed 1'
# Note that changing an instrument’s .partName or .instrumentName while it is already in the Stream will not automatically update this unless .coreElementsChanged() is called or this Stream’s elements are otherwise altered. This is because the value is cached so that O(n) searches through the Stream do not need to be done every time.
# 
# Read/write properties inherited from Stream:
# 
# atSoundingPitch
# 
# clef
# 
# duration
# 
# elements
# 
# finalBarline
# 
# keySignature
# 
# metadata
# 
# seconds
# 
# timeSignature
# 
# Read/write properties inherited from Music21Object:
# 
# activeSite
# 
# derivation
# 
# editorial
# 
# offset
# 
# priority
# 
# quarterLength
# 
# style
# 
# Part methods
# 
# Part.makeAccidentals(alteredPitches=None, cautionaryPitchClass=True, cautionaryAll=False, inPlace=True, overrideStatus=False, cautionaryNotImmediateRepeat=True, tiePitchSet=None)
# This overridden method of Stream.makeAccidentals provides the management of passing pitches from a past Measure to each new measure for processing.
# 
# TODO: by default inPlace should be False
# 
# Methods inherited from Stream:
# 
# activateVariants()
# 
# addGroupForElements()
# 
# allPlayingWhileSounding()
# 
# analyze()
# 
# append()
# 
# attachIntervalsBetweenStreams()
# 
# attachMelodicIntervals()
# 
# augmentOrDiminish()
# 
# beatAndMeasureFromOffset()
# 
# chordify()
# 
# clear()
# 
# cloneEmpty()
# 
# containerInHierarchy()
# 
# elementOffset()
# 
# expandRepeats()
# 
# explode()
# 
# extendDuration()
# 
# extendDurationAndGetBoundaries()
# 
# extendTies()
# 
# extractContext()
# 
# findConsecutiveNotes()
# 
# findGaps()
# 
# flattenUnnecessaryVoices()
# 
# getClefs()
# 
# getElementAfterElement()
# 
# getElementAtOrBefore()
# 
# getElementBeforeOffset()
# 
# getElementById()
# 
# getElementsByClass()
# 
# getElementsByGroup()
# 
# getElementsByOffset()
# 
# getElementsNotOfClass()
# 
# getInstrument()
# 
# getInstruments()
# 
# getKeySignatures()
# 
# getOverlaps()
# 
# getTimeSignatures()
# 
# hasElement()
# 
# hasElementOfClass()
# 
# hasMeasures()
# 
# hasPartLikeStreams()
# 
# hasVoices()
# 
# haveAccidentalsBeenMade()
# 
# index()
# 
# insert()
# 
# insertAndShift()
# 
# insertIntoNoteOrChord()
# 
# invertDiatonic()
# 
# isSequence()
# 
# isTwelveTone()
# 
# isWellFormedNotation()
# 
# lyrics()
# 
# makeBeams()
# 
# makeChords()
# 
# makeImmutable()
# 
# makeMeasures()
# 
# makeMutable()
# 
# makeNotation()
# 
# makeRests()
# 
# makeTies()
# 
# makeVariantBlocks()
# 
# makeVoices()
# 
# measure()
# 
# measureOffsetMap()
# 
# measures()
# 
# melodicIntervals()
# 
# mergeAttributes()
# 
# mergeElements()
# 
# metronomeMarkBoundaries()
# 
# offsetMap()
# 
# playingWhenAttacked()
# 
# plot()
# 
# pop()
# 
# quantize()
# 
# recurse()
# 
# remove()
# 
# removeByClass()
# 
# removeByNotOfClass()
# 
# repeatAppend()
# 
# repeatInsert()
# 
# replace()
# 
# restoreActiveSites()
# 
# scaleDurations()
# 
# scaleOffsets()
# 
# setDerivationMethod()
# 
# setElementOffset()
# 
# shiftElements()
# 
# show()
# 
# showVariantAsOssialikePart()
# 
# simultaneousAttacks()
# 
# sliceAtOffsets()
# 
# sliceByBeat()
# 
# sliceByGreatestDivisor()
# 
# sliceByQuarterLengths()
# 
# sort()
# 
# splitAtQuarterLength()
# 
# splitByClass()
# 
# storeAtEnd()
# 
# stripTies()
# 
# template()
# 
# toSoundingPitch()
# 
# toWrittenPitch()
# 
# transferOffsetToElements()
# 
# transpose()
# 
# voicesToParts()
# 
# write()
# 
# Methods inherited from StreamCoreMixin:
# 
# asTimespans()
# 
# asTree()
# 
# coreAppend()
# 
# coreElementsChanged()
# 
# coreGatherMissingSpanners()
# 
# coreGetElementByMemoryLocation()
# 
# coreGuardBeforeAddElement()
# 
# coreHasElementByMemoryLocation()
# 
# coreInsert()
# 
# coreSelfActiveSite()
# 
# coreStoreAtEnd()
# 
# Methods inherited from Music21Object:
# 
# containerHierarchy()
# 
# contextSites()
# 
# getAllContextsByClass()
# 
# getContextByClass()
# 
# getOffsetBySite()
# 
# getOffsetInHierarchy()
# 
# getSpannerSites()
# 
# informSites()
# 
# next()
# 
# previous()
# 
# purgeLocations()
# 
# purgeOrphans()
# 
# setOffsetBySite()
# 
# sortTuple()
# 
# splitAtDurations()
# 
# splitByQuarterLengths()
# 
# Methods inherited from ProtoM21Object:
# 
# isClassOrSubclass()
# 
# Part instance variables
# 
# Instance variables inherited from Stream:
# 
# autoSort
# 
# definesExplicitPageBreaks
# 
# definesExplicitSystemBreaks
# 
# isFlat
# 
# isSorted
# 
# recursionType
# 
# Instance variables inherited from Music21Object:
# 
# classSortOrder
# 
# groups
# 
# id
# 
# isStream
# 
# Score
# class music21.stream.Score(givenElements=None, *args, **keywords)
# A Stream subclass for handling multi-part music.
# 
# Almost totally optional (the largest containing Stream in a piece could be a generic Stream, or a Part, or a Staff). And Scores can be embedded in other Scores (in fact, our original thought was to call this class a Fragment because of this possibility of continuous embedding; though it’s probably better to embed a Score in an Opus), but we figure that many people will like calling the largest container a Score and that this will become a standard.
# 
# Score bases
# 
# Stream
# 
# StreamCoreMixin
# 
# Music21Object
# 
# ProtoM21Object
# 
# Score read-only properties
# 
# Score.parts
# Return all Part objects in a Score.
# 
# It filters out all other things that might be in a Score object, such as Metadata returning just the Parts.
# 

s = corpus.parse('bach/bwv66.6')
s.parts
# <music21.stream.iterator.StreamIterator for Score:0x104af3a58 @:0>
partStream = s.parts.stream()
partStream.classes
# ('Score', 'Stream', 'StreamCoreMixin', 'Music21Object', 'ProtoM21Object', 'object')
len(partStream)
# 4
# The partStream object is a full stream.Score object, thus the elements inside it can be accessed by index number or by id string, or iterated over:
# 

partStream[0]
# <music21.stream.Part Soprano>
partStream['Alto']
# <music21.stream.Part Alto>
for p in partStream:
# ...     print(p.id)
# Soprano
# Alto
# Tenor
# Bass
# Read-only properties inherited from Stream:
# 
# beat
# 
# beatDuration
# 
# beatStr
# 
# beatStrength
# 
# flat
# 
# highestOffset
# 
# highestTime
# 
# isGapless
# 
# iter
# 
# lowestOffset
# 
# notes
# 
# notesAndRests
# 
# pitches
# 
# secondsMap
# 
# semiFlat
# 
# sorted
# 
# spanners
# 
# variants
# 
# voices
# 
# Read-only properties inherited from StreamCoreMixin:
# 
# spannerBundle
# 
# Read-only properties inherited from Music21Object:
# 
# hasEditorialInformation
# 
# hasStyleInformation
# 
# measureNumber
# 
# Read-only properties inherited from ProtoM21Object:
# 
# classSet
# 
# classes
# 
# Score read/write properties
# 
# Read/write properties inherited from Stream:
# 
# atSoundingPitch
# 
# clef
# 
# duration
# 
# elements
# 
# finalBarline
# 
# keySignature
# 
# metadata
# 
# seconds
# 
# timeSignature
# 
# Read/write properties inherited from Music21Object:
# 
# activeSite
# 
# derivation
# 
# editorial
# 
# offset
# 
# priority
# 
# quarterLength
# 
# style
# 
# Score methods
# 
# Score.expandRepeats()
# Expand all repeats, as well as all repeat indications given by text expressions such as D.C. al Segno.
# 
# This method always returns a new Stream, with deepcopies of all contained elements at all level.
# 
# Score.flattenParts(classFilterList=('Note', 'Chord'))
# Given a Score, combine all Parts into a single Part with all elements found in each Measure of the Score.
# 
# The classFilterList can be used to specify which objects contained in Measures are transferred.
# 
# It also flattens all voices within a part.
# 
# To be deprecated at some point…
# 

s = corpus.parse('bwv66.6')
len(s.parts)
# 4
len(s.flat.notes)
# 165
post = s.flattenParts()
'Part' in post.classes
# True
len(post.flat.notes)
# 165
# Score.implode()
# Reduce a polyphonic work into two staves.
# 
# Currently, this is just a synonym for partsToVoices with voiceAllocation = 2, and permitOneVoicePerPart = False, but someday this will have better methods for finding identical parts, etc.
# 
# Score.makeNotation(meterStream=None, refStreamOrTimeRange=None, inPlace=False, bestClef=False, **subroutineKeywords)
# This method overrides the makeNotation method on Stream, such that a Score object with one or more Parts or Streams that may not contain well-formed notation may be transformed and replaced by well-formed notation.
# 
# If inPlace is True, this is done in-place; if inPlace is False, this returns a modified deep copy.
# 
# Score.measure(measureNumber, collect=('Clef', 'TimeSignature', 'Instrument', 'KeySignature'), gatherSpanners=True, indicesNotNumbers=False)
# Given a measure number (or measure index, if indicesNotNumbers is True) return another Score object which contains multiple parts but each of which has only a single Measure object if the Measure number exists, otherwise returns a score with parts that are empty.
# 
# This method overrides the measure() method on Stream to allow for finding a single “measure slice” within parts:
# 

bachIn = corpus.parse('bach/bwv324.xml')
excerpt = bachIn.measure(2)
excerpt
# <music21.stream.Score 0x10322b5f8>
len(excerpt.parts)
# 4
excerpt.parts[0].show('text')
# {0.0} <music21.instrument.Instrument 'P1: Soprano: '>
# {0.0} <music21.clef.TrebleClef>
# {0.0} <music21.key.Key of e minor>
# {0.0} <music21.meter.TimeSignature 4/4>
# {0.0} <music21.stream.Measure 2 offset=0.0>
    # {0.0} <music21.note.Note B>
    # {1.0} <music21.note.Note B>
    # {2.0} <music21.note.Note B>
    # {3.0} <music21.note.Note B>
# Note that the parts created have all the meta-information outside the measure unless this information appears in the measure itself at the beginning:
# 

bachIn.measure(1).parts[0].show('text')
# {0.0} <music21.instrument.Instrument 'P1: Soprano: '>
# {0.0} <music21.stream.Measure 1 offset=0.0>
    # {0.0} <music21.clef.TrebleClef>
    # {0.0} <music21.key.Key of e minor>
    # {0.0} <music21.meter.TimeSignature 4/4>
    # {0.0} <music21.layout.SystemLayout>
    # {0.0} <music21.note.Note B>
    # {2.0} <music21.note.Note D>
# This way the original measure objects can be returned without being altered.
# 
# The final measure slice of the piece can be obtained with index -1. Example: quickly get the last chord of the piece, without needing to run .chordify() on the whole piece:
# 

excerpt = bachIn.measure(-1)
excerptChords = excerpt.chordify()
excerptChords.show('text')
# {0.0} <music21.instrument.Instrument 'P1: Soprano: '>
# {0.0} <music21.clef.TrebleClef>
# {0.0} <music21.key.Key of e minor>
# {0.0} <music21.meter.TimeSignature 4/4>
# {0.0} <music21.stream.Measure 9 offset=0.0>
    # {0.0} <music21.chord.Chord E2 G3 B3 E4>
    # {4.0} <music21.bar.Barline type=final>

lastChord = excerptChords.recurse().getElementsByClass('Chord')[-1]
lastChord
# <music21.chord.Chord E2 G3 B3 E4>
# Note that we still do a .getElementsByClass(‘Chord’) since many pieces end with nothing but a rest…
# 
# Score.measureOffsetMap(classFilterList=None)
# This Score method overrides the measureOffsetMap() method of Stream. This creates a map based on all contained Parts in this Score. Measures found in multiple Parts with the same offset will be appended to the same list.
# 
# If no parts are found in the score, then the normal measureOffsetMap() routine is called.
# 
# This method is smart and does not assume that all Parts have measures with identical offsets.
# 
# Score.measures(numberStart, numberEnd, collect=('Clef', 'TimeSignature', 'Instrument', 'KeySignature'), gatherSpanners=True, indicesNotNumbers=False)
# This method overrides the measures() method on Stream. This creates a new Score stream that has the same measure range for all Parts.
# 
# The collect argument is a list of classes that will be collected; see Stream.measures()
# 

s = corpus.parse('bwv66.6')
post = s.measures(3, 5)  # range is inclusive, i.e., [3, 5]
len(post.parts)
# 4
len(post.parts[0].getElementsByClass('Measure'))
# 3
len(post.parts[1].getElementsByClass('Measure'))
# 3
# Score.partsToVoices(voiceAllocation: Union[int, List[Union[List, int]]] = 2, permitOneVoicePerPart=False, setStems=True)
# Given a multi-part Score, return a new Score that combines parts into voices.
# 
# The voiceAllocation parameter sets the maximum number of voices per Part.
# 
# The permitOneVoicePerPart parameter, if True, will encode a single voice inside a single Part, rather than leaving it as a single Part alone, with no internal voices.
# 

s = corpus.parse('bwv66.6')
len(s.flat.notes)
# 165
post = s.partsToVoices(voiceAllocation=4)
len(post.parts)
# 1
len(post.parts[0].getElementsByClass('Measure')[0].voices)
# 4
len(post.flat.notes)
# 165
# Score.sliceByGreatestDivisor(*, addTies=True, inPlace=False)
# Slice all duration of all part by the minimum duration that can be summed to each concurrent duration.
# 
# Overrides method defined on Stream.
# 
# Methods inherited from Stream:
# 
# activateVariants()
# 
# addGroupForElements()
# 
# allPlayingWhileSounding()
# 
# analyze()
# 
# append()
# 
# attachIntervalsBetweenStreams()
# 
# attachMelodicIntervals()
# 
# augmentOrDiminish()
# 
# beatAndMeasureFromOffset()
# 
# chordify()
# 
# clear()
# 
# cloneEmpty()
# 
# containerInHierarchy()
# 
# elementOffset()
# 
# explode()
# 
# extendDuration()
# 
# extendDurationAndGetBoundaries()
# 
# extendTies()
# 
# extractContext()
# 
# findConsecutiveNotes()
# 
# findGaps()
# 
# flattenUnnecessaryVoices()
# 
# getClefs()
# 
# getElementAfterElement()
# 
# getElementAtOrBefore()
# 
# getElementBeforeOffset()
# 
# getElementById()
# 
# getElementsByClass()
# 
# getElementsByGroup()
# 
# getElementsByOffset()
# 
# getElementsNotOfClass()
# 
# getInstrument()
# 
# getInstruments()
# 
# getKeySignatures()
# 
# getOverlaps()
# 
# getTimeSignatures()
# 
# hasElement()
# 
# hasElementOfClass()
# 
# hasMeasures()
# 
# hasPartLikeStreams()
# 
# hasVoices()
# 
# haveAccidentalsBeenMade()
# 
# index()
# 
# insert()
# 
# insertAndShift()
# 
# insertIntoNoteOrChord()
# 
# invertDiatonic()
# 
# isSequence()
# 
# isTwelveTone()
# 
# isWellFormedNotation()
# 
# lyrics()
# 
# makeAccidentals()
# 
# makeBeams()
# 
# makeChords()
# 
# makeImmutable()
# 
# makeMeasures()
# 
# makeMutable()
# 
# makeRests()
# 
# makeTies()
# 
# makeVariantBlocks()
# 
# makeVoices()
# 
# melodicIntervals()
# 
# mergeAttributes()
# 
# mergeElements()
# 
# metronomeMarkBoundaries()
# 
# offsetMap()
# 
# playingWhenAttacked()
# 
# plot()
# 
# pop()
# 
# quantize()
# 
# recurse()
# 
# remove()
# 
# removeByClass()
# 
# removeByNotOfClass()
# 
# repeatAppend()
# 
# repeatInsert()
# 
# replace()
# 
# restoreActiveSites()
# 
# scaleDurations()
# 
# scaleOffsets()
# 
# setDerivationMethod()
# 
# setElementOffset()
# 
# shiftElements()
# 
# show()
# 
# showVariantAsOssialikePart()
# 
# simultaneousAttacks()
# 
# sliceAtOffsets()
# 
# sliceByBeat()
# 
# sliceByQuarterLengths()
# 
# sort()
# 
# splitAtQuarterLength()
# 
# splitByClass()
# 
# storeAtEnd()
# 
# stripTies()
# 
# template()
# 
# toSoundingPitch()
# 
# toWrittenPitch()
# 
# transferOffsetToElements()
# 
# transpose()
# 
# voicesToParts()
# 
# write()
# 
# Methods inherited from StreamCoreMixin:
# 
# asTimespans()
# 
# asTree()
# 
# coreAppend()
# 
# coreElementsChanged()
# 
# coreGatherMissingSpanners()
# 
# coreGetElementByMemoryLocation()
# 
# coreGuardBeforeAddElement()
# 
# coreHasElementByMemoryLocation()
# 
# coreInsert()
# 
# coreSelfActiveSite()
# 
# coreStoreAtEnd()
# 
# Methods inherited from Music21Object:
# 
# containerHierarchy()
# 
# contextSites()
# 
# getAllContextsByClass()
# 
# getContextByClass()
# 
# getOffsetBySite()
# 
# getOffsetInHierarchy()
# 
# getSpannerSites()
# 
# informSites()
# 
# next()
# 
# previous()
# 
# purgeLocations()
# 
# purgeOrphans()
# 
# setOffsetBySite()
# 
# sortTuple()
# 
# splitAtDurations()
# 
# splitByQuarterLengths()
# 
# Methods inherited from ProtoM21Object:
# 
# isClassOrSubclass()
# 
# Score instance variables
# 
# Instance variables inherited from Stream:
# 
# autoSort
# 
# definesExplicitPageBreaks
# 
# definesExplicitSystemBreaks
# 
# isFlat
# 
# isSorted
# 
# recursionType
# 
# Instance variables inherited from Music21Object:
# 
# classSortOrder
# 
# groups
# 
# id
# 
# isStream
# 
# Opus
# class music21.stream.Opus(givenElements=None, *args, **keywords)
# A Stream subclass for handling multi-work music encodings. Many ABC files, for example, define multiple works or parts within a single file.
# 
# Opus objects can contain multiple Score objects, or even other Opus objects!
# 
# Opus bases
# 
# Stream
# 
# StreamCoreMixin
# 
# Music21Object
# 
# ProtoM21Object
# 
# Opus read-only properties
# 
# Opus.scores
# Return all Score objects in an iterator
# 
# Read-only properties inherited from Stream:
# 
# beat
# 
# beatDuration
# 
# beatStr
# 
# beatStrength
# 
# flat
# 
# highestOffset
# 
# highestTime
# 
# isGapless
# 
# iter
# 
# lowestOffset
# 
# notes
# 
# notesAndRests
# 
# pitches
# 
# secondsMap
# 
# semiFlat
# 
# sorted
# 
# spanners
# 
# variants
# 
# voices
# 
# Read-only properties inherited from StreamCoreMixin:
# 
# spannerBundle
# 
# Read-only properties inherited from Music21Object:
# 
# hasEditorialInformation
# 
# hasStyleInformation
# 
# measureNumber
# 
# Read-only properties inherited from ProtoM21Object:
# 
# classSet
# 
# classes
# 
# Opus read/write properties
# 
# Read/write properties inherited from Stream:
# 
# atSoundingPitch
# 
# clef
# 
# duration
# 
# elements
# 
# finalBarline
# 
# keySignature
# 
# metadata
# 
# seconds
# 
# timeSignature
# 
# Read/write properties inherited from Music21Object:
# 
# activeSite
# 
# derivation
# 
# editorial
# 
# offset
# 
# priority
# 
# quarterLength
# 
# style
# 
# Opus methods
# 
# Opus.getNumbers()
# Return a list of all numbers defined in this Opus.
# 

o = corpus.parse('josquin/oVenusBant')
o.getNumbers()
# ['1', '2', '3']
# Opus.getScoreByNumber(opusMatch)
# Get Score objects from this Stream by number. Performs title search using the search() method, and returns the first result.
# 

o = corpus.parse('josquin/oVenusBant')
o.getNumbers()
# ['1', '2', '3']
s = o.getScoreByNumber(2)
s.metadata.title
# 'O Venus bant'
s.metadata.alternativeTitle
# 'Tenor'
# Opus.getScoreByTitle(titleMatch)
# Get Score objects from this Stream by a title. Performs title search using the search() method, and returns the first result.
# 

o = corpus.parse('essenFolksong/erk5')
s = o.getScoreByTitle('Vrienden, kommt alle gaere')
s.metadata.title
# 'Vrienden, kommt alle gaere'
# Regular expressions work fine
# 

s = o.getScoreByTitle('(.*)kommt(.*)')
s.metadata.title
# 'Vrienden, kommt alle gaere'
# Opus.mergeScores()
# Some Opus objects represent numerous scores that are individual parts of the same work. This method will treat each contained Score as a Part, merging and returning a single Score with merged Metadata.
# 

from music21 import corpus
o = corpus.parse('josquin/milleRegrets')
s = o.mergeScores()
s.metadata.title
# 'Mille regrets'
len(s.parts)
# 4
