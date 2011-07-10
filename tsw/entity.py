
import sqlite3 as sqlite
import base64

class Proxy:
    '''
    the database table mapping object
    '''
    def __init__(self):
        #database fields
        self.id          = 0
        self.name        = ''
        self.server      = ''
        self.port        = ''
        self.username    = ''
        self.password    = ''
        self.authstring  = ''
        self.active      = 0
        self.description = ''

    def setAuthString(self):
        """generate authstring if user& password were set"""
        if self.username and self.password:
            authstr = base64.standard_b64encode(self.username+":"+self.password)
            self.authstring = authstr


    def __repr__(self):
        return ' Id:%d, \n name:%s \n server:%s \n port:%s \n authString: %s\n desc:%s' %(self.id,self.name, self.server, self.port, self.authstring, self.description )


class ProxyDao:

    '''
    database access object(dao), responsible for handle database related operations
    '''

    def __init__(self,conn):
        self.conn = conn

    def all(self):

        ''' get all proxy entries in database'''

        sql = """select id, name, server, port, username, password, authString, active, description From Proxy """
        proxyList = []
        cur = self.conn.cursor()
        cur.execute(sql)

        for row in cur.fetchall():
            p = Proxy()
            (p.id, p.name, p.server, p.port, p.username, p.password, p.authString, p.active, p.description ) = row
            proxyList.append(p)

        cur.close()
        return proxyList
    
    def getProxyByName(self,name):
        """
         find a proxy by given name
        """
        sql = """select id, name, server, port, username, password, authString, active, description From Proxy where name = ?"""
        cur = self.conn.cursor()
        cur.execute(sql,(name,))
        p = Proxy()
        row = cur.fetchone()
        if row:
            (p.id, p.name, p.server, p.port, p.username, p.password, p.authString, p.active, p.description ) = row
        cur.close()
        return p if p.id>0 else None

    def getProxyByServerAndPort(self, server, port):
        
        sql = """select id, name, server, port, username, password, authString, active, description 
                    From Proxy where server=? and port=? """
        cur = self.conn.cursor()
        cur.execute(sql,(server, port))
        p = Proxy()
        row = cur.fetchone()
        if row:
            (p.id, p.name, p.server, p.port, p.username, p.password, p.authString, p.active, p.description ) = row
        cur.close()
        return p if p else None

    def setActive(self,id):

        """ set the proxy entry with given Id as active"""

        sql = """ UPDATE proxy set active=1 where id=?  """
        cur = self.conn.cursor()
        cur.execute(sql,(id,))
        cur.close()

    def deactiveAll(self):

        """ set all proxy entries active=0"""
        
        sql = """ update proxy set active=0"""
        cur = self.conn.cursor()
        cur.execute(sql)
        cur.close()

    def addnew(self, p):

        """add a new proxy entry"""

        sql = """INSERT INTO proxy ( id, name, server, port, username, password, authString, active, description )
            VALUES(null,?,?,?,?,?,?,?,?)"""
        cur = self.conn.cursor()
        cur.execute(sql,(p.name, p.server, p.port, p.username, p.password, p.authstring, p.active, p.description ))
        cur.close()

    def isActive(self, id):
        """
        check if the given proxy entry is being used
        """
        
        sql = """select active from proxy where id=?"""
        cur = self.conn.cursor()
        cur.execute(sql,(id,))
        a = cur.fetchone()[0]
        cur.close()
        return a
    
    def removeByName(self, name):
        """ 
        remove a proxy by given name
        """
        sql = """DELETE FROM Proxy where name=?"""

        cur = self.conn.cursor()
        cur.execute(sql,(name,))
        cur.close()

    def removeById(self, id):
        """ 
        remove a proxy entry by Id
        """
        sql = """DELETE FROM Proxy where id=?"""

        cur = self.conn.cursor()
        cur.execute(sql,(id,))
        cur.close()


    def getTinyProxyPath(self):
        sql = """select value from Config where name='tinyproxy.bin.path'"""
        cur = self.conn.cursor()
        cur.execute(sql)
        path = cur.fetchone()[0]
        cur.close()
        return path

    def saveTinyProxyPath(self,v):
        sql = """UPDATE config SET value=? where name='tinyproxy.bin.path'"""
        cur = self.conn.cursor()
        cur.execute(sql,(v,))
        cur.close()

