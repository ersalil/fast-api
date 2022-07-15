import json

test = open('testTableData.json')
col = open('colModel.json')
line = open('testLineData.json')

testTableData = json.load(test)
colModel = json.load(col)
testLineData = json.load(line)