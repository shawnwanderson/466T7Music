import shutil
import sys
import os

subsetname = "V_and_D_and_C"	# change this value to D_only, D_and_C_only, etc..

inputf = "csv_subsets/subset_"+ subsetname + ".csv"

try:
	subset = open(inputf, 'r')
except:
	print('Something went wrong! Can\'t tell what?')
	sys.exit(0) # quit Python

data = subset.readlines()

inputdir = "ILAM_samples/"
outputdir = "mp3_subsets/"+subsetname#+'/'

if not os.path.exists(outputdir):
    os.makedirs(outputdir)  

for line in data:
	track = line.split(';')[0]
	title = track + ".mp3"
	srcfile = inputdir + title
	dstfile = outputdir + title 
	shutil.copy2(srcfile, outputdir)