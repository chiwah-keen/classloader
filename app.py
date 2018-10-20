# -*- coding: utf-8 -*-


import os, sys, unittest, traceback, inspect, pyclbr

import unittestcase.test_api_cases


def classLoder(module_path):

    module_name = "unittestcase.test_api_cases"

    __import__(module_name)

    the_module = sys.modules[module_name]
    for cls in dir(the_module):
        if cls.startswith("__") and cls.endswith("__"):
            continue
        f = getattr(the_module, cls)
        for func in dir(f):
            if func.startswith("__") and func.endswith("__"):
                continue
            print (func)
        print ("import module class success!")


classLoder("./unittestcase")

