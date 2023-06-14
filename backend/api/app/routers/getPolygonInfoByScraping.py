import requests
from fastapi import APIRouter
router = APIRouter()
from bs4 import BeautifulSoup
headers = {
    'authority': 'polygonscan.com' ,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' ,
    'accept-language': 'en,en-US;q=0.9' ,
    'cache-control': 'max-age=0' ,
    'cookie': 'ASP.NET_SessionId=fes44t2mlxqfzjq4r2qeptsj; __cflb=0H28vYYxgAifymwG4XL3XRekfBvuaNsjy7kH12kkFEL; _ga_QD3P95KD1C=GS1.1.1686672486.1.0.1686672486.0.0.0; _ga=GA1.1.1969594245.1686672487' ,
    'sec-ch-ua':'"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"' ,
    'sec-ch-ua-mobile': '?0' ,
    'sec-ch-ua-platform': '"Linux"' ,
    'sec-fetch-dest': 'document' ,
    'sec-fetch-mode': 'navigate' ,
    'sec-fetch-site': 'none' ,
    'sec-fetch-user': '?1' ,
    'upgrade-insecure-requests':'1' ,
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36' ,
}


   

BASE_URL = "https://polygonscan.com/address/"
stable_coin_list = [
    '0xc2132d05d31c914a87c6611c10748aeb04b58e8f',
    '0x170a18b9190669cda08965562745a323c907e5ec',
    '10x2791bca1f2de4661ed88a30c99a7a9449aa84174',
    '0x8f3cf7ad23cd3cadbd9735aff958023239c6a063',
    '0x2e1ad108ff1d8c782fcbbb89aad783ac49586756',
    '0x45c32fa6df82ead1e2ef74d17b76547eddfaff89'
]
@router.get("/getPolygonInfoByScraping/{wallet_address}")
async def getPolygonInfoByScraping(wallet_address):
    username = 'bitboyager'
    password = 'bitboyager'
    proxy = f"http://{username}:{password}@dc.smartproxy.com:10000"
    url = BASE_URL + wallet_address

    response = requests.get(url, headers=headers, proxies = {'http': proxy, 'https': proxy})

    soup = BeautifulSoup(response.content, 'html5lib')
    matic_value, total = 0.0, 0.0
    stable_total, general_total, lp_total = 0.0, 0.0, 0.0
    stable_list, general_list, lp_list = [], [], []
    try:
        overview_element = soup.find(lambda tag: tag.name == 'div' and tag.get_text(strip = True).lower() == "matic value:")
        print(float(overview_element.next_sibling.next_sibling.getText().strip().split(' ')[0].replace('$', '').replace(',', '')))
        matic_value = float(overview_element.next_sibling.next_sibling.getText().strip().split(' ')[0].replace('$', '').replace(',', ''))
        total += matic_value
    except:
        matic_value = 0.0

    ulElements = soup.find('ul', {"class" : "list list-unstyled mb-0"})
    elementArray = ulElements.find_all("a", {"class" : "link-hover d-flex justify-content-between align-items-center"})
    for element in elementArray:
        try:
            element_url = str(element.attrs.get('href')).replace('/token/', '').split('?')[0]
            token_value = float(str(element.find("div", {"class" : "text-right"}).find("span", {"class": "list-usd-value d-block"}).getText()).strip().replace('$', '').replace(',', ''))
            print(token_value)
            symbol_element = element.find("span", {"class" : "list-amount link-hover__item hash-tag hash-tag--md text-truncate"})
            symbol = symbol_element.getText().strip().split(' ')[1]
            print(symbol)
            if element_url in stable_coin_list:
                stable_total += token_value
                stable_list.append({symbol : token_value})
            else:
                general_total += token_value
                general_list.append({symbol : token_value})

        except: 
            continue
    total = total + general_total + stable_total
    
    
    return_value = {"total" : total, "matic" : matic_value, "stableCoin" : {"total": stable_total, "lists" : stable_list}, "erc20" :
                    {"total" : general_total, "list" : general_list}, "lptoken" : {"total" : lp_total, "list" : lp_list}}
    return return_value
