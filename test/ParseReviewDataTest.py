import sys, os, gzip
sys.path.insert(0, '../Data_Analyser')

from nose.tools import assert_equals
from ParseReviewData import ParseReviewData

class TestOutputDataSet:

	def generate_output_with_source(self, source):
		sourcefile = gzip.open("test.txt.gz",'wb')
		sourcefile.write(source)
		sourcefile.close()

		self.parseReviewData = ParseReviewData("test.txt.gz")
		self.parseReviewData.outputDataSet()

	def test_should_filter_unknown_value(self):
		source = """product/productId: B000GKXY4S
product/title: Crazy Shape Scissor Set
review/userId: unknown
review/score: unknown
review/text: I really enjoy these scissors"""
		self.generate_output_with_source(source)

		with open("outputtest.txt.gz.txt",'r') as inputfile:
			for line in inputfile:
				assert_equals(line,'')

		os.remove("test.txt.gz")
		os.remove("outputtest.txt.gz.txt")

	def test_should_generate_correct_format(self):
		source = """product/productId: B000GKXY4S
product/title: Crazy Shape Scissor Set
review/userId: A1QA985ULVCQOB
review/score: 5.0
review/text: I really enjoy these scissors"""
		
		self.generate_output_with_source(source)

		with open("outputtest.txt.gz.txt",'r') as inputfile:
			line = next(inputfile)
			assert_equals(line,"B000GKXY4S\tA1QA985ULVCQOB\t5.0\n")

		os.remove("test.txt.gz")
		os.remove("outputtest.txt.gz.txt")

class TestFilterOriginDataSet:

	def filter_with_source(self, source):
		sourcefile = gzip.open("test.txt.gz",'wb')
		sourcefile.write(source)
		sourcefile.close()

		self.parseReviewData = ParseReviewData("test.txt.gz")
		self.parseReviewData.filterOriginDataSet()

		with open("filtertedtest.txt.gz.txt","r") as inputfile:
			line = next(inputfile)
			assert_equals(line.strip(),"review/userId: A1QA985ULVCQOB")
			
			line = next(inputfile)
			assert_equals(line.strip(),"product/productId: B000GKXY4S")
		
		os.remove("filtertedtest.txt.gz.txt")
		os.remove("test.txt.gz")

	def test_with_ordered_source(self):	
		ordered_source = """product/productId: B000GKXY4S
product/title: Crazy Shape Scissor Set
review/userId: A1QA985ULVCQOB
review/score: 5.0
review/text: I really enjoy these scissors"""
		
		self.filter_with_source(ordered_source)
	
	def test_with_disordered_source(self):
		disordered_source = """product/productId: B000GKXY4S
product/title: Crazy Shape Scissor Set
review/score: 5.0
review/userId: A1QA985ULVCQOB
review/text: I really enjoy these scissors"""
		
		self.filter_with_source(disordered_source)

class TestGenerateDic:

	def filter_data_set(self,source):

		sourcefile = gzip.open("test.txt.gz",'wb')
		sourcefile.write(source)
		sourcefile.close()

		self.parseReviewData = ParseReviewData("test.txt.gz")
		self.parseReviewData.filterOriginDataSet()

	def teardown(self):
		os.remove("filtertedtest.txt.gz.txt")
		os.remove("test.txt.gz")

	def test_should_ignore_duplicate_product_id(self):
		source = """product/productId: B000GKXY4S
review/userId: A1QA985ULVCQOB
review/score: 5.0

product/productId: B000GKXY4S
review/userId: A1QA985ULVCQOB
review/score: 5.0"""
		self.filter_data_set(source)

		self.parseReviewData.generateDic()

		userDic = self.parseReviewData.getUserDic()
		assert_equals(userDic.keys(), ['A1QA985ULVCQOB'])
		assert_equals(len(userDic['A1QA985ULVCQOB']),1)

	def test_should_gernate_dic_correctly(self):
		source = """product/productId: B000GKXY4S
review/userId: A1QA985ULVCQOB
review/score: 5.0

product/productId: B000GKXY41
review/userId: A1QA985ULVCQOB
review/score: 5.0"""
		self.filter_data_set(source)

		self.parseReviewData.generateDic()

		userDic = self.parseReviewData.getUserDic()
		assert_equals(userDic.keys(), ['A1QA985ULVCQOB'])
		assert_equals(len(userDic['A1QA985ULVCQOB']),2)

class TestGenerateStatDic:
	def generate_user_dictionary(self, source):
		sourcefile = gzip.open("test.txt.gz",'wb')
		sourcefile.write(source)
		sourcefile.close()

		self.parseReviewData = ParseReviewData("test.txt.gz")
		self.parseReviewData.filterOriginDataSet()
		self.parseReviewData.generateDic()

	def tearDown(self):
		os.remove("filtertedtest.txt.gz.txt")
		os.remove("test.txt.gz")

	def test_with_two_people_comment_on_same_number_of_products(self):
		source = """product/productId: B000GKXY4S
review/userId: A1QA985ULVCQOB
review/score: 5.0

product/productId: B000GKXY4B
review/userId: A1QA985ULVCQO1
review/score: 5.0"""
		self.generate_user_dictionary(source)
		self.parseReviewData.generateStatDic()

		statDic = self.parseReviewData.getStatDic()
		print statDic

		assert_equals(statDic.keys(), [1])
		assert_equals(statDic[1],2)

	def test_with_two_people_comment_on_different_number_of_products(self):
		source = """product/productId: B000GKXY4S
review/userId: A1QA985ULVCQOB
review/score: 5.0

product/productId: B000GKXY4B
review/userId: A1QA985ULVCQO1
review/score: 5.0

product/productId: B000GKXY41
review/userId: A1QA985ULVCQO1
review/score: 5.0"""
		self.generate_user_dictionary(source)
		self.parseReviewData.generateStatDic()


		statDic = self.parseReviewData.getStatDic()

		assert_equals(statDic.keys(), [1,2])
		assert_equals(statDic[1],1)
		assert_equals(statDic[2],1)
