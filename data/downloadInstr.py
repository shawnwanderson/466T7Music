import urllib
import urllib2
import re
import csv
import sys

 

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}

link = 'http://www.folkways.si.edu/search/?JsonSearchModel={%22FiltersModel%22%3A{%22AppliedFilters%22%3A{}%2C%22AvailableContentTypes%22%3A[0%2C2%2C1%2C3%2C5]%2C%22ContentType%22%3A2}%2C%22PaginationModel%22%3A{%22ResultsPerPage%22%3A509%2C%22StartItemIndex%22%3A0}%2C%22Query%22%3A%22ilam%22%2C%22SelectedView%22%3A1%2C%22SortingOption%22%3A0%2C%22SpellingSuggestionSearchRestricted%22%3Afalse}'

songDict = {}
mp3Links = []
pageLinks = []
instDict = {}

mp3Pattern = re.compile('http://media.*\.mp3')
titlePattern = re.compile('/(.+)?/track/smithsonian')
pagePattern = re.compile('http://.*/track/smithsonian')
previnstPattern = re.compile('Instrument\(s\)')
#instPattern = re.compile('<meta content="(.+?)" name="Instrument" />')
instPattern = re.compile('">(.*?)</a>')


req1 = urllib2.Request(url=link, headers=hdr)

f = urllib2.urlopen(req1)
sourceHTML = f.readlines()



# Creating a new file to contain the metadata
#---------------------------------------------
filename = "instruments.csv"

try:
    metadata = open(filename,'w')   # Trying to create a new file or open one
    # file.close()
except:
    print('Something went wrong! Can\'t tell what?')
    sys.exit(0) # quit Python




for line in sourceHTML:

	if pagePattern.search(line):
		pageLink = pagePattern.findall(line)[0]
		pageLinks.append(pageLink)
		trackName = titlePattern.findall(pageLink)[0]
		trackName = trackName.split('/')[-1]


		try:
			req = urllib2.Request(url=pageLink, headers=hdr)
			page = urllib2.urlopen(req)
			pageHTML = page.readlines()

			print("Fetching " + trackName)

			for index, line in enumerate(pageHTML):
				# print(line)
				if previnstPattern.search(line):
					# print(pageHTML[index+1])
					instruments = instPattern.findall(pageHTML[index+1])
					# print(str(instruments))
					instDict[trackName] = instruments
					# instDict[trackName] = instruments.split('|')
					break

		except:
			print(trackName+" ------------------- Bad request!")


instDict_view = [ (songname,instrs) for songname,instrs in instDict.iteritems() ]
instDict_view.sort()
for songname, instrs in instDict_view:
	metadata.write(songname + ';' + ";".join(instrs)+'\n')
	print(songname + ';' + ";".join(instrs))





metadata.close()

		




