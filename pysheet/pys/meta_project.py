import os
import project as p

class MetaProject(type):

    @property
    def all(self):
        """Return all projects"""
        return os.listdir('.')