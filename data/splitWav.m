info = audioinfo('a-lona-le-utse-le-ithuta-dithuto-tseo-tsa-lona.wav');

Fs = info.SampleRate;
chunkDuration = 1; % 1 sec
numSamplesPerChunk = chunkDuration*Fs;

chunkCnt = 1;
for startLoc = 1:numSamplesPerChunk:info.TotalSamples
    endLoc = min(startLoc + numSamplesPerChunk - 1, info.TotalSamples);

    y = audioread('a-lona-le-utse-le-ithuta-dithuto-tseo-tsa-lona.wav', [startLoc endLoc]);
    outFileName = sprintf('a-lona-le-utse-le-ithuta-dithuto-tseo-tsa-lona%03d.wav', chunkCnt);
    audiowrite(outFileName, y, Fs);
    chunkCnt = chunkCnt + 1;
end