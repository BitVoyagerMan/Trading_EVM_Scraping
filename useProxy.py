import requests
url = 'https://ip.smartproxy.com/json'
username = 'bitboyager'
password = 'bitboyager'
proxy = f"http://{username}:{password}@dc.smartproxy.com:10000"
result = requests.get(url, proxies = {
    'http': proxy,
    'https': proxy
})
print(result.text)