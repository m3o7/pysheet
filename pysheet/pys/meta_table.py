import pkgutil
import table as t
from collections import defaultdict

class MetaTable(type):

    __table_classes__ = defaultdict(set) # register all tables

    def __new__(meta, name, bases, dct):
        """Create a new table class instance and register it"""
        module, _ = dct['__module__'].split('.')
        # create new table-class instance
        klass = super(MetaTable, meta).__new__(meta, name, bases, dct)
        # register the new table-(class) with its project-instance
        package_name, _ = klass.__module__.split('.')
        try:
            MetaTable.__table_classes__[package_name].add(klass)
        except AttributeError as err:
            # Table class has no corresponding project
            pass
        return klass

    @property
    def all(cls):
        return MetaTable.__table_classes__

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
