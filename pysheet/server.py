import flask as fl
import json
from pys.project import Project
app = fl.Flask(__name__, static_folder='static',template_folder='templates')

@app.route('/')
def serve_base():
    """Return basic-page scaffolding with javascript"""
    return fl.render_template('base.html.template')

@app.route('/projects')
def serve_projects():
    """Return all projects as JSON"""
    projects = [p.json for p in Project.all]
    return fl.Response(
        response=json.dumps(projects), 
        status=200,
        mimetype="application/json")

if __name__ == "__main__":
    app.run(debug=True)