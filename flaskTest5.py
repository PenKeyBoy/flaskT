#!/usr/bin/env/py35
# coding=utf-8

from flask import Flask,request
from flask.json import jsonify
import math
import redis
from flask_classy import route,FlaskView

app = Flask(__name__)

class MathAPI(FlaskView):


    @route('/pi/<int:num>')
    def pi(self,num):
        s = 0.0
        result = cache.get_pi(num)
        if result:
            return jsonify({"cache":True,"result":result})
        for i in range(1,num):
            s += 1/(i**2)
        result = math.sqrt(s*6)
        cache.set_pi(num,result)
        return jsonify(dict(cache=False,result=result))
    @route('/fib/<int:n>/<int:m>')
    def feibo(self,n,m):
        result,cache = self.get_feibo(n,m)
        return jsonify({"cache":cache,"result":result})

    def get_feibo(self,n,m):
        if n < m:
            return 1,True
        else:
            result = cache.get_feibo(n)
            if result:
                return result,True
            result = self.get_feibo(n-1)[0] + self.get_feibo(n-2)[0]
            cache.set_feibo(n,result)
            return result,False

#定义分布式缓存对象
class RedisCache(object):
    def __init__(self,client):
        self.client = client
    def set_pi(self,n,result):
        self.client.hset("pis",str(n),str(result))
    def get_pi(self,n):
        result = self.client.hget("pis",str(n))
        if not result:
            return
        return float(result)
    def set_feibo(self,n,result):
        self.client.hset("fibs",str(n),str(result))
    def get_feibo(self,n):
        result = self.client.hget("fibs",str(n))
        if not result:
            return
        return float(result)
client = redis.StrictRedis()
cache = RedisCache(client)

#mathAPI = MathAPI(cache)
#不能有带参数的构造函数作为注册类
MathAPI.register(app,route_base='/')

if __name__ == '__main__':
    app.run("127.0.0.1",5001)

