#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""

from models.amenity import Amenity
from models.base_model import Base, BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """This class manages storage of hbnb models in a database"""

    __engine = None
    __session = None

    def __init__(self):
        """ Initialize DBStorage """

        usr = getenv("HBNB_MYSQL_USER")
        psswd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        dtbs = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")
        url = "mysql+mysqldb://{}:{}@{}/{}".format(usr, psswd, host, dtbs)
        self.__engine = create_engine(url, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the curret database session all objects of the given class.

        If cls is None, queries all types of objects.

        Return:
            Dict of queried classes, format: <class name>.<obj id> = obj.
        """
        if not cls:  # create new SQL query object & make object list of tables.
            qry_obj = self.__session.query(Amenity)
            qry_obj.extend(self.__session.query(City))
            qry_obj.extend(self.__session.query(Place))
            qry_obj.extend(self.__session.query(Review))
            qry_obj.extend(self.__session.query(State))
            qry_obj.extend(self.__session.query(User))
        else:
            qry_obj = qry_obj = self.__session.query(cls)

        result = {'{}.{}'.format(type(obj).__name__, obj.id):
                      obj for obj in qry_obj}
        return (result)

    def new(self, obj):
        """ Adds an objet to the current db session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes 'obj' from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database """
        Base.metadata.create_all(self.__engine)

        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
