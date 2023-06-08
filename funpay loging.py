<<<<<<< HEAD
import requests
import socks
import socket
import stem
from stem.control import Controller

# Set the IP and port of the Tor proxy
TOR_PROXY_IP = '127.0.0.1'
TOR_PROXY_PORT = 9050

# Set the URL you want to fetch
url = 'https://funpay.com/'

# Set the hashed password for the Tor Control Port
TOR_CONTROL_PASSWORD = '16:2426680620937F1560608CE435BFB439FBA0533A3C849F25879A517F34'

# Create a session object
session = requests.session()

# Set the session to use Tor proxy
session.proxies = {'http': 'socks5://{}:{}'.format(TOR_PROXY_IP, TOR_PROXY_PORT),
                   'https': 'socks5://{}:{}'.format(TOR_PROXY_IP, TOR_PROXY_PORT)}

# Define your headers
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'funpay.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0',
}

# Set the headers for the session
session.headers.update(headers)

# Connect to the Tor Control Port and authenticate
with Controller.from_port(address=TOR_PROXY_IP, port=TOR_PROXY_PORT) as controller:
    controller.authenticate(TOR_CONTROL_PASSWORD)

    # Make the request through Tor proxy using the session object
    response = session.get(url)

# Print the response content
print(response.content)
=======
<<<<<<< HEAD
import requests
import socks
import socket
import stem
from stem.control import Controller

# Set the IP and port of the Tor proxy
TOR_PROXY_IP = '127.0.0.1'
TOR_PROXY_PORT = 9050

# Set the URL you want to fetch
url = 'https://funpay.com/'

# Set the hashed password for the Tor Control Port
TOR_CONTROL_PASSWORD = '16:2426680620937F1560608CE435BFB439FBA0533A3C849F25879A517F34'

# Create a session object
session = requests.session()

# Set the session to use Tor proxy
session.proxies = {'http': 'socks5://{}:{}'.format(TOR_PROXY_IP, TOR_PROXY_PORT),
                   'https': 'socks5://{}:{}'.format(TOR_PROXY_IP, TOR_PROXY_PORT)}

# Define your headers
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'funpay.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0',
}

# Set the headers for the session
session.headers.update(headers)

# Connect to the Tor Control Port and authenticate
with Controller.from_port(address=TOR_PROXY_IP, port=TOR_PROXY_PORT) as controller:
    controller.authenticate(TOR_CONTROL_PASSWORD)

    # Make the request through Tor proxy using the session object
    response = session.get(url)

# Print the response content
print(response.content)
=======
<<<<<<< HEAD
import requests
import socks
import socket
import stem
from stem.control import Controller

# Set the IP and port of the Tor proxy
TOR_PROXY_IP = '127.0.0.1'
TOR_PROXY_PORT = 9050

# Set the URL you want to fetch
url = 'https://funpay.com/'

# Set the hashed password for the Tor Control Port
TOR_CONTROL_PASSWORD = '16:2426680620937F1560608CE435BFB439FBA0533A3C849F25879A517F34'

# Create a session object
session = requests.session()

# Set the session to use Tor proxy
session.proxies = {'http': 'socks5://{}:{}'.format(TOR_PROXY_IP, TOR_PROXY_PORT),
                   'https': 'socks5://{}:{}'.format(TOR_PROXY_IP, TOR_PROXY_PORT)}

# Define your headers
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'funpay.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0',
}

# Set the headers for the session
session.headers.update(headers)

# Connect to the Tor Control Port and authenticate
with Controller.from_port(address=TOR_PROXY_IP, port=TOR_PROXY_PORT) as controller:
    controller.authenticate(TOR_CONTROL_PASSWORD)

    # Make the request through Tor proxy using the session object
    response = session.get(url)

# Print the response content
print(response.content)
=======
<<<<<<< HEAD
import requests
import socks
import socket
import stem
from stem.control import Controller

# Set the IP and port of the Tor proxy
TOR_PROXY_IP = '127.0.0.1'
TOR_PROXY_PORT = 9050

# Set the URL you want to fetch
url = 'https://funpay.com/'

# Set the hashed password for the Tor Control Port
TOR_CONTROL_PASSWORD = '16:2426680620937F1560608CE435BFB439FBA0533A3C849F25879A517F34'

# Create a session object
session = requests.session()

# Set the session to use Tor proxy
session.proxies = {'http': 'socks5://{}:{}'.format(TOR_PROXY_IP, TOR_PROXY_PORT),
                   'https': 'socks5://{}:{}'.format(TOR_PROXY_IP, TOR_PROXY_PORT)}

# Define your headers
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'funpay.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0',
}

# Set the headers for the session
session.headers.update(headers)

# Connect to the Tor Control Port and authenticate
with Controller.from_port(address=TOR_PROXY_IP, port=TOR_PROXY_PORT) as controller:
    controller.authenticate(TOR_CONTROL_PASSWORD)

    # Make the request through Tor proxy using the session object
    response = session.get(url)

# Print the response content
print(response.content)
=======
import requests
import socks
import socket
import stem
from stem.control import Controller

# Set the IP and port of the Tor proxy
TOR_PROXY_IP = '127.0.0.1'
TOR_PROXY_PORT = 9050

# Set the URL you want to fetch
url = 'https://funpay.com/'

# Set the hashed password for the Tor Control Port
TOR_CONTROL_PASSWORD = '16:2426680620937F1560608CE435BFB439FBA0533A3C849F25879A517F34'

# Create a session object
session = requests.session()

# Set the session to use Tor proxy
session.proxies = {'http': 'socks5://{}:{}'.format(TOR_PROXY_IP, TOR_PROXY_PORT),
                   'https': 'socks5://{}:{}'.format(TOR_PROXY_IP, TOR_PROXY_PORT)}

# Define your headers
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Connection': 'keep-alive',
    'Host': 'funpay.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0',
}

# Set the headers for the session
session.headers.update(headers)

# Connect to the Tor Control Port and authenticate
with Controller.from_port(address=TOR_PROXY_IP, port=TOR_PROXY_PORT) as controller:
    controller.authenticate(TOR_CONTROL_PASSWORD)

    # Make the request through Tor proxy using the session object
    response = session.get(url)

# Print the response content
print(response.content)
>>>>>>> 565460b5876c66c31060864aa69648006c9b57cf
>>>>>>> c94eb43cafae8456b0d09263493333b294208127
>>>>>>> 55d86b2620a499ab8f4b40407eda5f9cfbd762af
>>>>>>> e8743d690ca7d593304005160665172d2b2c5204
