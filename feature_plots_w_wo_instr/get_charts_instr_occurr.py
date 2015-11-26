import csv
import numpy as np
import pylab as pylab
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# vocals row[0]
# drums row[1]
# claps row[2]
# zero crossing row[3]
# centroid row[4]
# roll off row[5]
# flux row[6]


with open('zcrf_features.csv') as f:
	reader = csv.reader(f)
	featurex_instrument_yes = []
	featurex_instrument_no = []
	featurey_instrument_yes = []
	featurey_instrument_no = []

	data = []
	for row in reader:
		row.pop(0)
		data.append(row)
	data.pop(0)

	for row in data:
		if (int(row[2]) == 0):
			featurex_instrument_no.append(row[3])
			featurey_instrument_no.append(row[5])
			red_dot, = plt.plot(featurex_instrument_no,featurey_instrument_no, 'ro')
		if (int(row[2]) == 1):
			featurex_instrument_yes.append(row[3])
			featurey_instrument_yes.append(row[5])
			green_dot, = plt.plot(featurex_instrument_yes,featurey_instrument_yes, 'go')
		
	plt.legend([red_dot, green_dot], ["With vocals", "Without vocals"])
	plt.axis([0,0.5,0,0.15])
	plt.xlabel('Zero Crossing')
	plt.ylabel('Centroid')

	
	plt.savefig('C_rlf_vs_zcrs.png')