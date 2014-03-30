import flask as fl
app = fl.Flask(__name__, static_folder='static',template_folder='templates')

@app.route("/")
def serve_base():
    """Serve basic-page scaffolding with javascript"""
    return fl.render_template('base.html.template')

if __name__ == "__main__":
    app.run(debug=True)