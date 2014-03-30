from meta_project import MetaProject

class Project(object):
    """Represents a Project with all its tables"""

    __metaclass__ = MetaProject

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return '<{0}: {1}>'.format(self.path)

    @property
    def json(self):
        return self.path