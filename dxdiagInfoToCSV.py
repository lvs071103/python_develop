#!/usr/bin/python
# --*-- coding: utf-8 --*--


import re
import csv
import os


def getDataFromTxt(filePath):
    result = {}
    value = []
    hand = open(filePath)
    filename = os.path.basename(filePath)
    result['username'] = filename.split('.')[0]
    for line in hand:
        line = line.rstrip().strip(' ')
        if re.search('^Processor:', line):
            result['Processor'] = line.split(':')[1].strip(' ')
        if re.search(r'^Memory:', line):
            result['Memory'] = line.split(':')[1].strip(' ')
        if re.search(r'System Model: ', line):
            result['System_model'] = line.split(':')[1].strip(' ')
        if re.search(r'^Card name:', line):
            result['Display_card'] = line.split(':')[1].strip(' ')
        if re.search(r'^Monitor Model: ', line):
            value.append(line.split(':')[1].strip(' '))
            result['Monitor'] = value
        if re.search(r'^Display Memory:', line):
            result['Display_memory'] = line.split(': ')[1]
        if re.search(r'^Model:(.*)?(WDC|ST\d+)', line):
            result['Disk_model'] = line.split(': ')[1]
    return result


def fromDictToCSV(message):

    headings = ['username', 'System_model', 'Disk_model', 'Monitor', 'Display_card',
                'Memory', 'Display_memory', 'Processor']
    myDictData = message
    try:
        myFilePath = './MyDictionary.csv'
        with open(myFilePath, 'w') as myCSVFile:
            csvWriter = csv.DictWriter(myCSVFile, fieldnames=headings, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
            csvWriter.writeheader()
            for data in myDictData:
                csvWriter.writerow(data)
    except IOError as (errno, strerror):
        print("I/O error({0}): {1}".format(errno, strerror))

    return


def get_filepaths(directory):
    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths


if __name__ == '__main__':
    result = []
    path = raw_input("输入文件路径: ")
    full_file_paths = get_filepaths(path)
    for fileAbsPath in full_file_paths:
        Dict = getDataFromTxt(fileAbsPath)
        result.append(Dict)
    fromDictToCSV(result)
