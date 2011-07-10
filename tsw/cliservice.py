from entity import *
import service,os
from service import findtinyproxy
import config
import getpass

def __names(dao):
    """get proxy names, only used internally"""
    proxies = dao.all()
    print "\nName of proxies (proxy in use with '*'):"
    print "----------------"
    for p in proxies:
        pstr = "  %s"%(p.name)
        pstr = pstr.replace(' ','*' if p.active else ' ',1)

        print pstr
    print "----------------\n"

    

def all():
    """
	list all proxy profiles, proxy with '*' indicating that in use
    """
    conn    = service.getConnection()
    dao     = ProxyDao(conn)
    proxies = dao.all()
    #uproxy  = service.findUsingProxyInDB(conn)
    print "\nAll proxies in tinyswitch (proxy in use with '*'):"
    print "-"*70
    print "%-2s%-10s\t%-40s\t%-5s\t" % (" ","Name","Server","Port")
    print "-"*70
    for p in proxies:
        if  p.active:
            print "%-2s%-10s\t%-40s\t%-5s\t" % ("*", p.name, p.server, p.port) 
        else :
            print "%-2s%-10s\t%-40s\t%-5s\t" % (" ", p.name, p.server, p.port) 
    conn.close()

def remove():
    """remove a proxy by name"""
    conn = service.getConnection()
    dao  = ProxyDao(conn)
    __names(dao) # print available proxy names
    print "---- Removing Proxy ----"
    p = None # the proxy to be deleted
    while 1:
        name = raw_input("> Proxy name to be remove: ")
        if not name :
            print "Error: name cannot be empty!"
        else:
            p = dao.getProxyByName(name)
            if not p:
                print "Error: The proxy name doesn't exist!"
            elif p.active :
                print "Error: Current using proxy cannot be removed!"
            else:
                break
    
    print p
    confirm = raw_input("> Delete Proxy "+name+"? [yes|no] ")
    if confirm.lower() == "yes":
        dao.removeByName(name)
        conn.commit()
        print "---- Proxy removed ----"
    conn.close()
    

def add():
    """add a new proxy entry with cli"""
    conn  = service.getConnection()
    dao   = ProxyDao(conn)
    __names(dao) # print available proxy names
    print "---- Adding new Proxy ----"
    while 1:
        nname = raw_input("> The name of the new Proxy: ")
        if not nname or  dao.getProxyByName(nname):
            print "Error: name is empty or already exists!"
        else:
            break
    nserver = raw_input("> The server address of the new Proxy: ")
    nport   = raw_input("> The port number of the new Proxy: ")
    nuser   = raw_input("> Username  (Press Enter if no authentication needed): ")
    npwd    = ''
    if nuser:
        npwd = getpass.getpass("> password for the authentication: ")
    nnote         = raw_input("> The description of the new Proxy: ")
    p             = Proxy()
    p.name        = nname
    p.server      = nserver
    p.port        = nport
    p.username    = nuser
    p.password    = npwd
    p.description = nnote
    #set authString
    p.setAuthString()

    dao.addnew(p)
    np = dao.getProxyByName(nname)
    conn.commit()
    print "---- new proxy added ----"
    print np
    conn.close()

def set():
    """set proxy as current proxy"""
    
    init() #check if init() is needed
    conn = service.getConnection()
    dao  = ProxyDao(conn)
    __names(dao) # print available proxy names
    print "---- Set proxy ----"
    p = None # the proxy to be set
    while 1:
        name = raw_input("> Proxy name to be set: ")
        if not name :
            print "Error: name cannot be empty!"
        else:
            p = dao.getProxyByName(name)
            if not p:
                print "Error: The proxy name doesn't exist!"
            else:
                break
    
    conn.close()
    service.setproxy(p)
    print p
    print "---- Proxy set ----"

def init():
    """check tinyproxy start script path, if not there set the path interactively"""
    conn = service.getConnection()
    dao  = ProxyDao(conn)
    if not dao.getTinyProxyPath().strip(): # no value in DB for tinyproxy.bin.path
        print "\n---- tinyproxy mgmt script location has not been set. Enter initialization wizard ----\n"
        reconfig() 
        print "\n---- tinyswitch initialized ----\n"
    conn.close()

def reconfig():
    """reset tinyproxy.bin.path"""
    found = findtinyproxy()
    conn  = service.getConnection() 
    dao   = ProxyDao(conn)
    path  = ""
    print "\n---- set tinyproxy start script ----\n"
    if found:
        yn = raw_input("> TinySwtich found tinyproxy script (%s) Is that correct? [yes|no]: "%(found,))
        if yn.lower() == "yes":
            path = found
    while 1:
        
        path = raw_input( """> Please enter the tinyproxy mgmt script location:
Note:/usr/sbin/tinyproxy is NOT the script! \n """) if not path else path
        if path and os.path.isfile(path):
            break
        else:
            print "Error: script path is not valid"
            path=""
    #till here, path should be set successfully
    dao.saveTinyProxyPath(path)    
    conn.commit()
    print "\n---- tinyproxy mgmt script location [%s] was set ----\n" % (path,)
    conn.close()

