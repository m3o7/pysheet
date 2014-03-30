import flask as fl
import json
from pys.project import Project
from pys.table import Table

app = fl.Flask(__name__, static_folder='static',template_folder='templates')

def return_json(data):
    """Return flask-response with JSON header - convienience function"""
    return fl.Response( response=json.dumps(data), 
                        status=200,
                        mimetype="application/json")

@app.route('/')
def serve_base():
    """Return basic-page scaffolding with javascript"""
    return fl.render_template('base.html.template')

@app.route('/projects')
def list_projects():
    """Return all projects as JSON"""
    projects = [p.name for p in Project.all]
    return return_json( projects )

@app.route('/create_project/<name>', methods=['POST'])
def create_project(name):
    """Create a new project and return its name"""
    project = Project.create_new_project(name=name)
    return return_json( project.serialized )

@app.route('/project/<name>')
def list_tables(name):
    tables = [t.serialized for t in Project.get(name=name).tables]
    return return_json( tables )

@app.route('/project/<project>/create_table/<table>', methods=['POST'])
def create_table(project, table):
    table = Table.create_new_table(package_name=project, table_name=table)
    return return_json( table )

if __name__ == "__main__":
    app.run(debug=True)
