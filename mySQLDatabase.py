from secrets import connectStr
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


def SUBMISSIONS_createSubmission(submissionId: int, submissionUserId: int, submissionProblemId: int, submissionCode: str, submissionOutput: str, submissionStatus: int, submissionCompiler: str) -> None:
    submissionCode = json.dumps(submissionCode)
    submissionCode = submissionCode.replace("'", "''")

    submissionOutput = json.dumps(submissionOutput)
    submissionOutput = submissionOutput.replace("'", "''")

    executeCommandCommit(f"INSERT INTO {DATABASE_SUBMISSIONS} (SubmissionID, SubmissionUserID, SubmissionProblemID, SubmissionCode, SubmissionOutput, SubmissionStatus, SubmissionCompiler) VALUES ({str(submissionId)}, {str(submissionUserId)}, {str(submissionProblemId)}, '{submissionCode}', '{submissionOutput}', {str(submissionStatus)}, '{submissionCompiler}')")


def SUBMISSIONS_getSubmissionString(submissionId: int):
    arr = executeCommandFetchAll(f"SELECT SubmissionID, SubmissionUserID, SubmissionProblemID, SubmissionCode, SubmissionStatus, SubmissionCompiler FROM {DATABASE_SUBMISSIONS} WHERE SubmissionID={str(submissionId)}")

    for i in range(len(arr)):
        arr[i][0] = str(arr[i][0])
        arr[i][1] = str(arr[i][1])
        arr[i][2] = str(arr[i][2])
        arr[i][3] = json.loads(arr[i][3])

    return arr


if __name__ == "__main__":
    # print(ACCOUNT_getUniqueIDNumber())

    # print(PROBLEMS_getProblemsListString())
    # print(PROBLEMS_getProblemString(1))

    # print("'" == "\'")

    SUBMISSIONS_createSubmission(3, 2, 3, """this is a test statement
    
    
    




































































































































    \'  \' ' ' '' \" \"""", "out", 1200, "python3")
    print(SUBMISSIONS_getSubmissionString(3))

    # ACCOUNT_createAccount("Danny", "Kaja")

    # a = executeCommandFetchAll(f"SELECT TOP (1000) * FROM {DATABASE_USERACCOUNTS}")
    # print(a)
