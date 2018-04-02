#!/usr/bin/python
#coding:utf-8

from distutils.core import setup
import py2exe

option = {"pyexe": {"compressed": 1, "optimize": 2, "bundle_files": 1}}

setup(
    options=option,
    zipfile=None,
    console=[{
        "script": "api_checkfile_excel.py",
        "icon_resources": [(1, "myicon.ico")]
    }])
