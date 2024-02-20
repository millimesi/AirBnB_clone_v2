#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        name = Column(String(128), nullable=False)

        cities = relationship("City", backref="state", cascade="all, delete")
    else:
        name = ""

    @property
    def cities(self):
        """
        Getter attribute to return a list of City instances with
        state_id equal to the current State.id
        """
        from models import storage
        city_instances = storage.all(City)
        matching_cities = [city for city in city_instances.values()
                           if city.state_id == self.id]
        return matching_cities
