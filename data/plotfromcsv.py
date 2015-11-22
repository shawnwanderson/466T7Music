import csv
import numpy as np
import pylab as pylab
import matplotlib.pyplot as plt
with open('zcrf_features.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    zero_crossing_vocal = []
    zero_crossing_drums = []
    zero_crossing_claps = []
    Centroid_vocal = []
    Centroid_drums = []
    Centroid_claps = []
    data = []
    for row in reader:
    	row.pop(0)
    	data.append(row)
    data.pop(0)
    for row in data:
    	if (int(row[0]) == 1):
    		zero_crossing_vocal.append(row[4])
    		Centroid_vocal.append(row[5])
    	if (int(row[1]) == 1):
    		zero_crossing_drums.append(row[4])
    		Centroid_drums.append(row[5])
    	if (int(row[2]) == 1):
    		zero_crossing_claps.append(row[4])
    		Centroid_claps.append(row[5])
    plt.plot(zero_crossing_vocal,Centroid_vocal,'ro',zero_crossing_drums,Centroid_drums,'bo',zero_crossing_claps,Centroid_claps,'go')
    plt.axis([0,0.5,0,0.5])
    plt.show()
