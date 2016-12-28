from oslo_config import cfg  
import oslo_messaging  
import time  
import os
import MySQLdb
import uuid
  
class ServerControlEndpoint(object):  
  
    def __init__(self, server):  
        self.server = server  
  
    def stop(self, ctx):  
        if self.server:  
            self.server.stop()  
  
class TestEndpoint(object):  
  
    def test(self, ctx, a,b):  
        return a-b  
  
    def printTxt(self, ctx):
        return os.system("echo 'Hello 80'")

    def sayGood(self, ctx):
        return os.system("echo 'Good 80'")

def getMac():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

def getCid():
    db = MySQLdb.connect("database ip","root","password","databaseName" )
    cursor = db.cursor()
    sql = "select * from thinclient where mac='" + getMac() +"'"
    print sql
    cursor.execute(sql)
    result = cursor.fetchone()
    cid = result[8]
    db.commit()
    db.close()
    print cid
    return cid

#cfg.CONF.set_override("rabbit_host","10.1.101.36")  
transport_url = 'rabbit://guest:guest@10.0.0.108:5672/'  
#transport_url = 'rabbit://guest:0082e5a4f6ab4a2e9096c4988110d67b@10.1.101.36:5672/'  
transport = oslo_messaging.get_transport(cfg.CONF,transport_url)  
target = oslo_messaging.Target(topic='test', server=getCid())
endpoints = [  
    ServerControlEndpoint(None),  
    TestEndpoint(),  
]  
server = oslo_messaging.get_rpc_server(transport, target, endpoints,  
                                       executor='blocking')  
try:  
    server.start()  
    while True:  
        time.sleep(1)  
except KeyboardInterrupt:  
    print("Stopping server")  
  
server.stop()  
server.wait() 
