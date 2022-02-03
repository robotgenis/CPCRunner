from secrets import connectStr
import pyodbc

cnxn = pyodbc.connect(connectStr)
cursor = cnxn.cursor()

def executeCommandFetchAll(cmd:str):
    cursor.execute(cmd)
    
    return cursor.fetchall()

a = executeCommandFetchAll("SELECT TOP (1000) * FROM [dbo].[Persons]")
print(a)
