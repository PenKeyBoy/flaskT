#!/usr/bin/env/py35
# coding=utf-8
from flask import Flask,request
from flask.json import jsonify
import math
import redis

app = Flask(__name__)

@app.route('/pi')
def pi():
    num = int(request.args.get('n','10'))
    s = 0.0
    result = cache.get(num)
    if result:
        return jsonify({"cache":True,"result":result})
    for i in range(1,num):
        s += 1/(i**2)
    result = math.sqrt(s*6)
    cache.set(num,result)
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

if __name__ == '__main__':
    app.run("127.0.0.1",5001)