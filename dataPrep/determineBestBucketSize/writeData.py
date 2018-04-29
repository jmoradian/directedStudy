import csv, time, os

BUCKET_SIZES = [1., .5, .25]
MATRIX_FILEPATH = 'featureMatrices/BucketSizeFeatureMatrix'
EXTENSION = '.csv'


PERCENT_LABELS_FILEPATH = 'labels/percentLabels.csv'
ONE_HOT_LABELS_FILEPATH = 'labels/oneHotLabels.csv'





def writeFeatureMatrix(feature_matrix):
	for bucketSize in BUCKET_SIZES:
		fname = MATRIX_FILEPATH + str(bucketSize).replace('.','') + EXTENSION
		with open(fname, 'w') as csvfile:
			writer = csv.writer(csvfile)
			writer.writerows(feature_matrix[bucketSize])



def writePercentLabels(labels):
	labelMatrix = [[val] for val in labels]

	with open(PERCENT_LABELS_FILEPATH, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(labelMatrix)


def writeOneHotBinaryLabels(labels):
	with open(ONE_HOT_LABELS_FILEPATH, 'w') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerows(labels)