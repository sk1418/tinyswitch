from entity import *
import service,os
from service import findtinyproxyConf
import config, confighandler
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
        elif name == 'noproxy':
            print "Error: 'noproxy' is a reversed proxy, it cannot be deleted!"
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
    while 1:
        nserver = raw_input("> The server address of the new Proxy: ")
        if not nserver:
            print "Error: server address cannot be empty!"
        else:
            break
    while 1:
        nport   = raw_input("> The port number of the new Proxy: ")
        if not nport:
            print "Error: port number cannot be empty!"
        else:
            break
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

def setByName(name):
    
    """set proxy by given name"""
    #check permission
    if not service.checkPermission():
        print "Error: set proxy failed. Permission denied!"
        exit(1)
    conn  = service.getConnection() 
    dao   = ProxyDao(conn)
    p = dao.getProxyByName(name)
    conn.close()
    if not p:
        print "Error: The proxy name doesn't exist!"
    else:
        service.setproxy(p)
        print "Proxy was set successfully."
        print p

def set():
    """set proxy as current proxy (interactively)"""
    
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

def reconfig():
    """reset values in config file"""
    cmd  = ""
    print "\n---- set command line to restart tinyproxy  ----\n"
    while 1:
    
        cmd = raw_input( """> Please enter the command line to restart tinyproxy [without sudo]:
> For example : 
    systemctl restart tinyproxy.service 
> or
    /etc/init.d/tinyproxy restart
> or
    /etc/rc.d/tinyproxy restart \n """) 
        if cmd and cmd.find("restart")>=0 and cmd.find('tinyproxy')>=0:
            break
        else:
            print "Error: tinyproxy restart command is not correct."

    cmd = cmd.lower().replace('sudo','')
    #till here, cmd should be set successfully
    confighandler.updateconfig("settings","tinyproxy.restart",cmd)

    #tinyproxy conf part (tinyproxy.conf)
    found = findtinyproxyConf()
    cfg = ''
    if found:
        yn = raw_input("> TinySwitch has found tinyproxy.conf at (%s) Is that correct? [yes|no]" % found)
        if yn.lower() == 'yes':
            cfg = found
    while 1:
        cfg = raw_input("""> Please enter the tinyproxy config file location:
        > (usually it has name tinyproxy.conf)\n """) if not cfg else cfg

        if cfg and os.path.isfile(cfg):
            break
        else:
            print "Error: given tinyproxy config file is not valid."
    confighandler.updateconfig("settings","tinyproxy.config",cfg)




