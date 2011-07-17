Introduction

Sometimes we have to work under various network environments. At different clients, in office, at home... Switching proxy settings again and again is really annoying.

TinySwitch? could help us to switch proxy setting easily.

Tinyproxy will work as a transparent proxy forwarding service. So tinyproxy is required to be installed.

Currently tinyswitch has only a CLI. A GUI may be added in the near future.
Requirements

    python 2.6+
    tinyproxy 

How to switch proxy

  1  install tinyproxy if you haven't done it yet.
  2  configurate tinyproxy to make localhost:port your system proxy. And set this proxy to any of your applications that need to configurate a proxy server.
  3  download and extract the archive. start the application by:

    cd {appDir}
    python tinyswitch

    Finally, follow the usage info to manage your own proxies and switch to certain proxy setting. 

project homepage:http://code.google.com/p/tinyswitch/
