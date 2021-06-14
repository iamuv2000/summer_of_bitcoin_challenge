import pandas as pd
import numpy as np

MAX_WEIGHT = 4000000
TOTAL_WEIGTH = 0
MAX_FEES = 0
transactions = []
awaiting_parents = {}
parentsNeeded = {}

df = pd.read_csv('mempool.csv')
test = df.sort_values('fee', ascending=False)
test.fillna(value = 0, inplace = True)


def addTnxToBlock(weight , fees , tx_id):
	global TOTAL_WEIGTH , MAX_WEIGHT, MAX_FEES, transactions
	if((TOTAL_WEIGTH + weight < MAX_WEIGHT)):
		transactions.append(tx_id)
		TOTAL_WEIGTH = TOTAL_WEIGTH + int(weight)
		MAX_FEES = MAX_FEES + int(fees)
		
		return True
	else:
		return False




for index, row in test.iterrows():
	if((TOTAL_WEIGTH + row["weight"] < MAX_WEIGHT) and (row["weight"] < 33500)):
		isParent = False
		if(row["tx_id"] in parentsNeeded.keys()):
			# Parent is found
			isParent = True

		if(row["parents "] != 0):
			allParentsProcessed = True
			parents = row["parents "].split(';')

			for parent in parents:
				if(parent not in transactions):
					if parent in parentsNeeded.keys():
						parentsNeeded[parent].append(row["tx_id"])
					else:
						parentsNeeded[parent] = [row["tx_id"]]
					allParentsProcessed = False
					if row["tx_id"] in awaiting_parents.keys():
						existingList = awaiting_parents[row["tx_id"]]
						existingList.append(parent)
						awaiting_parents[row["tx_id"]] = existingList
					else:
						awaiting_parents[row["tx_id"]] = [parent]
								
			if (allParentsProcessed):
				# All parent transactions has already occured. Proceed with transaction
				if(addTnxToBlock(row["weight"] , row["fee"] , row["tx_id"])):
					if(isParent):
						# This is a parent of a pending transaction
						for child in parentsNeeded[row["tx_id"]]:
							awaiting_parents[child].remove(row["tx_id"])
							if(len(awaiting_parents[child]) == 0):
								child_el = test.loc[test['tx_id'] == child]
								addTnxToBlock(child_el['weight'].item() , child_el['fee'].item() , child_el["tx_id"].item())
			else:
				pass
		else:
			if(addTnxToBlock(row["weight"] , row["fee"] , row["tx_id"])):
				pass
			if(isParent):
				# This is a parent of a pending transaction
				for child in parentsNeeded[row["tx_id"]]:
					awaiting_parents[child].remove(row["tx_id"])
					if(len(awaiting_parents[child]) == 0):
						child_el = test.loc[test['tx_id'] == child]
						addTnxToBlock(child_el['weight'].item() , child_el['fee'].item() , child_el["tx_id"].item())

print("Block weight: "+str(TOTAL_WEIGTH))
print("Fees: "+str(MAX_FEES))


with open('block.txt', 'w') as filehandle:
	for txn in transactions:
		filehandle.write('%s\n' % txn)