import gzip

with gzip.open("allReviews.txt.gz",'r') as inputfile:
	with open("testContent.txt","wb") as outputfile:
		n = 0
		for line in inputfile:
			if n > 10000:
				break
			n += 1
			outputfile.write(line.strip())