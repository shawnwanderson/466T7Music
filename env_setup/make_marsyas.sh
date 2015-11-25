#!/bin/sh
cd marsyas/
mkdir build
cd build
cmake -DWITH_QT=OFF -D MARSYAS_MIDIIO=OFF -D MARSYAS_JACK=ON -D WITH_OSC=ON -D WITH_SWIG=ON -D PYTHON_INCLUDE_PATH=/usr/include/python2.7/ ..
make
sudo make install
