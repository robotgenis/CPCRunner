from dataclasses import dataclass
from urllib import response
from flask import Flask, request, send_from_directory, redirect, render_template
import mySQLDatabase
import myCompiler

app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

@app.route('/public/<path:path>')
def send_public(path):
    return send_from_directory('public', path)

# @app.route("/submission", methods=['get'])
# def submission():
#     id = ""
#     if("id" in request.args): 
#         id = request.args['id']
    
#     problems = myDatabase.getShownProblemsIDs()
    
#     return render_template("submission.jade", problems=problems, id=id)
    
#basic pages
@app.route("/", methods=['get'])
def home():
    return render_template("pages/index.jade")

@app.route("/login", methods=['get'])
def login():
    return render_template("pages/login.jade")
    

@app.route('/about', methods=['get'])
def about():
    return render_template("pages/about.jade")


@app.route('/problems', methods=['get'])
def problems():
    arr = mySQLDatabase.PROBLEMS_getProblemsListString()
    
    return render_template("problems/problems.jade", problems=arr)

@app.route('/problem/<path:path>')
def send_problem(path):
    arr = mySQLDatabase.PROBLEMS_getProblemString(int(path))
    
    if len(arr) == 0: return redirect("/")
    
    return render_template("problems/problemPage.jade", problem=arr[0])

# @app.route("/submit", methods=['post'])
# def submit():
#     form = request.form.to_dict()
    
#     compiler = form['compiler']
#     problem = form['problem']
#     code = form['code']
    
#     print(compiler, problem, code)
    
#     prob = myDatabase.getProblem(problem)
    
#     if not prob: return "ERROR"
    
#     compileProblem = myCompiler.problemFromDatebase(prob)
    
#     sub = myCompiler.Submission(code, compiler, compileProblem)
    
#     sub.createSubmission()
    
#     return "Submitted: " + str(sub.results)