import os
import project as p

class MetaProject(type):
    """Metaclass for a project, which contains some convienience methods"""

    __ext__ = 'pys.proj'
    __path__ = '.'

    def __init__(cls, name, bases, dct):
        super(MetaProject, cls).__init__(name, bases, dct)

    @property
    def all(self):
        """Return all projects as generator"""
        # setup
        path = MetaProject.__path__
        files = os.listdir(path) 
        fullpath = lambda path, filename : os.path.join(path, filename)

        # filter the project folders
        projects = (_f for _f in files if os.path.isdir(fullpath(path, _f)))
        projects = (p for p in projects if p.endswith(MetaProject.__ext__))
        projects = (fullpath(path, p) for p in projects)
        projects = (p.Project(path=path) for path in projects)
        return projects

    def __create_new_project_folder__(self, name):
        """Create a new project path"""
        foldername = '{0}.{1}'.format(name, MetaProject.__ext__)
        path = os.path.join(MetaProject.__path__, foldername)
        os.mkdir(path)
        return path

    def create_new_project(self, name):
        """Create a new project (incl. folder structure) and return its
        object representation"""
        path = self.__create_new_project_folder__(name)
        return p.Project(path=path)
