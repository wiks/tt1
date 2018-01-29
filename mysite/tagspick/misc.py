# -*- coding: utf-8 -*-
import os
import sys

def req_as_dict():

    requirements = ["Python==" + ".".join(map(str, sys.version_info[:3]))]
    file = open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'requirements.txt'), 'r')
    for line in file:
        requirements.append(line)
    file.close()
    return requirements
