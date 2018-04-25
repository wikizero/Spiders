# coding:utf-8
from pymongo import MongoClient


def save(data):
    try:
        conn = MongoClient()
        db = conn.jobs
        my_set = db.mycol
        my_set.insert(data)
    except Exception, e:
        print e
