from ParseReviewData import ParseReviewData

def main():
	inputfile = "Electronics.txt.gz"
	
	parseReviewData = ParseReviewData(inputfile)

	parseReviewData.outputDataSet()


if __name__ == '__main__':
	main()