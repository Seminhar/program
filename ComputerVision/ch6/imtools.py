# -*- coding: utf-8 -*-
"""
Created on Fri Jan 19 16:16:46 2018

@author: kaisya
"""

import os
def get_imlist(path):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]