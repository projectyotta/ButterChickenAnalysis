import socks
import socket
import stem.process
import requests
from bs4 import BeautifulSoup 
import win_inet_pton


SOCKS_PORT=7040# You can change the port number

tor_process = stem.process.launch_tor_with_config(tor_cmd='C:\\Users\\raosa\\Desktop\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe',config = {'SocksPort': str(SOCKS_PORT),},)


socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5,addr="127.0.0.1", port=SOCKS_PORT)
socket.socket = socks.socksocket

page= requests.get("http://lchudifyeqm4ldjj.onion/?category=125")
soup= BeautifulSoup(page.content,'html.parser')
html1=soup.find_all("script",{"type":"text/javascript"})
s=str(html1)
start = 'var proddata = '
end = '$( document ).ready'
print (s[s.find(start)+len(start):s.rfind(end)])

tor_process.kill()