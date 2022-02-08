from mySecrets import connectStr
import json
import pyodbc

DATABASE_USERACCOUNTS = "[dbo].[UserAccounts]"
DATABASE_PROBLEMS = "[dbo].[Problems]"
DATABASE_SUBMISSIONS = "[dbo].[Submissions]"


def executeCommandCommit(cmd: str) -> None:
    cnxn = pyodbc.connect(connectStr)
    cursor = cnxn.cursor()
    cursor.execute(cmd)
    cursor.commit()
    cnxn.close()


def executeCommandFetchAll(cmd: str) -> list:
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


def PROBLEMS_getProblemString(problemID: int) -> list:
    arr = executeCommandFetchAll(f"SELECT ProblemID, ProblemName, ProblemDescription, ProblemInput, ProblemOutput, ProblemExampleInput, ProblemExampleOutput, TimeLimit, MemoryLimit, Difficulty FROM {DATABASE_PROBLEMS} WHERE ProblemID={str(problemID)}")

    for i in range(len(arr)):
        arr[i][0] = str(arr[i][0])
        arr[i][7] = str(arr[i][7])
        arr[i][8] = str(arr[i][8])
        arr[i][9] = str(arr[i][9])
        for k in range(len(arr[i])):
            arr[i][k] = arr[i][k].replace("\\n", "\n")

    return arr


def PROBLEMS_getProblemNameString(problemID: int) -> list:
    arr = executeCommandFetchAll(f"SELECT ProblemID, ProblemName FROM {DATABASE_PROBLEMS} WHERE ProblemID={str(problemID)}")

    for i in range(len(arr)):
        arr[i][0] = str(arr[i][0])

    return arr


def PROBLEMS_getProblemTest(problemID: int) -> list:
    arr = executeCommandFetchAll(f"SELECT ProblemID, ProblemRunInput, ProblemRunOutput, ProblemRunCheckFunction, TimeLimit, MemoryLimit, Difficulty FROM {DATABASE_PROBLEMS} WHERE ProblemID={str(problemID)}")

    for i in range(len(arr)):
        for k in range(1, 3):
            arr[i][k] = arr[i][k].replace("\\n", "\n")

    return arr


def SUBMISSIONS_getUniqueIDNumber() -> int:
    return executeCommandFetchAll(f"SELECT MAX(submissionId) FROM {DATABASE_SUBMISSIONS}")[0][0] + 1


def SUBMISSIONS_createSubmission(submissionUserId: int, submissionProblemId: int, submissionCompiler: str, submissionCode: str, submissionOutput: str, submissionStatus: int) -> str:
    submissionId = SUBMISSIONS_getUniqueIDNumber()

    submissionCode = json.dumps(submissionCode)
    submissionCode = submissionCode.replace("'", "''")

    submissionOutput = json.dumps(submissionOutput)
    submissionOutput = submissionOutput.replace("'", "''")

    executeCommandCommit(f"INSERT INTO {DATABASE_SUBMISSIONS} (SubmissionID, SubmissionUserID, SubmissionProblemID, SubmissionCompiler, SubmissionCode, SubmissionOutput, SubmissionStatus) VALUES ({str(submissionId)}, {str(submissionUserId)}, {str(submissionProblemId)}, '{submissionCompiler}', '{submissionCode}', '{submissionOutput}', {str(submissionStatus)})")

    return str(submissionId)


def SUBMISSIONS_getSubmissionString(submissionId: int):
    arr = executeCommandFetchAll(f"SELECT SubmissionID, SubmissionUserID, SubmissionProblemID, SubmissionCode, SubmissionStatus, SubmissionCompiler FROM {DATABASE_SUBMISSIONS} WHERE SubmissionID={str(submissionId)}")

    for i in range(len(arr)):
        arr[i][0] = str(arr[i][0])
        arr[i][1] = str(arr[i][1])
        arr[i][2] = str(arr[i][2])
        arr[i][3] = json.loads(arr[i][3])

    return arr


# if __name__ == "__main__":
#     # print(ACCOUNT_getUniqueIDNumber())

#     # print(PROBLEMS_getProblemsListString())
#     # print(PROBLEMS_getProblemString(1))

#     # print("'" == "\'")

#     SUBMISSIONS_createSubmission(2, 3, "python3", """Some cool code""", "out", 1500)
#     print(SUBMISSIONS_getSubmissionString(3))

#     # ACCOUNT_createAccount("Danny", "Kaja")

#     # a = executeCommandFetchAll(f"SELECT TOP (1000) * FROM {DATABASE_USERACCOUNTS}")
#     # print(a)
