"""
the file checking for "#" char in the end of the line, in hebrew songs, and moving it to the start.
using because the "#" jumping from the end to the start in Right-To-Left mode.
"""

import glob
import os
import re

print("convert right left started")
RLM = u"\u200F"
LRM = u"\u200E"

this_folder = "/".join(os.path.realpath(__file__).split("/")[:-1])
chars_to_remove = ["A#6add9", "Ab6add9", "A#add9", "A#dim7", "A#m7b5", "A#maj7", "A#maj9", "A#sus2", "A#sus4", "A6add9",
                   "Abadd9", "Abdim7", "Abm7b5", "Abmaj7", "Abmaj9", "Absus2", "Absus4", "A#7#5", "A#7b5", "A#7b9",
                   "A#aug",
                   "A#dim", "A#m11", "Aadd9", "Ab7#5", "Ab7b5", "Ab7b9", "Abaug", "Abdim", "Abm11", "Adim7", "Am7b5",
                   "Amaj7",
                   "Amaj9", "Asus2", "Asus4", "A#11", "A#13", "A#m6", "A#m7", "A#m9", "A7#5", "A7b5", "A7b9", "Aaug",
                   "Ab11",
                   "Ab13", "Abm6", "Abm7", "Abm9", "Adim", "Am11", "A#6", "A#7", "A#9", "A#m", "A11", "A13", "Ab6",
                   "Ab7", "Ab9",
                   "Abm", "Am6", "Am7", "Am9", "A#", "A6", "A7", "A9", "Ab", "Am", "A", "Bb6add9", "B6add9", "Bbadd9",
                   "Bbdim7",
                   "Bbm7b5", "Bbmaj7", "Bbmaj9", "Bbsus2", "Bbsus4", "Badd9", "Bb7#5", "Bb7b5", "Bb7b9", "Bbaug",
                   "Bbdim",
                   "Bbm11", "Bdim7", "Bm7b5", "Bmaj7", "Bmaj9", "Bsus2", "Bsus4", "B7#5", "B7b5", "B7b9", "Baug",
                   "Bb11", "Bb13",
                   "Bbm6", "Bbm7", "Bbm9", "Bdim", "Bm11", "B11", "B13", "Bb6", "Bb7", "Bb9", "Bbm", "Bm6", "Bm7",
                   "Bm9", "B6",
                   "B7", "B9", "Bb", "Bm", "B", "C#6add9", "C#add9", "C#dim7", "C#m7b5", "C#maj7", "C#maj9", "C#sus2",
                   "C#sus4",
                   "C6add9", "C#7#5", "C#7b5", "C#7b9", "C#aug", "C#dim", "C#m11", "Cadd9", "Cdim7", "Cm7b5", "Cmaj7",
                   "Cmaj9",
                   "Csus2", "Csus4", "C#11", "C#13", "C#m6", "C#m7", "C#m9", "C7#5", "C7b5", "C7b9", "Caug", "Cdim",
                   "Cm11",
                   "C#6", "C#7", "C#9", "C#m", "C11", "C13", "Cm6", "Cm7", "Cm9", "C#", "C6", "C7", "C9", "Cm", "C",
                   "C",
                   "D#6add9", "Db6add9", "D#add9", "D#dim7", "D#m7b5", "D#maj7", "D#maj9", "D#sus2", "D#sus4", "D6add9",
                   "Dbadd9", "Dbdim7", "Dbm7b5", "Dbmaj7", "Dbmaj9", "Dbsus2", "Dbsus4", "D#7#5", "D#7b5", "D#7b9",
                   "D#aug",
                   "D#dim", "D#m11", "Dadd9", "Db7#5", "Db7b5", "Db7b9", "Dbaug", "Dbdim", "Dbm11", "Ddim7", "Dm7b5",
                   "Dmaj7",
                   "Dmaj9", "Dsus2", "Dsus4", "D#11", "D#13", "D#m6", "D#m7", "D#m9", "D7#5", "D7b5", "D7b9", "Daug",
                   "Db11",
                   "Db13", "Dbm6", "Dbm7", "Dbm9", "Ddim", "Dm11", "D#6", "D#7", "D#9", "D#m", "D11", "D13", "Db6",
                   "Db7", "Db9",
                   "Dbm", "Dm6", "Dm7", "Dm9", "D#", "D6", "D7", "D9", "Db", "Dm", "D", "Eb6add9", "E6add9", "Ebadd9",
                   "Ebdim7",
                   "Ebm7b5", "Ebmaj7", "Ebmaj9", "Ebsus2", "Ebsus4", "Eadd9", "Eb7#5", "Eb7b5", "Eb7b9", "Ebaug",
                   "Ebdim",
                   "Ebm11", "Edim7", "Em7b5", "Emaj7", "Emaj9", "Esus2", "Esus4", "E7#5", "E7b5", "E7b9", "Eaug",
                   "Eb11", "Eb13",
                   "Ebm6", "Ebm7", "Ebm9", "Edim", "Em11", "E11", "E13", "Eb6", "Eb7", "Eb9", "Ebm", "Em6", "Em7",
                   "Em9", "E6",
                   "E7", "E9", "Eb", "Em", "E", "F#6add9", "F#add9", "F#dim7", "F#m7b5", "F#maj7", "F#maj9", "F#sus2",
                   "F#sus4",
                   "F6add9", "F#7#5", "F#7b5", "F#7b9", "F#aug", "F#dim", "F#m11", "Fadd9", "Fdim7", "Fm7b5", "Fmaj7",
                   "Fmaj9",
                   "Fsus2", "Fsus4", "F#11", "F#13", "F#m6", "F#m7", "F#m9", "F7#5", "F7b5", "F7b9", "Faug", "Fdim",
                   "Fm11",
                   "F#6", "F#7", "F#9", "F#m", "F11", "F13", "Fm6", "Fm7", "Fm9", "F#", "F6", "F7", "F9", "Fm", "F",
                   "G#6add9",
                   "Gb6add9", "G#add9", "G#dim7", "G#m7b5", "G#maj7", "G#maj9", "G#sus2", "G#sus4", "G6add9", "Gbadd9",
                   "Gbdim7",
                   "Gbm7b5", "Gbmaj7", "Gbmaj9", "Gbsus2", "Gbsus4", "G#7#5", "G#7b5", "G#7b9", "G#aug", "G#dim",
                   "G#m11",
                   "Gadd9", "Gb7#5", "Gb7b5", "Gb7b9", "Gbaug", "Gbdim", "Gbm11", "Gdim7", "Gm7b5", "Gmaj7", "Gmaj9",
                   "Gsus2",
                   "Gsus4", "G#11", "G#13", "G#m6", "G#m7", "G#m9", "G7#5", "G7b5", "G7b9", "Gaug", "Gb11", "Gb13",
                   "Gbm6",
                   "Gbm7", "Gbm9", "Gdim", "Gm11", "G#6", "G#7", "G#9", "G#m", "G11", "G13", "Gb6", "Gb7", "Gb9", "Gbm",
                   "Gm6",
                   "Gm7", "Gm9", "G#", "G6", "G7", "G9", "Gb", "Gm", "G", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                   "0", "x", chr(32), chr(160), "/", "sus", "maj", "+", "aj", chr(8207)]
to_remove = {i: "" for i in chars_to_remove}
to_remove = dict((re.escape(k), v) for k, v in to_remove.items())
levels = [["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"],
          ["Ab", "A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F", "Gb", "G"]]
pattern = re.compile("|".join(to_remove.keys()))


def is_hebrew(s):
    return any("\u0590" <= c <= "\u05EA" for c in s)


def c_l(line):
    print("converting started")
    new_line = line
    print(line)
    if new_line[-1] == "#":
        new_line = "#" + new_line[:-1]

    return new_line


def n_k(data):
    print(data)
    print("converting started")
    new_data = ""

    for i in data:

        if i == "":
            new_data += '\n'
            print(i)
            continue

        print("before: ", i)
        j = pattern.sub(lambda m: to_remove[re.escape(m.group(0))], i)

        if j:
            print("regular: ", i)
            new_data += i
            new_data += '\n'
        else:
            print("chords: ", i)
            new_data += c_l(i)
            new_data += '\n'

    print("new data: ", new_data)
    return new_data


for fpath in glob.glob(this_folder + "/toUpload/*"):
    if is_hebrew(fpath):
        print(fpath)
        with open(fpath, "r+") as f:
            data = f.read().split('\n')
            data = n_k(data)
            song = ''.join(data)
            f.seek(0)
            f.truncate()
            f.write(song)
