#!/usr/bin/env/py35
# coding=utf-8

from flask import Flask,request
from flask.json import jsonify
import math
import redis
from flask.views import MethodView

app = Flask(__name__)

class PIAPI(MethodView):

    def __init__(self,cache):
        self.cache = cache

    def get(self,num):
        s = 0.0
        result = self.cache.get(num)
        if result:
            return jsonify({"cache":True,"result":result})
        for i in range(1,num):
            s += 1/(i**2)
        result = math.sqrt(s*6)
        self.cache.set(num,result)
        return jsonify(dict(cache=False,result=result))

#定义分布式缓存对象
class RedisCache(object):
    def __init__(self,client):
        self.client = client
    def set(self,n,result):
        self.client.hset("pis",str(n),str(result))
    def get(self,n):
        result = self.client.hget("pis",str(n))
        if not result:
            return
        return float(result)
client = redis.StrictRedis()
cache = RedisCache(client)

app.add_url_rule('/pi/<int:num>',view_func=PIAPI.as_view("pi",cache))

if __name__ == '__main__':
    app.run("127.0.0.1",5001)