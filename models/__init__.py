#!/usr/bin/python3
"""This module instantiates an object of class FileStorage

-> If the environmental variable 'HBNB_TYPE_STORAGE' is set to 'db':
instantiates a database storage engine (DBStorage).
-> Else: instantiates a file storage engine (FileStorage).
"""

from os import getenv


if getenv("HBNB_TYPE_STORAGE") == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()  # use database
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()  # use 'file.json'

storage.reload()
