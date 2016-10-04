#!/usr/bin/env python
import requests
import csv
import re
import sys
reload(sys)
from pprint import pprint
from datetime import datetime
sys.setdefaultencoding('utf-8')

SERVER_NAME = 'rgi.nrgi-assessment.org'
DESTPATH = "/Users/cperry/Box Sync/RAD/RGI/raw_data"

PORTION_SIZE = 50

def grepBadChars(string_parse):
	new_str = re.sub(r'[\xc2\xa0]', " ", string_parse)
	return new_str

csv_header = ['country_code']
header_written = False

with open('raw_data' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + '.csv', "w") as csvfile:
	csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
	loaded_completely = False
	page = 0

	while loaded_completely == False:
		res = requests.get('http://' + SERVER_NAME + '/api/raw_answers/' + str(PORTION_SIZE) + '/' + str(page))
		page = page + 1
		answers = res.json()
		loaded_completely = len(answers["data"]) < PORTION_SIZE

		if header_written == False:
			csv_header = csv_header + answers["header"]
			csvwriter.writerow(csv_header)
			header_written = True

		for obj in answers["data"]:
			row = []
			for key in csv_header:
				if key is "country_code":
					row.append(obj["answer_ID"][0:2])
				elif key == "question_order" or key == "reviewer_score_history_order":
					try:
						row.append(obj[key])
					except KeyError:
						row.append("")
				else:
					try:
						row.append(grepBadChars(obj[key]))
					except KeyError:
						row.append("")

			try:
				csvwriter.writerow(row)
			except UnicodeEncodeError:
				# print row[6]
				if row[5] == "c":
					row[6] = 'The government awards licenses/contracts via a first-come, first-served process.'
				elif row[5] == "d":
					row[6] = 'Through swap agreements, whereby raw materials are exchanged or swapped for refined products, financing (e.g. oil-backed loans) or other assets.'
				elif row[8] == "c":
					row[9] = 'The government awards licenses/contracts via a first-come, first-served process.'
				elif row[8] == "d":
					row[9] = 'Through swap agreements, whereby raw materials are exchanged or swapped for refined products, financing (e.g. oil-backed loans) or other assets.'
				csvwriter.writerow(row)
