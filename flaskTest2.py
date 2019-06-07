#!/usr/bin/env/py35
# coding=utf-8

from flask import Flask,request
import math
import threading
from flask.json import jsonify
app = Flask(__name__)

#缓存数据到内存中
class CacheData(object):
    def __init__(self):
        self.lock = threading.RLock()   #定义锁,多线程访问时防止对全局变量修改造成的问题发生
        self.dataDict = {}              #json对象
    def get(self,n):
        with self.lock:
            return self.dataDict.get(n)  #注意这样写会报字典中的keyError,这里的dataDict是json对象,通过get访问value
    def set(self,n,pi):
        with self.lock:
            self.dataDict[n] = pi
cache = CacheData()
@app.route('/pi')
def pi():
    n = int(request.args.get('n','10'))  #传递参数给url,参数名为n,初始化值为10(必须为字符型),url访问时,则通过?参数名=参数值进行传递
    s = 0.0
    result = cache.get(n)
    if result:
        return jsonify({"cache":True,"result":result})
    for i in range(1,n):
        s += 1/(i**2)
    result = math.sqrt(6*s)
    cache.set(n,result)
    return jsonify(dict(cache=False,result=result))

if __name__ == '__main__':
    app.run('127.0.0.1',5001)