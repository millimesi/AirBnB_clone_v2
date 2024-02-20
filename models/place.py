#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id'),
                             primary_key=True, nullable=False)
                      )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    if getenv("HBNB_TYPE_STORAGE") == 'db':
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(120), nullable=False)
        description = Column(String(1024), nullable='True')
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        reviews = relationship('Review', backref='place',
                               cascade='all, delete-orphan')
        amenities = relationship('Amenity', secondary='place_amenity',
                                 viewonly=False,
                                 back_populates='place_amenities')

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """
            Getter attribute that returns the list of Review instances with
            place_id equals to the current Place.id
            """
            from models import storage
            all_reviews = storage.all("Review").values()
            return [review for review in all_reviews
                    if review.place_id == self.id]

        @property
        def amenities(self):
            """
            Getter attribute that returns the list of Amenity instances based
            on the attribute amenity_ids that contains all Amenity.id linked
            to the Place
            """
            return [storage.all("Amenity").get(amenity_id)
                    for amenity_id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """
            Setter attribute that handles append method for adding an
            Amenity.id to the attribute amenity_ids. This method should
            accept only Amenity object, otherwise, do nothing.
            """
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
