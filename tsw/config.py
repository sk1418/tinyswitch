from os import path
import confighandler
import os

APP_PATH       = path.join(path.dirname(__file__),"../")
CONN_PATH      = path.join(os.getenv("HOME") , ".tinyswitch","data","proxies") #sqlite3

# backup tinyproxy.conf if it was changed by tinyswithcer
BACKUP_PATH    = path.join(os.getenv("HOME") , ".tinyswitch","backup","tinyproxy.conf.last")
TEMP_PATH    = path.join(os.getenv("HOME") , ".tinyswitch",".tmp")
VERSION        = '1.1.0'                                            #software version
VERSION_URL    = 'http://to be defined'                             #version url, used to check if there is new version
LATEST_VERSION = None
TP_BIN         = ''                                                 #tinyproxy starting script path, will be assigned by the confighandler
TP_CONF        = None #tinyproxy configuration file path, will be set by confighandler
TP_CONF_LOOKUP = ['/etc/tinyproxy/tinyproxy.conf','/etc/tinyproxy.conf']
UPSTREAM       = 'upstream http {0}:{1}\n'                               # proxy forwarding
ADD_HEADER     = 'AddHeader "Proxy-Authorization" "Basic {0}"\n'    # add header template. the placeholder {0} will be filled by authString
