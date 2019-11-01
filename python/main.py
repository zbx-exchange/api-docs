#coding=utf-8

# python 3.6

from python.restful import ZbxSDK

def main():
    sdk = ZbxSDK("37cb78cd-7c35-48cc-83bb-aaa", "aaa")
    print("balance: ", sdk.getBalance())
    print("market config: ", sdk.getMarketConfig())
    print("funds: ", sdk.getFunds())
    print("getDepth: ", sdk.getDepth("btc_usdt"))

if __name__ == '__main__':
    main()
