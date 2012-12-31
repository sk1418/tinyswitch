import os,shutil, sys 
import ConfigParser
import config


# Default(sample) conf 
APP_PATH       = os.path.join(os.path.dirname(__file__),"../")
SAMPLE_CONF = os.path.join(APP_PATH,'sample','tsw.conf')
SAMPLE_DATA  = os.path.join(APP_PATH,'sample','data','proxies')

#database path
DATA_PATH= os.path.join(os.getenv("HOME") , ".tinyswitch","data","proxies")


def configfile():
        return os.path.join(configdir(),"tsw.conf")

def configdir():
        return os.path.join(os.getenv("HOME") , ".tinyswitch")

def updateconfig(section, key, value):
    """ update the given config option"""
    cf = ConfigParser.ConfigParser()
    configFile = configfile()
    with open( configFile , 'r') as cfgf:
        cf.readfp(cfgf)
    cf.set(section, key, value)
    with open( configFile, 'w') as cfgf:
        cf.write(cfgf)

def requireInit():
    """
    check if the home config directory exists
    """
    return not os.path.exists(configdir())

def loadConfig():
    """
        load config from config file 
        return True if sucessful, otherwise False
    """
    cf = ConfigParser.ConfigParser()
    configFile = configfile()
    # if ~/.tinyswitch/tsw.conf doesn't exist, return False
    if not os.path.exists(configFile):
        return False

    cf.read(configFile);

    #load options
    config.TP_BIN  = cf.get("settings","tinyproxy.restart")
    config.TP_CONF = cf.get("settings", "tinyproxy.config")
    return True;




def initHomeConfPath():
    """
    create .tinyswitch under home
    """
    
    print "run the application 1st time. create .tinyswitch under your $HOME"
    confDir = configdir()
    dataDir = os.path.join(confDir, "data")
    backupDir = os.path.join(confDir, "backup")
    #mkdir and copy files
    if not os.path.exists(confDir):
        os.makedirs(dataDir)
        os.makedirs(backupDir)


    global SAMPLE_DATA, SAMPLE_CONF
    shutil.copy(SAMPLE_CONF,confDir)
    shutil.copy(SAMPLE_DATA, dataDir)
    print "configuration files are initialized"


