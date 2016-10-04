#!/usr/bin/env python
import requests
import csv
import re
import sys

from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

SERVER_NAME = 'rgi.nrgi-assessment.org'
DESTINATION_PATH = "/Users/cperry/Box Sync/RAD/RGI/raw_data"

PORTION_SIZE = 100


def grep_bad_characters(string_parse):
    new_str = re.sub(r'[\xc2\xa0]', " ", string_parse)
    return new_str

csv_header = ['country_code']
answers = []
loaded_completely = False
page = 0

while not loaded_completely:
    res = requests.get('http://' + SERVER_NAME + '/api/raw_answers/' + str(PORTION_SIZE) + '/' + str(page))
    page += 1
    portion_data = res.json()
    loaded_completely = len(portion_data["data"]) < PORTION_SIZE
    answers += portion_data["data"]

    for field in portion_data["header"]:
        if not (field in csv_header):
            csv_header.append(field)

with open('raw_data' + datetime.now().strftime('%Y-%m-%d-%H:%M:%S') + '.csv', "w") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"')
    csv_writer.writerow(csv_header)

    for answer_data in answers:
        answer = []

        for key in csv_header:
            if key is "country_code":
                answer.append(answer_data["answer_ID"][0:2])
            elif key == "question_order" or key == "reviewer_score_history_order":
                try:
                    answer.append(answer_data[key])
                except KeyError:
                    answer.append("")
            else:
                try:
                    answer.append(grep_bad_characters(answer_data[key]))
                except KeyError:
                    answer.append("")

        try:
            csv_writer.writerow(answer)
        except UnicodeEncodeError:
            # print row[6]
            if answer[5] == "c":
                answer[6] = 'The government awards licenses/contracts via a first-come, first-served process.'
            elif answer[5] == "d":
                answer[6] = 'Through swap agreements, ' \
                         'whereby raw materials are exchanged or swapped for refined products, ' \
                         'financing (e.g. oil-backed loans) or other assets.'
            elif answer[8] == "c":
                answer[9] = 'The government awards licenses/contracts via a first-come, first-served process.'
            elif answer[8] == "d":
                answer[9] = 'Through swap agreements, whereby raw materials are exchanged or ' \
                         'swapped for refined products, financing (e.g. oil-backed loans) or other assets.'
            csv_writer.writerow(answer)
