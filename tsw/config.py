from os import path

APP_PATH       = path.join(path.dirname(__file__),"../")
CONN_PATH      = path.join(APP_PATH,"data/proxies")                 #sqlite3 data file path
VERSION        = '1.0.0'                                            #software version
VERSION_URL    = 'http://to be defined'                             #version url, used to check if there is new version
LATEST_VERSION = None
TP_BIN         = ''                                                 #tinyproxy starting script path, will be assigned by the app.
TP_CONF        = path.join(APP_PATH,"tinyproxy.config")             #tinyproxy configuration file path
TP_LOOKUP1     = '/etc/init.d/tinyproxy'                            #tinyproxy lookup location 1
TP_LOOKUP2     = '/etc/rc.d/tinyproxy'                              #tinyproxy lookup location 2
UPSTREAM       = 'upstream {0}:{1}\n'                               # proxy forwarding
ADD_HEADER     = 'AddHeader "Proxy-Authorization" "Basic {0}"\n'    # add header template. the placeholder {0} will be filled by authString
