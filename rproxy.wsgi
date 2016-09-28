#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bottle import Bottle
import json

from common import Service, ReverseProxyRecords, ReverseProxyRecord, params

app = application = Bottle()
get = app.get
post = app.post
put = app.put
delete = app.delete
error = app.error

@get('/')
def ping():
    return {'status': 'LIVE'}


@get('/record/json')
def get_record():
    return ReverseProxyRecords().json()


@get('/record/<id_:int>')
def get_record_from_id(id_):
    return [str(ReverseProxyRecord(id_))]


@post('/record')
@Service.auth
@params(require=['host', 'upstream'])
def post_record(user, params):
    record = ReverseProxyRecords().add(**params)
    return {'id': str(record.id_)}

@put('/record/<id_:int>')
@Service.auth
@params(option=['host', 'upstream'])
def put_record(user, id_, params):
    ReverseProxyRecord(id_).update(**params)


@delete('/record/<id_:int>')
@Service.auth
def delete_record(user, id_):
    ReverseProxyRecords().delete(id_)


@error(400)
@error(401)
@error(404)
@error(405)
def error(err):
    return json.dumps({'message': err.body})

if __name__ == '__main__':
    app.run(reloader=True, debug=True)