from flask import Flask, request,send_from_directory, redirect, render_template

app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

@app.route('/public/<path:path>')
def send_public(path):
    return send_from_directory('public', path)

@app.route('/problem/<path:path>')
def send_problem(path):
    return render_template("problems/" + path + ".jade")

@app.route("/", methods=['get'])
def home():
    return render_template("index.jade")

@app.route("/submit", methods=['post'])
def submit():
    form = request.form.to_dict()
    return "Submitted: " + str(form)

@app.route("/view", methods=['get'])
def submission():
    return "Hi"