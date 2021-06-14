import pandas as pd
import numpy as np

MAX_WEIGHT = 4000000
TOTAL_WEIGTH = 0
MAX_FEES = 0
transactions = []
txn_waiting_for_parent = []
rows_to_remove = []
awaiting_parents = {}
parentsNeeded = {}

def calculate(x , y):
	print("Calculating " + str(x) + " of 295164")
	global TOTAL_WEIGTH , MAX_WEIGHT, MAX_FEES, transactions, txn_waiting_for_parent, rows_to_remove, awaiting_parents, parentsNeeded
	df = pd.read_csv('mempool.csv')
	test = df.sort_values('fee', ascending=False)
	test.fillna(value = 0, inplace = True)


	def addTnxToBlock(weight , fees , tx_id):
		global TOTAL_WEIGTH , MAX_WEIGHT, MAX_FEES, transactions, txn_waiting_for_parent
		if((TOTAL_WEIGTH + weight < MAX_WEIGHT)):
			transactions.append(tx_id)
			TOTAL_WEIGTH = TOTAL_WEIGTH + int(weight)
			MAX_FEES = MAX_FEES + int(fees)
			
			return True
		else:
			return False




	for index, row in test.iterrows():
		if((TOTAL_WEIGTH + row["weight"] < MAX_WEIGHT) and ((int(row["weight"]) < x) and (int(row["fee"]) > y))):
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
						txn_waiting_for_parent.append(row["tx_id"])
						if row["tx_id"] in awaiting_parents.keys():
							existingList = awaiting_parents[row["tx_id"]]
							existingList.append(parent)
							awaiting_parents[row["tx_id"]] = existingList
						else:
							awaiting_parents[row["tx_id"]] = [parent]
									
				if (allParentsProcessed):
					# All parent transactions has already occured. Proceed with transaction
					if(addTnxToBlock(row["weight"] , row["fee"] , row["tx_id"])):
						rows_to_remove.append(index)
						if(isParent):
							# This is a parent of a pending transaction
							for child in parentsNeeded[row["tx_id"]]:
								try:
									awaiting_parents[child].remove(row["tx_id"])
									if(len(awaiting_parents[child]) == 0):
										child_el = test.loc[test['tx_id'] == child]
										addTnxToBlock(child_el['weight'].item() , child_el['fee'].item() , child_el["tx_id"].item())
								except:
									pass
				else:
					pass
			else:
				if(addTnxToBlock(row["weight"] , row["fee"] , row["tx_id"])):
					rows_to_remove.append(index)
				if(isParent):
					# This is a parent of a pending transaction
					for child in parentsNeeded[row["tx_id"]]:
						try:
							awaiting_parents[child].remove(row["tx_id"])
							if(len(awaiting_parents[child]) == 0):
								child_el = test.loc[test['tx_id'] == child]
								addTnxToBlock(child_el['weight'].item() , child_el['fee'].item() , child_el["tx_id"].item())
						except:
							pass

	print("Block weight: "+str(TOTAL_WEIGTH))
	print("Fees: "+str(MAX_FEES))

	fees = MAX_FEES

	TOTAL_WEIGTH = 0
	transactions = []
	parentsNeeded = {}
	rows_to_remove = []
	awaiting_parents = {}
	txn_waiting_for_parent = []

	MAX_FEES = 0

	return {
		"MAX_FEES" : fees,
		"transactions" : transactions
	}
	
	

	# with open('block.txt', 'w') as filehandle:
	# 	for txn in transactions:
	# 		filehandle.write('%s\n' % txn)