#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """ The State class, contains state ID and name """
    __tablename__ = "states"

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade='all, delete')
    else:
        name = ""

        @property
        def cities(self):
            cities_list = []
            all_cities = models.storage.all(City).values()
            for cty in all_cities:
                if cty.state_id == self.id:
                    cities_list.append(cty)
            return (cities_list)
