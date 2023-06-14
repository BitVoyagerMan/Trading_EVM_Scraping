import asyncio
from fastapi import APIRouter
from moralis import evm_api
from web3 import Web3
#from backend.api.core.config import settings
import time

api_key = "UnxwRjMhBpOphkaYuxTT6f3HOH6SHi05z1TqHTKJneBI5sUETucsDuxGlZKFxICA"
infura_url = "https://eth-mainnet.g.alchemy.com/v2/vhgO2iZpWuCCQDMEWcegkkN6sbTPitfs"


router = APIRouter()
native_address = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
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
w3 = Web3(Web3.HTTPProvider(infura_url))
lpTokenAbi = [{"inputs":[],"payable":False,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint0256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"sender","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":True,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"sender","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"sender","type":"address"},{"indexed":False,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":True,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":False,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":True,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[],"name":"sync","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":True,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},{"constant":False,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"}]
lpSampleAddress = "0x0d4a11d5EEaaC28EC3F61d100daF4d40471f1852"

async def getPriceByTokenAddress(address, balance, decimals, symbol, count):
    time.sleep(count * 0.01)
    params = {
        "address": address,
        "include": "percent_change",
        "chain" : "eth"
    }
    try:
        result = evm_api.token.get_token_price(
            api_key=api_key,
            params=params,
        )
        return {"address" : address,"symbol":symbol,  "price":float(result["usdPrice"]) * int(balance) / (10**int(decimals))}
    except:
        return -1
        
def getEthPrice(address):
    params = {
        "address": address,
        "chain": "eth"
    }
    result = evm_api.token.get_token_price(
            api_key=api_key,
            params=params,
    )
    return result["usdPrice"]
def getEthBalance(wallet_address):
    params = {
        "address": wallet_address,
        "chain": "eth",
    }
    result = evm_api.balance.get_native_balance(api_key = api_key, params = params)
    return result["balance"]

@router.get("/getMainInfo/{wallet_address}")
async def get_Main_Info(wallet_address): 
    params = {
        "address": wallet_address,
        "chain": "eth",
    }
    
    result = evm_api.token.get_wallet_token_balances(
        api_key=api_key,
        params=params,
    )
    coroutines = []
    general_erc_token_list, stable_erc_token_list, lp_token_list = [], [], []
    general_total_amount, stable_total_amount, lp_total_amount = 0.0, 0.0, 0.0
    
    count = 0
    for item in result:
        try:
            tokenContract = w3.eth.contract(address=item['token_address'], abi=lpTokenAbi)
            temp = tokenContract.functions.factory().call()
            lpTokenPrice = getPriceByTokenAddress(item["token_address"], item["balance"], item["decimals"], item["symbol"], 0.1)
            lp_total_amount += lpTokenPrice
            lp_token_list.append({item["symbol"]: lpTokenPrice})    
        except:
            try:
                coroutines.append(getPriceByTokenAddress(item["token_address"], item["balance"], item["decimals"], item["symbol"], count))
                count += 1
                # if item['token_address'] in stable_coin_list:
                #     # if item['possible_spam'] == False:
                #     #     coroutines.append(getPriceByTokenAddress(item["token_address"], item["balance"], item["decimals"]))
                #     thisPrice = getPriceByTokenAddress(item["token_address"], item["balance"], item["decimals"])
                #     if thisPrice != -1:
                #         stable_total_amount += thisPrice
                #         stable_erc_token_list.append({item["symbol"]: thisPrice})

                # else:
                #     # if item['possible_spam'] == True:
                #     #     coroutines.append(getPriceByTokenAddress(item["token_address"], item["balance"], item["decimals"]))
                #     #     print(item)
                #     thisPrice =  getPriceByTokenAddress(item["token_address"], item["balance"], item["decimals"])
                #     if thisPrice != -1:
                #         general_total_amount += thisPrice
                #         general_erc_token_list.append({item["symbol"]: thisPrice})
            except:
                print(item['token_address'])
    results = await asyncio.gather(*coroutines)
    for item in results:
        if item is not -1:
            if item["address"] in stable_coin_list:
                stable_total_amount += item["price"]
                stable_erc_token_list.append({item["symbol"] : item["price"]})
            else:
                general_total_amount += item["price"]
                general_erc_token_list.append({item["symbol"] : item["price"]})

    print(results)
    native_total_amount = int(getEthBalance(wallet_address)) * float(getEthPrice(native_address)) / (10**18)
    return {
        "total" : native_total_amount + stable_total_amount + general_total_amount + lp_total_amount,
        "eth" : {"total": native_total_amount},
        "stableCoin" : {"total" : stable_total_amount, "lists" : stable_erc_token_list}, 
            "erc20" : {"total" : general_total_amount, "lists": general_erc_token_list},
        "lptoken" : {"total" : lp_total_amount , "lists" : lp_token_list}
    }