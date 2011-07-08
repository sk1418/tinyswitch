from entity import *
import sqlite3 as sqlite
import os,re,config

def getConnection():
    conn = sqlite.connect(config.CONN_PATH)
    return conn


def __lookupTP():
    """
    search the tinyproxy starting script. if found one (either in /etc/init.d/ or /etc/rc.d/) 
    return the path, otherwise return None. This should be done when application starts the 
    first time.(or the config in DB is empty)
    """
    if os.path.isfile(TP_LOOKUP1) :
        return config.TP_LOOKUP1
    elif os.path.isfile(TP_LOOKUP2):
        return config.TP_LOOKUP2
    else:
        return None

def findUsingProxyInConf():
    """
    find out the current proxy in use by tinyproxy
    return a list[server,port]
    """
    result = []
    f = open(config.TP_CONF)
    lines = f.readlines()
    lines.reverse()
    f.close()
    # find "upstream server:port"
    exp = """^\s*upstream (.+?:\d+)"""
    for l in lines:
        m = re.search(exp,l)
        if m :
            result = m.group(1).split(':')
            break
    return result

def findUsingProxyInDB(conn):
    """find the current using proxy in DB. this method will firstly get result from findUsingProxyInConf(),
    then do a database query to find out the match proxy entry"""
    serverInUse = findUsingProxyInConf()
    proxyDao = ProxyDao(conn)
    proxy = proxyDao.getProxyByServerAndPort(serverInUse[0],serverInUse[1])
    return proxy

def startup():
    """
    startup processing:
    1, set the config parameters (TP_BIN)
    2, get the proxy in conf file, set the corresponding proxy in db as active
    """
    # set system parameters(TP_BIN) in config
    conn = getConnection()
    proxyDao = ProxyDao(conn)
    bin = getTinyProxyPath(conn)
    config.TP_BIN = bin 

    # get the using proxy in conf file and set active in db
    deactiveAll(conn)
    serverInUse = findUsingProxyInConf()
    proxy = findUsingProxyInDB(conn)
    if proxy:
        proxyDao.setActive(proxy.id)
    conn.commit()
    conn.close()

def __restartTP():
    """
    restart tinyproxy. 
    """
    os.popen(config.TP_BIN + ' restart')   

    
def setproxy(proxy):
    """set the proxy as upstream of tinyproxy"""
    #read tinyproxy.conf        
    with open(config.TP_CONF,'r+w') as tinyconf:
        
        lines = tinyconf.readlines()
        lines.reverse()

        # find "upstream server:port" and remove
        exp = """^\s*upstream .+?:\d+"""
        for l in lines:
            m = re.search(exp,l)
            if m :
                lines.remove(l)
                break
        # find "Add header (authorization)" and remove
        expheader = """^\s*AddHeader "Proxy-Authorization" "Basic .+" """     
        for l in lines:
            m = re.search(expheader,l)
            if m:
                lines.remove(l)
                break
        
        lines.reverse()
        lines.append(config.UPSTREAM.format(proxy.server, proxy.port))
        if proxy.authString:
            lines.append(config.ADD_HEADER.format(proxy.authString))

        #write back to conf
        tinyconf.writelines(lines)

        #update the active flag
        conn = sqlite.connect(config.CONN_PATH)
        dao = ProxyDao(conn)
        dao.deactiveAll()
        dao.setActive(proxy.id)
        conn.commit()
        conn.close()

            



