# -*- coding: utf-8 -*-


import os, sys

BUILDINFUNCTIONS = ["unittest"]


class ClassDiscover(object):

    def __init__(self, module_path, file_prefix, method_prefix):
        self.module_path = module_path
        self.file_prefix = file_prefix
        self.method_prefix = method_prefix
        self.module_files = []
        self.module_names = []
        self.test_suite = []

    def discover_module_files(self, module_path=None, pattern="test"):
        if not module_path or not os.path.isdir(module_path):
            module_path = self.module_path
        for subdir in os.listdir(module_path):
            if str(subdir).startswith("__init__"):
                continue
            if str(subdir).endswith(".py") and pattern in subdir:
                self.module_files.append(os.path.join(module_path, subdir))
                continue
            if os.path.isdir(os.path.join(module_path, subdir)) \
                    and not subdir.startswith("__"):
                self.discover_module_files( os.path.join(module_path, subdir))
        return self.module_files

    def get_module_name(self, file_path, module_path=None):
        if not os.path.isabs(file_path):
            raise TypeError("module name must be abs path.")
        if module_path is None:
            module_path = self.module_path
        curr_path = os.path.dirname(module_path)
        module_name = os.path.splitext(file_path.replace(curr_path, ""))[0]
        return module_name.replace(os.path.sep, ".")[1:]

    def get_all_modules(self, files):
        for f in files:
            module_name = self.get_module_name(f)
            self.module_names.append(module_name)

    def import_modules(self, module_list=None):
        if not module_list:
            module_list = self.module_names
        for module_name in module_list:
            try:
                __import__(module_name)
            except ImportError:
                raise ImportError("module %s can not be imported" % module_name)

    def get_class_name(self):
        for module_name in self.module_names:
            module = sys.modules[module_name]
            for classz_name in dir(module):
                if classz_name.startswith("__"): continue
                if classz_name in BUILDINFUNCTIONS: continue
                clazz = getattr(module, classz_name)
                method_list = self.get_method_name(clazz, self.method_prefix)
                for method in method_list:
                    self.test_suite.append(clazz(method))

    def get_method_name(self, clazz_obj, method_prefix):
        method_list = []
        for clazz_method in dir(clazz_obj):
            if clazz_method.startswith("__"): continue
            if method_prefix in clazz_method:
                method_list.append(clazz_method)
        return method_list

    def discover(self):
        files = self.discover_module_files(pattern=self.file_prefix)
        self.get_all_modules(files)
        self.import_modules()
        self.get_class_name()
        return self.test_suite

#discover("/Users/datagrand/test/classloader/unittestcase", 'test', 'test_')
a = ClassDiscover("/Users/datagrand/test/classloader/unittestcase", "test", "test")
print a.discover()
