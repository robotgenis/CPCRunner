import pyodbc
from secrets import connectStr

cnxn = pyodbc.connect(connectStr)
cursor = cnxn.cursor()

cursor.execute("SELECT TOP (1000) * FROM [dbo].[UserAccounts]")
row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()