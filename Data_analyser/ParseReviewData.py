from collections import defaultdict
import os, gzip

class ParseReviewData(object):
	def __init__(self, inputfile):
		self.__userDic = defaultdict(set)
		self.__stat = defaultdict(int)
		self.__N = 0
		self.__input = inputfile
		self.__filteredinput = "filterted" + inputfile + ".txt"
		self.__output = "result" + inputfile + ".txt"

	def getUserDic(self):
		return self.__userDic

	def getStatDic(self):
		return self.__stat

	def parseDataSet(self):
		self.filterOriginDataSet()
		self.generateDic()
		self.generateStatDic()
		self.printResult()
		self.deleteTempFiles()

	def findUserId(self, line, inputfile):
		while "review/userId:" not in line:
			line = next(inputfile)
		return line

	def findScore(self, line, inputfile):
		while "review/score:" not in line:
			line = next(inputfile)
		return line

	def filterOriginDataSet(self):
		with gzip.open(self.__input,'r') as inputfile:
			with open(self.__filteredinput, 'wb') as outputfile:
				for line in inputfile:
					if "product/productId:" in line:
						outputfile.write(self.findUserId(line,inputfile))
						outputfile.write(line + "\n")						

	def outputDataSet(self):
		with gzip.open(self.__input,'r') as inputfile:
			with open("output"+self.__input+".txt", 'wb') as outputfile:
				for line in inputfile:
					if "product/productId:" in line:
						userId = self.getId(self.findUserId(line,inputfile))
						score = self.getId(self.findScore(line,inputfile))
						productId = self.getId(line)

						if userId == "unknown" or score == "unknown":
							continue
							
						outputfile.write(productId + "\t" + userId + "\t"
							+ score + "\n")

	def generateDic(self):
		with open(self.__filteredinput, 'r') as inputfile:
			for line in inputfile:
				if "review/userId:" not in line:
					continue

				userId = self.getId(line)
				
				if userId == "unknown":
					continue
				
				productId = self.getId(next(inputfile))	
				self.addReview(userId, productId)
				
	def generateStatDic(self):
		for key in self.__userDic:
			self.__stat[len(self.__userDic[key])] += 1

	def printResult(self):
		with open(self.__output,'wb') as outputfile:
			for key in self.__stat:
				outputfile.write("There are " + str(self.__stat[key]) + 
					" users comment on " + str(key) + " of products" + "\n")

	def deleteTempFiles(self):	
		os.remove(self.__filteredinput)

	def printProcedure(self):
		self.__N += 1
		if self.__N % 10000 == 0:
			print self.__N
		
	def addReview(self, userId, productId):
		self.printProcedure()
		self.__userDic[userId].add(productId)

	def getId(self, line):
		return line.strip().split(':')[1].strip()