from secrets import connectStr
import pyodbc

DATABASE_USERACCOUNTS = "[dbo].[UserAccounts]"
DATABASE_PROBLEMS = "[dbo].[Problems]"


def executeCommandCommit(cmd: str):
    cnxn = pyodbc.connect(connectStr)
    cursor = cnxn.cursor()
    cursor.execute(cmd)
    cursor.commit()
    cnxn.close()


def executeCommandFetchAll(cmd: str):
    cnxn = pyodbc.connect(connectStr)
    cursor = cnxn.cursor()
    cursor.execute(cmd)
    arr = cursor.fetchall()
    cnxn.close()
    return arr


def ACCOUNT_getUniqueIDNumber() -> int:
    return executeCommandFetchAll(f"SELECT MAX(AccountID) FROM {DATABASE_USERACCOUNTS}")[0][0] + 1


def ACCOUNT_createAccount(firstName: str, lastName: str) -> None:
    id = ACCOUNT_getUniqueIDNumber()

    executeCommandCommit(f"INSERT INTO {DATABASE_USERACCOUNTS} VALUES ({id}, '{firstName}', '{lastName}')")


def PROBLEMS_getProblemsListString() -> list:
    arr = executeCommandFetchAll(f"SELECT ProblemID, ProblemName, Difficulty FROM {DATABASE_PROBLEMS}")

    for i in range(len(arr)):
        arr[i][0] = str(arr[i][0])
        arr[i][2] = str(arr[i][2])
    return arr


def PROBLEMS_getProblemString(id: int) -> list:
    arr = executeCommandFetchAll(f"SELECT ProblemID, ProblemName, ProblemDescription, ProblemInput, ProblemOutput, ProblemExampleInput, ProblemExampleOutput, TimeLimit, MemoryLimit, Difficulty FROM {DATABASE_PROBLEMS} WHERE ProblemID={str(id)}")

    for i in range(len(arr)):
        arr[i][0] = str(arr[i][0])
        arr[i][7] = str(arr[i][7])
        arr[i][8] = str(arr[i][8])
        arr[i][9] = str(arr[i][9])
        for k in range(len(arr[i])):
            arr[i][k] = arr[i][k].replace("\\n", "\n")

    return arr


if __name__ == "__main__":
    # print(ACCOUNT_getUniqueIDNumber())

    print(PROBLEMS_getProblemsListString())
    print(PROBLEMS_getProblemString(1))

    # ACCOUNT_createAccount("Danny", "Kaja")

    # a = executeCommandFetchAll(f"SELECT TOP (1000) * FROM {DATABASE_USERACCOUNTS}")
    # print(a)
