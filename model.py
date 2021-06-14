import calculate
import pandas as pd


MAX_RESULT = 0
LIST = []


for i in range(28000 , 35000, 100):
	result = calculate.calculate(i , 0)
	if(result["MAX_FEES"]>MAX_RESULT):
		MAX_RESULT = result["MAX_FEES"]
		LIST = result["transactions"]
		if(i > 295164):
			break

print(MAX_RESULT)


with open('block.txt', 'w') as filehandle:
	for txn in LIST:
		filehandle.write('%s\n' % txn)