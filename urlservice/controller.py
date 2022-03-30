import json
from flask import Flask, jsonify, request, redirect
from datetime import datetime
from datetime import timedelta

from pymongo import MongoClient, ReturnDocument

from utils import get_db_client


def create_url(request):
    db = ""
    startt = datetime.now()
    try:
        client = get_db_client()
        db = client.url_db
        data = json.loads(request.data)
        expiry_date = data.get('expiration_date', datetime.now() + timedelta(days=30))
        if isinstance(expiry_date, str):
            expiry_date = datetime.strptime(expiry_date, '%Y-%m-%dT%H:%M:%SZ')
        print(expiry_date)
        if data.get('url', '') == '':
            return 'Please provide a URL to shorten'
        print('Before DB Access!')
        row = db.url_tb.find_one({'url': {'$eq': data['url']}})
        print('After DB Access')
        if row and row.get('url'):
            endt = datetime.now()
            print((endt - startt).microseconds / 1000)
            return {'url': '{}shortly/{}'.format(request.host_url, row['id']), 'created_at': row.get('created_at'), 'expiration_date': row.get('expiration_date')}
        if data.get('alias'):
            if len(data['alias']) < 3 or len(data['alias']) > 10:
                return 'Selected Custom URL length should be between 3 to 10 characters!'
            row = db.url_tb.find_one({'id': {'$eq': data['alias']}})
            if row and row['url']:
                return 'Selected Custom URL already exists, please select another one!'
            row = db.url_tb.find_one_and_replace({'id': data['alias']},
                                                 {'id': data['alias'],
                                                  'url': data['url'],
                                                  'created_at': datetime.now(),
                                                  'expiration_date': expiry_date},
                                                 return_document=ReturnDocument.AFTER,
                                                 upsert=True)
        else:
            row = db.url_tb.find_one_and_update({'url': {'$eq': ''}},
                                                {"$set": {'url': data['url'], 'created_at': datetime.now(), 'expiration_date': expiry_date}},
                                                return_document=ReturnDocument.AFTER)
        endt = datetime.now()
        print((endt - startt).microseconds / 1000)
        return {'url': '{}shortly/{}'.format(request.host_url, row['id']), 'created_at': row.get('created_at'), 'expiration_date': expiry_date}
    except:
        return 'Internal Server Error'
    finally:
        if type(db) == MongoClient:
            db.close()


def recover_url_entry(db, key):
    db.url_tb.find_one_and_replace({'id': key},
                                   {'id': key,
                                    'url': '',
                                    'created_at': '',
                                    'expiration_date': ''},
                                   return_document=ReturnDocument.AFTER,
                                   upsert=True)


def is_expired(date):
    now = datetime.now()
    if now >= date:
        return True
    return False


def get_url(request, key):
    db = ""
    try:
        startt = datetime.now()
        client = get_db_client()
        db = client.url_db
        row = db.url_tb.find_one({'id': {'$eq': key}})
        endt = datetime.now()
        print((startt - endt).microseconds/1000)
        if row and row.get('url'):
            if not is_expired(row['expiration_date']):
                return redirect(row['url'])
            else:
                recover_url_entry(db, key)
                return jsonify('Your link has expired!')

        return jsonify('The request resource does not exist!')
    except:
        return 'Internal Server Error'
    finally:
        if type(db) == MongoClient:
            db.close()