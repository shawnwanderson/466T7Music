'''
Copyright (c) 2013-2015, Gregory Burlet, Abram Hindle

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

from __future__ import division
from glob import glob
import os
import marsyas
import marsyas_util
import numpy as np
from scipy.signal import butter
import sys

import theano
import theano.tensor as T

class StreamFeatureExtractor:
    '''
    From sound card input, extract spectral features for each window
    '''

    def __init__(self, w, h, featuredef, dsf=1, verbose=False):
        '''
        Initialize the feature extractor. Note that if dsf > 0, the sampling rate (f) of the 
        input audio files will become f/dsf. This is decimation, so a butterworth low-pass filter is 
        applied prior to downsampling to mitigate against aliasing.

        PARAMETERS:
            audio_path (String) or (List): path to directory containing audio files or list of audio paths
            annotation_path (String): path to directory containing midi files corresponding
                to the audio files in 'audio_path'. Note: midi files must have the same 
                filename as its corresponding audio file, with a .midi extension of course.
            w (int): window size (samples)
            h (int): window hop size (samples)
            featuredef (dict): dict containing type and parameters for feature extraction
                for STFT: featuredef = {type: 'STFT'}
                for MFCC: featuredef = {type: 'MFCC', coefficients: x}
            dsf (int): downsampling factor
            verbose (bool)
        '''

        # cache feature extraction parameters
        self._w = w             
        self._h = h
        self._featuredef = featuredef
        self._dsf = dsf 
        self._verbose = verbose
        self._fs = 44100        # default sampling rate (Hz)
        self._pitch_offset = 36 # starting MIDI number of class labels, i.e., class label 0 is MIDI pitch 36
        self._num_pitches = 51  # 51 pitches: MIDI number 36 (C2: 65.406Hz) -- MIDI number 86 (D6: 1174.7Hz)
        self._max_poly = 0      # maximum number of pitches per frame (populated in function _extract_labels)
        self._num_features = 0  # dimensionality of feature vector (populated in function _extract_features)

        self.data = []
        self._oldmax = 0.0
        self._assemble_network()

    def _assemble_network(self):
        '''
        Helper function to construct the Marsyas network for preprocessing and feature extraction
        '''
        
        mng = marsyas.MarSystemManager()
        self._net = mng.create("Series", "extract_features")
        self._net.addMarSystem(mng.create("AudioSource", "src"))
        self._net.addMarSystem(mng.create("MixToMono", "mono"))
        
        if self._dsf > 1:
            # butterworth low-pass filter
            f_order = 9
            b, a = butter(f_order, 0.9/self._dsf, 'lowpass')
            bcoeffs = marsyas.realvec(1, f_order+1)
            acoeffs = marsyas.realvec(1, f_order+1)
            for i in range(f_order+1):
                bcoeffs[i] = b[i]
                acoeffs[i] = a[i]
            self._net.addMarSystem(mng.create("Filter", "lowpass"))

            self._net.updControl("Filter/lowpass/mrs_realvec/ncoeffs", marsyas.MarControlPtr.from_realvec(bcoeffs))
            self._net.updControl("Filter/lowpass/mrs_realvec/dcoeffs", marsyas.MarControlPtr.from_realvec(acoeffs))

            self._net.addMarSystem(mng.create("DownSampler", "down"))
            self._net.updControl("DownSampler/down/mrs_natural/factor", self._dsf)

        self._net.addMarSystem(mng.create("ShiftInput", "slice"))
        self._net.addMarSystem(mng.create("Windowing", "win"))
        self._net.addMarSystem(mng.create("Spectrum", "fft"))
        self._net.addMarSystem(mng.create("PowerSpectrum", "pspec"))

        if self._featuredef["type"] == "MFCC":
            # takes DFT as input
            self._net.addMarSystem(mng.create("MFCC", "mfcc"))
            self._net.updControl("MFCC/mfcc/mrs_natural/coefficients", int(self._featuredef["coefficients"]))

        # create control links
        self._net.linkControl("mrs_bool/hasData", "AudioSource/src/mrs_bool/hasData")

        # set algorithm parameters
        self._net.updControl("ShiftInput/slice/mrs_natural/winSize", self._w)
        self._net.updControl("mrs_natural/inSamples", self._h*self._dsf)
        self._net.updControl("mrs_real/israte", 44100.0)
        self._net.updControl("ShiftInput/slice/mrs_bool/reset", marsyas.MarControlPtr.from_bool(True))
        self._net.updControl("Windowing/win/mrs_string/type", "Hamming")
        self._net.updControl("PowerSpectrum/pspec/mrs_string/spectrumType", "power")
        self._net.updControl("AudioSource/src/mrs_bool/initAudio", marsyas.MarControlPtr.from_bool(True));

    def extract_features(self):
        '''
        Extract the windowed features from the mic
        '''

        # STFT vector structure: [Re(0), Re(N/2), Re(1), Im(1), Re(2), Im(2), ..., Re(N/2-1), Im(N/2-1)]
        # create mask to gather only real components (an audio signal is real so the imaginary values are redundant)
        # for i, s in enumerate(self.data):
        #    self._net.updControl("SoundFileSource/src/mrs_string/filename", s['audio_path'])
        # num_samples = self._net.getControl("AudioSource/src/mrs_natural/size").to_natural() / self._dsf
        if self._dsf > 1:
            self._fs = self._net.getControl("DownSampler/down/mrs_real/osrate").to_real()
        else:
            self._fs = self._net.getControl("AudioSource/src/mrs_real/osrate").to_real()
        num_wins = 1 # int(num_samples/self._h)+1   # marsyas zero-pads the last window
        # calculate number of features
        if self._featuredef["type"] == "STFT":
            self._num_features = int(self._w/2)+1
        elif self._featuredef["type"] == "MFCC":
            self._num_features = int(self._featuredef["coefficients"])

        sx = np.zeros([num_wins, self._num_features], dtype=np.float32)   # initialize feature matrix for song
        iwin = 0
        if self._net.getControl("mrs_bool/hasData").to_bool():
            self._net.tick()
            out = self._net.getControl("mrs_realvec/processedData").to_realvec()
            sx[iwin,:] = np.array(out, dtype=np.float32)
            # running normalization
            self._oldmax = max(0.99*self._oldmax,np.max(np.abs(sx)))
            sx = sx / self._oldmax
            iwin += 1
            
            # update progress bar
            X = theano.shared(sx, borrow=False)
            return X
        return None

        

    def _speak(self, msg):
        '''
        Helper function to print to the terminal and support printing progress bars
        '''

        if self._verbose:
            sys.stdout.write(msg)
            sys.stdout.flush()

if __name__ == "__main__":
    fe = StreamFeatureExtractor(2048, 1536, {"type":"STFT"})
    for i in range(0,10000):
        v = fe.extract_features()
        print(sum(v.get_value()[0]))

