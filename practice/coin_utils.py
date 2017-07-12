# coding=utf-8
import json
import requests

def get_details(eth=False):
    """ 현 시간 기준 detail 가격 정보를 가져 온다. """
    # 현시각, 가격, 매도가, 매수가, 지난 24시간 기준 최고가 최저가, 거래 볼륨
    coin = 'btc_krw'
    if eth:
        coin = 'eth_krw'
    DETAIL_PAGE = 'https://api.korbit.co.kr/v1/ticker/detailed?currency_pair=' + coin
    res = requests.get(DETAIL_PAGE)
    if res.status_code == 200:
        return res.status_code, res.json()
    return res.status_code, res.text