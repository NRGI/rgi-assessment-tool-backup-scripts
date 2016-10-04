#!/usr/bin/env python
import requests
import csv
import re
import sys

from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

SERVER_NAME = 'localhost:3030'
DESTINATION_PATH = "/home/alex/projects/backup-scripts"

PORTION_SIZE = 100

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
            else:
                try:
                    answer.append(answer_data[key])
                except KeyError:
                    answer.append("")

        csv_writer.writerow(answer)
