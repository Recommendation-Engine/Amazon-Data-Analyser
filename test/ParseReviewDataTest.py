import sys, os, gzip
sys.path.insert(0, '../Data_Analyser')

from ParseReviewData import ParseReviewData
import unittest

class TestOutputDataSet(unittest.TestCase):

	def test(self):
		source = """product/productId: B000GKXY4S
product/title: Crazy Shape Scissor Set
review/userId: A1QA985ULVCQOB
review/score: 5.0
review/text: I really enjoy these scissors"""
		
		sourcefile = gzip.open("test.txt.gz",'wb')
		sourcefile.write(source)
		sourcefile.close()

		self.parseReviewData = ParseReviewData("test.txt.gz")
		self.parseReviewData.outputDataSet()

		with open("outputtest.txt.gz.txt",'r') as inputfile:
			line = next(inputfile)
			self.assertEqual(line,"B000GKXY4S\tA1QA985ULVCQOB\t5.0\n")

		os.remove("test.txt.gz")
		os.remove("outputtest.txt.gz.txt")

class TestFilterOriginDataSet(unittest.TestCase):

	def test_with_different_source(self):	
		def test_with_source(source):
			sourcefile = gzip.open("test.txt.gz",'wb')
			sourcefile.write(source)
			sourcefile.close()

			self.parseReviewData = ParseReviewData("test.txt.gz")
			self.parseReviewData.filterOriginDataSet()

			with open("filtertedtest.txt.gz.txt","r") as inputfile:
				line = next(inputfile)
				self.assertEqual(line.strip(),"review/userId: A1QA985ULVCQOB")
				
				line = next(inputfile)
				self.assertEqual(line.strip(),"product/productId: B000GKXY4S")
			
			os.remove("filtertedtest.txt.gz.txt")
			os.remove("test.txt.gz")

		ordered_source = """product/productId: B000GKXY4S
product/title: Crazy Shape Scissor Set
review/userId: A1QA985ULVCQOB
review/score: 5.0
review/text: I really enjoy these scissors"""
		disordered_source = """product/productId: B000GKXY4S
product/title: Crazy Shape Scissor Set
review/score: 5.0
review/userId: A1QA985ULVCQOB
review/text: I really enjoy these scissors"""
		
		test_with_source(ordered_source)
		test_with_source(disordered_source)
		

class TestGenerateDic(unittest.TestCase):

	def setUp(self):
		source = """product/productId: B000GKXY4S
review/userId: A1QA985ULVCQOB
review/score: 5.0

product/productId: B000GKXY41
review/userId: A1QA985ULVCQOB
review/score: 5.0

product/productId: B000GKXY42
review/userId: A1QA985ULVCQOB
review/score: 5.0

product/productId: B000GKXY43
review/userId: A1QA985ULVCQOB
review/score: 5.0

product/productId: B000GKXY4S
review/userId: A1QA985ULVCQOB
review/score: 5.0"""

		sourcefile = gzip.open("test.txt.gz",'wb')
		sourcefile.write(source)
		sourcefile.close()

		self.parseReviewData = ParseReviewData("test.txt.gz")
		self.parseReviewData.filterOriginDataSet()

	def tearDown(self):
		os.remove("filtertedtest.txt.gz.txt")
		os.remove("test.txt.gz")

	def test_with_duplicate_product_id(self):
		self.parseReviewData.generateDic()

		userDic = self.parseReviewData.getUserDic()

		self.assertEqual(userDic.keys(), ['A1QA985ULVCQOB'])
		self.assertEqual(len(userDic['A1QA985ULVCQOB']),4)

class TestGenerateStatDic(unittest.TestCase):
	def setUp(self):
		source = """product/productId: B000GKXY4S
review/userId: A1QA985ULVCQOB
review/score: 5.0

product/productId: B000GKXY41
review/userId: A1QA985ULVCQOB
review/score: 5.0

product/productId: B000GKXY43
review/userId: A1QA985ULVCQO1
review/score: 5.0

product/productId: B000GKXY4S
review/userId: A1QA985ULVCQO1
review/score: 5.0"""

		sourcefile = gzip.open("test.txt.gz",'wb')
		sourcefile.write(source)
		sourcefile.close()

		self.parseReviewData = ParseReviewData("test.txt.gz")
		self.parseReviewData.filterOriginDataSet()
		self.parseReviewData.generateDic()

	def tearDown(self):
		os.remove("filtertedtest.txt.gz.txt")
		os.remove("test.txt.gz")

	def test_two_people_comment_on_two_different_products(self):
		self.parseReviewData.generateStatDic()

		statDic = self.parseReviewData.getStatDic()

		self.assertEqual(statDic.keys(), [2])
		self.assertEqual(statDic[2],2)

if __name__ == '__main__':
	unittest.main()