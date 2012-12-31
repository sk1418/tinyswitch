from entity import *
import sqlite3 as sqlite
import os,re,config,subprocess,shutil
import confighandler

def getConnection():
    conn = sqlite.connect(config.CONN_PATH)
    return conn

def checkPermission():
    """check if the user has permission to update tinyproxy conf file and manage tinyproxy"""
    return  True


def findtinyproxyConf():
    """
    search the tinyproxy conf file. If one was found (defined in config.TP_CONF_LOOKUP)
    return the path, otherwise return None. 
    this is needed for reconfig tinyswitcher
    """
    for f in config.TP_CONF_LOOKUP:
        if os.path.isfile(f) :
            return f
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
    proxy = proxyDao.getProxyByServerAndPort(serverInUse[0],serverInUse[1]) if len(serverInUse)==2 else proxyDao.getNoProxy()
    return proxy

def resync_proxy():
    """
     get the proxy in conf file, set the corresponding proxy in db as active
    return true if everything is ok, otherwise return false
    """
    conn = getConnection()
    proxyDao = ProxyDao(conn)
    proxyDao.deactiveAll()
    serverInUse = findUsingProxyInConf()
    proxy = findUsingProxyInDB(conn)
    if proxy:
        proxyDao.setActive(proxy.id)
    conn.commit()
    conn.close()
    return 1

def __refresh_tinyproxy():
    """
    update the tinyproxy.conf and 
    restart tinyproxy. 
    """
    
    print "updating tinyproxy config and restarting tinyproxy..."
    cmd= "sudo cp -f "  + config.TEMP_PATH + " " + config.TP_CONF+" && sudo " + config.TP_BIN
    retval =  subprocess.call(cmd, shell=True)
    print "done"
    return retval
    
def __backupConf():
    """cp the tinyproxy.conf to backup directory before setproxy"""
    shutil.copy2(config.TP_CONF,config.BACKUP_PATH)
    print "A backup of the original tinyproxy.conf was stored at " + config.BACKUP_PATH

def setproxy(proxy):
    """set the proxy as upstream of tinyproxy
        since updating tinyproxy.conf and restarting tinyproxy service need
        root privilege, the setproxy will work in following steps:
        1- cp tinyproxy.conf to ~/.tinyswitch/.tmp
        2- backup tinyproxy.conf to backup dir
        3- read and update the tmp file
        4- sudo cp tmp -> real conf, and sudo restart tinyproxy
        5- update database
    """
    
    # cp tinyproxy.conf to .tmp
    shutil.copy(config.TP_CONF, config.TEMP_PATH)



    lines = []
    #read tmp
    with open(config.TEMP_PATH,'r+') as tinyconf: 
        lines = tinyconf.readlines()
        lines.reverse()
        exp = """^\s*upstream .+?:\d+"""
        for l in lines:
            m = re.search(exp,l)
            if m :
                lines.remove(l)
                break
        # find "Add header (authorization)" and remove
        expheader = '''^\s*AddHeader "Proxy-Authorization" "Basic .+"'''     
        for l in lines:
            m = re.search(expheader,l)
            if m:
                lines.remove(l)
                break
        
        lines.reverse()
        if lines[-1][-1] != '\n':
            lines.append('\n')
        if proxy.name != 'noproxy':
            lines.append(config.UPSTREAM.format(proxy.server, proxy.port))
            if proxy.authString:
                lines.append(config.ADD_HEADER.format(proxy.authString))
        #before write back to file, do backup
        __backupConf()

        #write back to conf(tmp file)
        tinyconf.seek(0,0)
        tinyconf.writelines(lines)
        tinyconf.truncate(tinyconf.tell())

    #cp tmp to real tinyproxy.conf
    if not __refresh_tinyproxy() >0 :
        #update the active flag
        conn = sqlite.connect(config.CONN_PATH)
        dao = ProxyDao(conn)
        dao.deactiveAll()
        dao.setActive(proxy.id)
        conn.commit()
        conn.close()
                



