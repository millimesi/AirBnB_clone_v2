#!/usr/bin/python3
"""DBStorage engine"""

import os
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect


class DBStorage:
    """DBStorage engine class"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialization"""
        user = os.environ.get('HBNB_MYSQL_USER')
        password = os.environ.get('HBNB_MYSQL_PWD')
        host = os.environ.get('HBNB_MYSQL_HOST', 'localhost')
        database = os.environ.get('HBNB_MYSQL_DB')

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}"
                                      .format(user, password, host, database),
                                      pool_pre_ping=True)
        if os.environ.get('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        objects_types = [User, State, City, Amenity, Place, Review]
        result = {}

        if cls is None:
            for obj_type in objects_types:
                query = self.__session.query(obj_type)
                # print(query)
                for obj in query.all():
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    result[key] = obj
                    # print("Object:", obj)
        else:
            queries = self.__session.query(cls)
            # print(queries)
            # print("Entering loop")
            for obj in queries.all():
                # print(obj)
                class_name = obj.__class__.__name__
                object_id = obj.id
                key = '{}.{}'.format(class_name, object_id)
                # print("Class Name:", class_name)
                # print("Object ID:", object_id)
                # print(key)
                result[key] = obj

        return result

    def new(self, obj):
        """add the object to the current database session (self.__session)"""
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session
        (self.__session)
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Creates all tables in the database.
        Create the current database session (self.__session)
        from the engine (self.__engine) by using a sessionmaker
        """

        # Creates all tables in the database
        Base.metadata.create_all(self.__engine)

        # Create the current database session from the engine
        # Used scoped_session to ensure the session is thread-safe.
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def close(self):
        """Close query"""
        self.__session.close()
