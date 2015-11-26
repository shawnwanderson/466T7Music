import csv
import sys
import os
import numpy as np
import pylab as pylab
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def main():
	""" 
		Description:
			Plots a scatterplot, plotting the two specified features, for the specified instrument 
			(if instrument present, green; if instrument absent, red)


		Usage example:
			$ python plot.py V zcrs ctd [0,0.5,0,0.5] ~/Documents/plots


		Arguments:
			- arg 1) Instrument ID: v, d or c 
			- arg 2) Feature ID for x-axis: zcrs, ctd, rlf, flx
			- arg 3) Feature ID for y-axis: zcrs, ctd, rlf, flx
			- arg 4) XY-range, i.e. [0, 0.5, 0, 1.0]
			- arg 4) Input file (& directory) name (a CSV file)
			- arg 5) Output file (& directory) name (a PNG file)


		Formats:
			- arg 1) A CSV file with the first line as [Track Name, Instrument 1, Instrument 2, Instrument 3, Feature 1, Feature 2, Feature 3, Feature 4]




		NOTE:
			The range argument is nont implemented. At the moment, the script will always plot from 0 to 0.5 on the x-axis, and 0 to 0.5 on the y-axis.


	"""


	args = {'instrument' : sys.argv[1],
			   'x-axis' : sys.argv[2],
			   'y-axis' : sys.argv[3],
			   'xyrange' : sys.argv[4],
			   'infile' : sys.argv[5],
			   'outdir' : sys.argv[6]}


	data = csv_to_dictionary(args['infile'])

	# print(data)
	scatterplot(data, args['instrument'], args['x-axis'], args['y-axis'], args['xyrange'], args['infile'], args['outdir'])



def csv_to_dictionary(infile):
	""" Takes a CSV file as input and creates a dictionary from it, with the first line used for keys. """

	dataDict = {}


	try:
		dataset = open(infile, 'r')
	except:
		print('ERROR - No such file.')
		sys.exit(0)

	keys = []
	keys_aux = dataset.readline().split(',')
	for key in keys_aux:
		keys.append(key.lstrip().rstrip())

	values = dataset.readlines()
	

	# initialize the value for each key as an empty list
	for kindex, key in enumerate(keys):
		dataDict[key] = []



	for line in values:
		for kindex, key in enumerate(keys):
			dataDict[key].append(line.rstrip().split(',')[kindex])



	return dataDict




def scatterplot(data, instrument, xfeat, yfeat, xyrange, infile, outdir):

	id2kw = {'v': 'Vocals',
		   	 'd': 'Drums',
		   	 'c': 'Claps',
		   	 'zcrs': 'Zero-Crossing',
		   	 'ctd': 'Centroid',
		   	 'rlf': 'Roll Off',
		   	 'flx': 'Flux'}

	featurex_instrument_yes = []
	featurex_instrument_no = []
	featurey_instrument_yes = []
	featurey_instrument_no = []

	for sample_i in range(len(data["Track Name"])):

		if (int(data[id2kw[instrument]][sample_i]) == 0):
			featurex_instrument_no.append(data[id2kw[xfeat]][sample_i])
			featurey_instrument_no.append(data[id2kw[yfeat]][sample_i])
			red_dot, = plt.plot(featurex_instrument_no,featurey_instrument_no, 'ro')

		if (int(data[id2kw[instrument]][sample_i]) == 1):
			featurex_instrument_yes.append(data[id2kw[xfeat]][sample_i])
			featurey_instrument_yes.append(data[id2kw[yfeat]][sample_i])
			green_dot, = plt.plot(featurex_instrument_yes,featurey_instrument_yes, 'go')
		
	plt.legend([green_dot, red_dot], ["With "+id2kw[instrument], "Without "+id2kw[instrument]])
	plt.axis([0,0.5,0,0.5])#list(xyrange))
	plt.xlabel(id2kw[xfeat])
	plt.ylabel(id2kw[yfeat])

	
	if not os.path.exists(outdir):
		os.makedirs(outdir)



	plt.savefig(outdir+'/'+instrument+'_'+yfeat+'_vs_'+xfeat+'.png')






if __name__ == "__main__":
	main()