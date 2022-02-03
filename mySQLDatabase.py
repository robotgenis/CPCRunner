from secrets import connectStr
import pyodbc

cnxn = pyodbc.connect(connectStr)
cursor = cnxn.cursor()

DATABASE_USERACCOUNTS = "[dbo].[UserAccounts]"
DATABASE_PROBLEMS = "[dbo].[Problems]"

def executeCommandCommit(cmd:str):
    cursor.execute(cmd)
    cursor.commit()
    
def executeCommandFetchAll(cmd:str):
    cursor.execute(cmd)
    return cursor.fetchall()

def ACCOUNT_getUniqueIDNumber() -> int:
    return executeCommandFetchAll(f"SELECT MAX(AccountID) FROM {DATABASE_USERACCOUNTS}")[0][0] + 1

def ACCOUNT_createAccount(firstName:str, lastName:str) -> None:
    id = ACCOUNT_getUniqueIDNumber()
    
    executeCommandCommit(f"INSERT INTO {DATABASE_USERACCOUNTS} VALUES ({id}, '{firstName}', '{lastName}')")

def PROBLEMS_getProblemsInfo() -> list:
    arr = executeCommandFetchAll(f"SELECT ProblemID, ProblemName, ProblemDescription, ProblemInput, ProblemOutput, ProblemExampleInput, ProblemExampleOutput, TimeLimit, MemoryLimit FROM {DATABASE_PROBLEMS}")
    #change nubmers to string
    for i in range(len(arr)):
        arr[i][7] = str(arr[i][7])
        arr[i][8] = str(arr[i][8])
    return arr

if __name__=="__main__":
    # print(ACCOUNT_getUniqueIDNumber())

    print(PROBLEMS_getProblemsInfo())

    # ACCOUNT_createAccount("Danny", "Kaja")

    # a = executeCommandFetchAll(f"SELECT TOP (1000) * FROM {DATABASE_USERACCOUNTS}")
    # print(a)
