import sys
# v, d, c = [0, 0, 0]

# v, n			[1, 0, 0]
# d, n			[0, 1, 0]
# v, d, n		[1, 1, 0]
# c, n			[0, 0, 1]
# v, c, n		[1, 0, 1]
# c, d, n		[0, 1, 1]
# v, d, c 		[1, 1, 1]
# c, d, a		[]
# v, d, a
# v, c, a
# d, a
# c, a
# v, a

inputf = "instruments.csv"
outputf = "subset_V_and_D_and_C.csv"

try:
	dataset = open(inputf, 'r')
	subset = open(outputf, 'w')   # Trying to create a new file or open one
	# file.close()
except:
	print('Something went wrong! Can\'t tell what?')
	sys.exit(0) # quit Pyt	hon



data = dataset.readlines()

# print(data)

for line in data:
	if ("Vocals" in line) and ("Drum" in line) and ("Clapping" in line):
		subset.write(';'.join(line.split(";")))
		# subset.write(line.split(";")[0]+"\n")

dataset.close()
subset.close()






