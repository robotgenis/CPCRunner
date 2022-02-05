from flask import Flask, send_from_directory, render_template, abort, request
import mySQLDatabase
import myCompiler

app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')


@app.errorhandler(404)
def error_404(e):
    return render_template("errors/error404.jade"), 404


@app.errorhandler(500)
def error_500(e):
    return render_template("errors/error404.jade"), 500


@app.route('/public/<path:path>')
def public(path):
    return send_from_directory('public', path)


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


@app.route('/problem/<path:path>', methods=['get'])
def problemPage(path):
    arr = mySQLDatabase.PROBLEMS_getProblemString(int(path))

    if len(arr) == 0:
        return abort(404)

    prob = arr[0]

    prob[5] = zip(prob[5].split("\\r"), prob[6].split("\\r"))

    return render_template("problems/problemPage.jade", problem=prob)


@app.route("/submission/<path:path>", methods=['get'])
def submissionPage(path):
    arr = mySQLDatabase.PROBLEMS_getProblemNameString(int(path))

    if len(arr) == 0:
        return abort(404)

    return render_template("/problems/submission.jade", problem=arr[0], compilers=myCompiler.compilerConstants.COMPILERS_PUBLIC)


@app.route("/submission/<path:path>", methods=['post'])
def submit(path):
    id = int(path)

    compiler = request.form['compiler']

    code = request.form['code']

    print(id, compiler, code)

    return "Done"
