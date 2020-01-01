from music21 import *

#######################################################################################
def getNotesFromScore(score):
    tonic = score.flat.keySignature.asKey().tonic.name
    print("score.filePath.name = " + score.filePath.name)
    print("tonic = " + tonic)
    tonicNote = note.Note(tonic)
    print("tonicNote = " + str(tonicNote))

    # We'll assume the first part is the top-line melody
    # FIXME: add more checks, e.g., is it labeled voice?
    melody = score.getElementsByClass(stream.Part)[0]

    intervals = []
    for myNote in melody.recurse().notes:
        # print("myNote = " + str(myNote))

        # Make sure it's not a ChordSymbol, Rest, or some other non-Note.
        # And skip tied notes.
        if myNote.isNote and (getattr(myNote, 'tie.type', None) != 'stop'):
            # print("interval = " + str(interval.Interval(tonicNote, myNote)))
            # print("myNote = " + str(myNote))

            # Compute the interval between the tonic and the note under inspection, e.g., M2, P5, m6
            myInterval = interval.Interval(tonicNote, myNote)
            intervals.append(myInterval)

    return intervals
#######################################################################################

aNewLocalCorpus = corpus.corpora.LocalCorpus('newCorpus')
aNewLocalCorpus.existsInSettings
# False
aNewLocalCorpus.delete()
aNewLocalCorpus.removePath("/Users/hmdcadministrator/Documents/MuseScore3/Scores")
aNewLocalCorpus.removePath("~/Documents/MuseScore3/Scores")
aNewLocalCorpus.addPath('./scores')
#aNewLocalCorpus.directoryPaths ('/Users/josiah/Desktop',)
aNewLocalCorpus.save()
aNewLocalCorpus.existsInSettings

corpus.manager.listLocalCorporaNames()
# [None, 'funk', 'newCorpus', 'bach']
# Note

# When running listLocalCorporaNames(), you will see None - indicating the default
# local corpus - along with the names of any non-default local corpora you’ve manually
#  yourself. In the above example, a number of other corpora have already been created.
#
# In Python2, take care to make all of these “unicode” entries.
#
# Finally, we can delete the local corpus we previously created like this:

# aNewLocalCorpus.delete()
aNewLocalCorpus.existsInSettings
allScores = aNewLocalCorpus.all()
print(aNewLocalCorpus.all())

allNotes = []
i = 0
for el in allScores:
    score = el.parse()
    i = i + 1
    allNotes = allNotes + getNotesFromScore(score)

print("All done.")
exit;

#  False
# Inspecting metadata bundle search results
# Let’s take a closer look at some search results:

#bachBundle = corpus.corpora.CoreCorpus().search('bach', 'composer')
bachBundle = aNewLocalCorpus.search('lennon')
bachBundle
 # <music21.metadata.bundles.MetadataBundle {362 entries}>
bachBundle[0]
 # <music21.metadata.bundles.MetadataEntry: bach_bwv10_7_mxl>
bachBundle[0].sourcePath
 # PosixPath('bach/bwv10.7.mxl')
bachBundle[0].metadata
 # <music21.metadata.RichMetadata at 0x11e2bd1d0>
bachBundle[0].metadata.all()
#  [('ambitus',
#    "AmbitusShort(semitones=34, diatonic='m7', pitchLowest='G2', pitchHighest='F5')"),
#   ('composer', 'J.S. Bach'),
#   ('keySignatureFirst', '<music21.key.Key of g minor>'),
#   ('keySignatures',
#    "['<music21.key.Key of g minor>', '<music21.key.Key of B- major>']"),
#   ('movementName', 'bwv10.7.mxl'),
#   ('noteCount', '214'),
#   ('numberOfParts', '4'),
#   ('pitchHighest', 'F5'),
#   ('pitchLowest', 'G2'),
#   ('quarterLength', '88.0'),
#   ('sourcePath', 'bach/bwv10.7.mxl'),
#   ('timeSignatureFirst', '4/4'),
#   ('timeSignatures', "['4/4']")]


mdpl = bachBundle[0].metadata
mdpl.noteCount
# 214
bachAnalysis0 = bachBundle[0].parse()
# print("notes = " + str(bachAnalysis0.recurse().notes))

# 'F'
# Get key tonic
# Open in MuseScore
# bachAnalysis0.show()

1

