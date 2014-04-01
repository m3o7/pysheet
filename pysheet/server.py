import flask
import json
from pys.project import Project
from pys.table import Table

app = flask.Flask(__name__, static_folder='static',template_folder='templates')

def return_data(data, mimetype):
    """Return flask-response with custom header - convienience function"""
    return flask.Response(  response=data, 
                            status=200,
                            mimetype=mimetype)

def return_json(data):
    """Return respone with JSON header"""
    return return_data(data=json.dumps(data), mimetype="application/json")

@app.route('/')
def serve_base():
    """Return basic-page scaffolding with javascript"""
    return app.send_static_file('index.html')

@app.route('/projects')
def list_projects():
    """Return all projects as JSON"""
    projects = [p.name for p in Project.all]
    return return_json( projects )

@app.route('/create_project/<name>', methods=['POST'])
def create_project(name):
    """Create a new project and return its name"""
    project = Project.create_new_project(name=name)
    return project.serialized

@app.route('/project/<name>')
def list_tables(name):
    tables = [t.serialized for t in Project.get(name=name).tables]
    return return_json( tables )

@app.route('/project/<project>/_create_table/<table>', methods=['POST'])
def create_table(project, table):
    table = Table.create_new_table(package_name=project, table_name=table)
    return return_json( table )

def __get_table_method_source__(project, table, method):
    table = Project.get(name=project).get_table(name=table)
    return table().get_source(method=method)

@app.route('/project/<project>/<table>/_source/<method>')
def get_table_method_source(**kwargs):
    return return_data( data=__get_table_method_source__(**kwargs), 
                        mimetype='text/x-script.phyton')

@app.route('/project/<project>/<table>/_update_source/<method>', methods=['POST'])
def update_table_method_source(project, table, method):
    _table = Project.get(name=project).get_table(name=table)
    new_source = flask.request.data
    # cleaning the source
    new_source = new_source.strip()
    _table().update_source(new_source=new_source, method=method)
    # reload the data and serve it - to verify that the changes took effect
    return '\n'.join(__get_table_method_source__(project=project, table=table, method=method))

@app.route('/project/<project>/<table>/_source')
def get_table_source(project, table):
    table = Project.get(name=project).get_table(name=table)
    return return_data( data=table().get_source(), 
                        mimetype='text/x-script.phyton')

@app.route('/project/<project>/<table>/_update_source', methods=['POST'])
def update_table_source(project, table):
    _table = Project.get(name=project).get_table(name=table)
    new_source = flask.request.data
    # cleaning the source
    new_source = new_source.strip()
    _table().update_source(new_source=new_source)
    return '\n'.join(__get_table_method_source__(project=project, table=table))

@app.route('/project/<project>/<table>/<method>')
def execute_table_method(project, table, method):
    table = Project.get(name=project).get_table(name=table)
    table = table()
    func = getattr(table, method)
    try:
        return return_json( func() )
    except TypeError:
        #  in case there was a generator returned
        return return_json( list(func()) )


if __name__ == "__main__":
    app.run(debug=True)
