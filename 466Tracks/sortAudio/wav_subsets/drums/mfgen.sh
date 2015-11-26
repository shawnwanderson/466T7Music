#!/bin/sh
mkcollection -c pos.mf -l 1 /home/shawn/Desktop/466/466T7Music/466Tracks/sortAudio/wav_subsets/drums/pos
mkcollection -c neg.mf -l 0 /home/shawn/Desktop/466/466T7Music/466Tracks/sortAudio/wav_subsets/drums/neg
cat pos.mf neg.mf > all.mf
bextract -sv all.mf -w all.arff
kea -w all.arff
