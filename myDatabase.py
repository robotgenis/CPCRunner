import json

database = {'problems':[{'name':'Problem A'}]}


def loadFileJson(fil:str):
	try:
		f = open(fil, "r")
		lines = f.readlines()
		f.close()
		return json.loads("".join(lines))
	except:
		return

def saveFileJson(fil:str, j):
	try:
		f = open(fil, "w")
		f.write(json.dumps(j))
		f.close()
	except:
		return

def saveDatabaseSection(name):
	if name in database:
		saveFileJson(name + ".json", database[name])

def loadDatabaseSection(name):
	database[name] = loadFileJson(name + ".json")

loadDatabaseSection('problems')
loadDatabaseSection('test')

a = database['problems']

database['problems'][0]['details'] = "something"

print(database)

saveDatabaseSection('problems')