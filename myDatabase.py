import json
import os

database = {}

DATABASE_PATH = os.path.join(os.getcwd(),"database")

SECTION_PROBLEMS = "problems"

def loadFileJson(name:str):
    fil = os.path.join(DATABASE_PATH, name + ".json")
    print(fil)
    try:
        f = open(fil, "r")
        lines = f.readlines()
        f.close()
        return json.loads("".join(lines))
    except:
        return

def saveFileJson(name:str, j):
    fil = os.path.join(DATABASE_PATH, name + ".json")
    try:
        f = open(fil, "w")
        f.write(json.dumps(j))
        f.close()
    except:
        return

def saveDatabaseSection(name:str):
    if name in database:
        saveFileJson(name, database[name])

def loadDatabaseSection(name:str):
    database[name] = loadFileJson(name)

def getSection(name:str):
    if name in database:
        return database[name]
    return

def loadDatabasePath(path:str):
    f = []
    for (dirpath, dirnames, filenames) in os.walk(os.path.join(DATABASE_PATH, path)):
        print(dirpath, dirnames, filenames)
        f.extend(filenames)
        break
    for i in f:
        loadDatabaseSection(os.path.join(path, "".join(i.split(".")[:-1])))

def getProblem(id:str):
    problems = getSection(SECTION_PROBLEMS)
    if not problems: return
    
    for prob in problems:
        if prob['id'] == id:
            return prob
        
def getShownProblemsIDs():
    problems = getSection(SECTION_PROBLEMS)
    
    if not problems: return []
    
    ids = []
    
    for prob in problems:
        if prob['shown']:
            ids.append(prob['id'])
    
    return ids
        


loadDatabasePath("")
loadDatabasePath("accounts")


if __name__ == "__main__":
    print(database)
    print(getProblem("a"))