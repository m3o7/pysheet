from meta_table import MetaTable
import inspect

class Table(object):
    
    __metaclass__ = MetaTable

    def execute(self):
        """Encapsulate run method"""
        return self.run()

    def get_run_source(self):
        """Return the source-code of the run-method"""
        source, _ = inspect.getsourcelines(self.run)
        return source

    def get_class_source(self):
        """Return the source-code of the entire class"""
        source, _ = inspect.getsourcelines(self.__class__)
        return source

    def run(self):
        """Stub, needs to be implemented by its sub-classes"""
        raise NotImplementedError
