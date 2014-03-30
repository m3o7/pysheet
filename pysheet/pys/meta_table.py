import pkgutil
from collections import defaultdict
import project
import os

class MetaTable(type):

    __table_classes__ = defaultdict(set) # register all tables

    def __new__(meta, name, bases, dct):
        """Create a new table class instance and register it"""
        # create new table-class instance
        klass = super(MetaTable, meta).__new__(meta, name, bases, dct)
        # register the new table-(class) with its project-instance
        package_name, _ = klass.__module__.split('.')
        MetaTable.__table_classes__[package_name].add(klass)
        return klass

    def create_new_table(cls, package_name, table_name):
        """Create new table file"""
        path = project.Project.get(package_name).path
        filename = '{0}.py'.format(table_name)
        fullpath = os.path.join(path, filename)
        with open(fullpath, 'w') as table:
            pass
        return fullpath

    def import_tables(cls, package_name):
        """Return all tables of a module"""
        # reload the instances
        package = __import__( package_name )
        prefix = "{0}.".format( package.__name__ )
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            module = __import__( modname )
            # force reload all modules - in case something has changed
            reload(module)

        return MetaTable.__table_classes__[package_name]

    @property
    def name(cls):
        return cls.__name__

    @property
    def serialized(cls):
        return cls.name
