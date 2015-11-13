import urllib
import urllib2
import re
import csv
import sys
import os


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

mp3Pattern = re.compile('http://media.*\.mp3')
titlePattern = re.compile('/(.+?)/track/smithsonian')
pagePattern = re.compile('http://.*/track/smithsonian')


req1 = urllib2.Request(url=link, headers=hdr)

f = urllib2.urlopen(req1)
sourceHTML = f.readlines()


for line in sourceHTML:

	if mp3Pattern.search(line):
		mp3Link = mp3Pattern.findall(line)[0]
		mp3Links.append(mp3Link)

	if pagePattern.search(line):
		pageLink = pagePattern.findall(line)[0]
		pageLinks.append(pageLink)
		trackName = titlePattern.findall(pageLink)[0]
		trackName = trackName.split('/')[-1]

		songDict[trackName] = mp3Link


# print(songDict)
print(len(songDict))

directory = "ILAM_samples"
if not os.path.exists(directory):
    os.makedirs(directory)

count = 0
for songname, songlink in songDict.iteritems():
	track = songname + ".mp3"
	fullfilename = os.path.join(directory, track)
	try:
		urllib.urlretrieve (songlink, fullfilename)
		count += 1
		print(str(count) + ' ' + songname+" DOWNLOADED!")
	except:
		print("--- ERROR :"+ songname + " FAILED")
	

		




