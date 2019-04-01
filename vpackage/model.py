# pylint: disable-msg=C0103
# '''the models'''
from vpackage import db,login_manager

from flask_login import UserMixin

import json
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Customer.get(id)


customer_orders = db.Table('customer_orders',
    db.Column('customer_id', db.Integer, db.ForeignKey('customer.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.prod_id'), primary_key=True)
)


class Allstates(db.Model):
    __tablename__ = 'allstates'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    state_name = db.Column(db.String(50), nullable=False)
    #define relationship
    hostels = db.relationship('Hostel', backref='states', cascade="all, delete-orphan")

class Hostel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hostel_name = db.Column(db.String(50), nullable=False)
    hostel_state = db.Column(db.Integer, db.ForeignKey('allstates.id'))
    hostel_desc= db.Column(db.String(50), nullable=False)

    #def __repr__(self):
    #    return json.dumps(self.__dict__)

    
class Product(db.Model): 
    prod_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    product_name = db.Column(db.String(64))
    product_price = db.Column(db.String(120))
    
    # create a Foreign Key Column
   
    product_category = db.Column(db.Integer(), db.ForeignKey('category.id'))
    #create relationship
    transactions = db.relationship('Transaction', backref='product', cascade="all, delete-orphan")


class Category(db.Model):
    ''' The Parent Class, we only define relationship here '''
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    # the relationship can be used to retrieve many instances of the child class
    products = db.relationship('Product', backref='category', cascade="all, delete-orphan")

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_name = db.Column(db.String(50), nullable=False)
    admin_email = db.Column(db.String(50), nullable=False)
    admin_user = db.Column(db.String(50), nullable=False)
    admin_pass = db.Column(db.String(50), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    trans_prod_id = db.Column(db.Integer, db.ForeignKey('product.prod_id'), nullable=False)
    trans_ref = db.Column(db.String(100), nullable=False)
    trans_status = db.Column(db.Integer, nullable=False) 
    trans_amt = db.Column(db.Float, nullable=False)
    trans_date = db.Column(db.Date, default=datetime.utcnow)
    trans_type = db.Column(db.String(100), nullable=False)

class Customer(db.Model):
    ''' The Parent Class, we only define relationship here '''
    id = db.Column(db.Integer, primary_key=True)
    cust_name = db.Column(db.String(50), nullable=False)
    cust_email = db.Column(db.String(50), nullable=False)
    cust_phone = db.Column(db.String(50), nullable=False)

    #relationship
    transactions = db.relationship('Transaction', backref='customer', cascade="all, delete-orphan")

    
#Sam's db
class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(50), nullable=False)
    #define the relationships

    from_user = db.relationship('Messages', foreign_keys='Messages.from_id', backref='fromuser')
    to_user = db.relationship('Messages', foreign_keys='Messages.to_id', backref='touser')


class Messages(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    from_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    to_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    message_text = db.Column(db.String(100), nullable=False)
    message_status = db.Column(db.String(100), nullable=False)
    date_sent = db.Column(db.DateTime(), default=datetime.utcnow)

   
    
# End Sam's db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500))
    datesent = db.Column(db.DateTime(), default=datetime.utcnow)
    msg_status = db.Column(db.String(50), nullable=False)