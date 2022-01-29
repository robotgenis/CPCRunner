from dataclasses import dataclass
from urllib import response
from flask import Flask, request,send_from_directory, redirect, render_template
import myDatabase
import myCompiler

app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

@app.route('/public/<path:path>')
def send_public(path):
    return send_from_directory('public', path)

@app.route('/problem/<path:path>')
def send_problem(path):
    prob = myDatabase.getProblem(path)
    
    if not prob: return redirect("/")
    
    problems = myDatabase.getShownProblemsIDs()
    
    return render_template("problem.jade",visual=prob['visual'], problems=problems, id=prob['id'])

@app.route("/", methods=['get'])
def home():
    id = ""
    if("id" in request.args): 
        id = request.args['id']
    
    problems = myDatabase.getShownProblemsIDs()
    
    return render_template("index.jade", problems=problems, id=id)

@app.route("/submit", methods=['post'])
def submit():
    form = request.form.to_dict()
    
    compiler = form['compiler']
    problem = form['problem']
    code = form['code']
    
    print(compiler, problem, code)
    
    prob = myDatabase.getProblem(problem)
    
    if not prob: return "ERROR"
    
    compileProblem = myCompiler.problemFromDatebase(prob)
    
    sub = myCompiler.Submission(code, compiler, compileProblem)
    
    sub.createSubmission()
    
    return "Submitted: " + str(sub.results)

@app.route("/view", methods=['get'])
def submission():
    return "Hi"