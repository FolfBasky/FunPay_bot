import requests
from stem import Signal
from stem.control import Controller
import os


os.startfile('D:\Tor\Tor Browser\Browser\TorBrowser\Tor\\tor.exe')
def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                    'https': 'socks5://127.0.0.1:9050'}
    return session

session = get_tor_session()
print(session.get("http://httpbin.org/ip").text)
print(requests.get("http://httpbin.org/ip").text)

def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="password")
        controller.signal(Signal.NEWNYM)

session = get_tor_session()
print(session.get("http://httpbin.org/ip").text)

