from secrets import connectStr
import pyodbc

cnxn = pyodbc.connect(connectStr)
cursor = cnxn.cursor()

DATABASE_USERACCOUNTS = "[dbo].[UserAccounts]"

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

if __name__=="__main__":
    # print(ACCOUNT_getUniqueIDNumber())

    ACCOUNT_createAccount("Danny", "Kaja")

    a = executeCommandFetchAll(f"SELECT TOP (1000) * FROM {DATABASE_USERACCOUNTS}")
    print(a)
