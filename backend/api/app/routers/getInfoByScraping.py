import requests
from fastapi import APIRouter
router = APIRouter()
from bs4 import BeautifulSoup
headers = {
    "authority": "etherscan.io",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en,en-US;q=0.9",
    "cache-control": "max-age=0",
    "cookie": "ASP.NET_SessionId=lyy03wk1ykawt1mwcsh3n4cv; bitmedia_fid=eyJmaWQiOiIxYWNiZWQ3YzE5ZTJlZWYwMDdkMDdhYTQxMjEwOTdhNyIsImZpZG5vdWEiOiI1YzhlMTk4ZjhlZjE1NGRiNzQxNzdiMzhiNmM3Y2QyNSJ9; etherscan_cookieconsent=True; _gid=GA1.2.200767984.1686483741; __cflb=02DiuFnsSsHWYH8WqVXaqGvd6BSBaXQLToUQJzJ87oPdN; _ga_T1JC9RNQXV=GS1.1.1686566128.24.1.1686566129.0.0.0; _ga=GA1.2.268979062.1685986797",
    "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Linux",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}
BASE_URL = "https://etherscan.io/address/"
stable_coin_list = [
    '0xdac17f958d2ee523a2206206994597c13d831ec7',
    '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
    '0x6b175474e89094c44da98b954eedeac495271d0f',
    '0x0000000000085d4780B73119b644AE5ecd22b376',
    '0x8e870d67f660d95d5be530380d0ec0bd388289e1',
    '0x0c10bf8fcb7bf5412187a595ab97a3609160b5c6',
    '0x056Fd409E1d7A124BD7017459dFEa2F387b6d5Cd',
    '0xa47c8bf37f92aBed4A126BDA807A7b7498661acD',
    '0x853d955acef822db058eb8505911ed77f175b99e',
    '0x5f98805A4E8be255a32880FDeC7F6728C6568bA0'
]
@router.get("/getInfoByScraping/{wallet_address}")
async def getInfoByScraping(wallet_address):
    username = 'bitboyager'
    password = 'bitboyager'
    proxy = f"http://{username}:{password}@dc.smartproxy.com:10000"
    url = BASE_URL + wallet_address
    response = requests.get(url, headers=headers, proxies = {'http': proxy, 'https': proxy})

    soup = BeautifulSoup(response.content, 'html5lib')

    eth_balance_float = 0.0
    #get Eth
    try: 
        h4_element_eth_balance = soup.find(lambda tag: tag.name == 'h4' and tag.get_text(strip=True).lower() == "eth balance")
        eth_balance_integer = h4_element_eth_balance.parent.find("i").next_sibling
        eth_balance_non_integer = str(eth_balance_integer.next_sibling.next_sibling).strip().split(' ')[0]
        eth_balance_total = str(eth_balance_integer).strip().replace(',', '') + '.' + eth_balance_non_integer
        eth_balance_float = float(eth_balance_total)
    except: 
        eth_balance_float = 0.0
    print(eth_balance_float)


    #get Eth value
    h4_element_eth_value = soup.find(lambda tag: tag.name == 'h4' and tag.get_text(strip=True).lower() == "eth value")
    eth_value_float, lp_total = 0.0, 0.0
    eth_value_float= float(str(h4_element_eth_value.next_sibling).strip().replace(',', '').replace('$', ''))
    print(eth_value_float)    
    
    #get all tokens
    ulElements = soup.find("ul", {"class" : "list nav nav-pills nav-pills-flush nav-list flex-column w-100"})
    elementArray = ulElements.find_all("a", {"class" : "nav-link d-flex justify-content-between align-items-center gap-2 px-2"})
    stable_list, general_list, lp_list = [], [], []
    stable_total, general_total = 0.0, 0.0
    for element in elementArray:
        try:

            element_url = str(element.attrs.get('href')).replace('/token/', '').split('?')[0]
            previousTokenELement = element.find("div", {"class" : "d-flex align-items-center gap-1"})
            tokenValue = str(element.find("div", {"class": "list-usd-value"}).getText())
            if tokenValue.find('$') < 0:
                continue
            else:
                try:
                    tokenValue = float(tokenValue.replace('$', '').replace(',', ''))
                    tokenSymbole = previousTokenELement.next_sibling.getText().split(' ', 1)[1]
                    if element_url in stable_coin_list:
                        stable_total += tokenValue
                        stable_list.append({tokenSymbole : tokenValue})
                    else:
                        general_total += tokenValue
                        general_list.append({tokenSymbole : tokenValue})
                except:
                    continue
        except:
            continue
    total_value = eth_value_float + stable_total + general_total
    return_value = {"total" : total_value, "eth" : eth_value_float, "stableCoin" : {"total": stable_total, "lists" : stable_list}, "erc20" :
                    {"total" : general_total, "list" : general_list}, "lptoken" : {"total" : lp_total, "list" : lp_list}}
    return return_value
