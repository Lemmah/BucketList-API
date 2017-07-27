# app loads configurations here from the config file
from app import app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://bucketlist_api:easyPassword@localhost:5432/bucketlist_app"

db = SQLAlchemy(app)


class User(db.Model):
    ''' A model of the User Table '''
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(60))
    password = db.Column(db.String(256))
    secure_id = db.Column(db.String(60), unique=True)


class BucketList(db.Model):
    ''' A model of the BucketList Table '''
    bucketlist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    description = db.Column(db.String(100))
    # foreign key to user: from User.secure_id
    user_sid = db.Column(db.String(60))
    secure_id = db.Column(db.String(60), unique=True)


class BucketListItem(db.Model):
    ''' A model of the BucketListItem Table '''
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    category = db.Column(db.String(30))
    description = db.Column(db.String(100))
    # foreign key to bucketlist: from Bucketlist.secure_id
    bucketlist_sid = db.Column(db.String(60), unique=True)

