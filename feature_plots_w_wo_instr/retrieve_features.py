import sys


""" Returns the output in a csv file in the following format:
	trackname, vocals, drums, claps, zerocrossing, centroid, rolloff, flux
"""


featuresf = "MARSYAS_EMPTYILAM_zcrf.arff"
instrumentsf = "instruments.csv"
outfile = "zcrf_features_notrack.csv"

try:
	inputf1 = open(featuresf, 'r')
	inputf2 = open(instrumentsf, 'r')
	outputf = open(outfile, 'w')
except:
	print("Could not open "+ featuresf)
	sys.exit(0)


dataset = inputf1.readlines()

data = {}

for index, line in enumerate(dataset):
	if "filename" in line:
		track = (line.split('/')[-1])[0:-5]
		features = dataset[index+2].split(',')[0:4]
		# data[track] = {"zcrs": features[0], "ctd": features[1], "rlf": features[2], "flx": features[3]}
		data[track] = features

for line in inputf2:
	vs = ds = cs = 0
	if "Vocals" in line:
		vs = 1
	if "Drum" in line:
		ds = 1
	if "Clapping" in line:
		cs = 1

	data[line.split(';')[0]].append(vs)
	data[line.split(';')[0]].append(ds)
	data[line.split(';')[0]].append(cs)
	# data[line.split(';')[0]] = {"vocals": vs, "drums": ds, "claps": cs}


data_view = [ (songname,features) for songname,features in data.iteritems() ]
data_view.sort()

# +str(line[1]['vocals'])+','+str(line[1]['drums'])+','+str(line[1]['claps'])+','

# outputf.write("Track Name, Vocals, Drums, Claps, Zero-Crossing, Centroid, Roll Off, Flux\n")
outputf.write("Vocals, Drums, Claps, Zero-Crossing, Centroid, Roll Off, Flux\n")

for line in data_view:
	# print(line)
	try:
		# entry = line[0]+','+str(line[1][4])+','+str(line[1][5])+','+str(line[1][6])+','+line[1][0]+','+line[1][1]+','+line[1][2]+','+line[1][3]+'\n'
		entry = str(line[1][4])+','+str(line[1][5])+','+str(line[1][6])+','+line[1][0]+','+line[1][1]+','+line[1][2]+','+line[1][3]+'\n'
		print(entry)
		outputf.write(entry)
	except:
		print(line[0]+" -- The file is missing instruments data\n")
	# outputf.write(entry)
