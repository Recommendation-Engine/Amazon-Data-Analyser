import sys, os
sys.path.insert(0, '../')

from ParseReviewData import ParseReviewData
import unittest

class TestFilterOriginDataSet(unittest.TestCase):

	def test_with_correct_content_order(self):
		self.parseReviewData = ParseReviewData("test.txt.gz")
		self.parseReviewData.filterOriginDataSet()

		with open("filtertedtest.txt.gz.txt","r") as inputfile:
			line = next(inputfile)
			self.assertEqual(line.strip(),"review/userId: A1QA985ULVCQOB")
			
			line = next(inputfile)
			self.assertEqual(line.strip(),"product/productId: B000GKXY4S")

		os.remove("filtertedtest.txt.gz.txt")
	
	def test_with_disorder_content(self):
		self.parseReviewData = ParseReviewData("testdisorder.txt.gz")
		self.parseReviewData.filterOriginDataSet()

		with open("filtertedtestdisorder.txt.gz.txt","r") as inputfile:
			line = next(inputfile)
			self.assertEqual(line.strip(),"review/userId: A1QA985ULVCQOB")
			
			line = next(inputfile)
			self.assertEqual(line.strip(),"product/productId: B000GKXY4S")

		os.remove("filtertedtestdisorder.txt.gz.txt")

class TestGenerateDic(unittest.TestCase):

	def setUp(self):
		self.parseReviewData = ParseReviewData("filtertedtest.txt")
		self.parseReviewData.filterOriginDataSet()

	def test_should_generate_correct_dictionary(self):
		self.parseReviewData.generateDic()

if __name__ == '__main__':
	unittest.main()