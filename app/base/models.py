# -*- encoding: utf-8 -*-
from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, DateTime
from app import db, login_manager
from app.base.util import hash_pass


class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


class Properties(db.Model):
    __tablename__ = 'Properties'
    propertyId = Column(Integer, primary_key=True)
    bedrooms = Column(Integer)
    bathrooms = Column(Integer)
    carSpaces = Column(Integer)
    floorAreaM2 = Column(Integer)
    landAreaM2 = Column(Integer)
    propertyType = Column(String)
    saleDate = Column(DateTime)
    salePrice = Column(Integer)
    valuationDate = Column(DateTime)
    yearBuilt = Column(DateTime)

class Address(db.Model):
    __tablename__ = 'Address'
    property_id = db.Column(Integer, db.ForeignKey('Properties.propertyId'), primary_key=True)
    address = Column(String)
    street = Column(String)
    suburb = Column(String)
    state = Column(String)
    postcode = Column(Integer)

class Ownership(db.Model):
    __tablename__ = 'Ownership'
    id = Column(Integer, primary_key=True)
    user_id = db.Column(Integer, db.ForeignKey('User.id'))
    property_id = db.Column(Integer, db.ForeignKey('Properties.propertyId'))

@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
