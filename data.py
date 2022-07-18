import json

test = open('testTableData.json')
col = open('colModel.json')
line = open('testLineData.json')
bar = open('testBarData.json')

testBarData = json.load(bar)
testTableData = json.load(test)
colModel = json.load(col)
testLineData = json.load(line)