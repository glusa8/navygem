from navygem.settings import BASE_DIR
import glob
import json
import os

class ResourceRegistrarMeta(type):
    file = __file__
    def __new__(cls, name, parents, dct):

        if 'types' in dct:
            files = {}
            for root, _, filenames in os.walk(os.path.dirname(os.path.realpath(cls.file))):
                for filename in filenames:
                    _, extention = os.path.splitext(filename)
                    if extention in dct['types']:
                        if filename not in files:
                            files[filename] = os.path.join(root, filename)
                        else:
                            raise Exception('Two resource files cannot be named the same name.')

            dct['files'] = files

        return super(ResourceRegistrarMeta, cls).__new__(cls, name, parents, dct)


class ResourceRegistrar(object):

    __metaclass__ = ResourceRegistrarMeta

    # Subclasses should override 'types' array.
    types = []

    @classmethod
    def find(cls, filename, loader):
        if filename in cls.files:
            _, extention = os.path.splitext(filename)
            if extention in cls.types:
                return loader(cls.files[filename])


def load_class(class_name):
    def load_from(file_full_path):
        _, extention = os.path.splitext(file_full_path)
        full_path = os.path.relpath(file_full_path, BASE_DIR)
        full_path_no_extention = full_path[:-len(extention)]
        module_name = full_path_no_extention.replace(os.sep, '.')
        # Why we use fromlist:
        # http://stackoverflow.com/a/2725668
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name)
    return load_from
