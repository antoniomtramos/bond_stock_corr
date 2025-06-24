#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 23:27:03 2024

@author: amtramos
"""
import pandas as pd
import requests
import urllib.parse
from datetime import timedelta, datetime


class YF:
    
    def __init__(self):
        pass
        
    def init_param(self,ticker="^GSPC",dtEnd = pd.Timestamp.today(),dtIni = pd.Timestamp.today() - timedelta(10*365)):
        self.dtEnd     = dtEnd
        self.dtIni     = dtIni
        self.dtEndUnix = (dtEnd - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
        self.dtIniUnix = (dtIni - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
        self.ticker = ticker
        
    def chg_ticker(self,ticker):
        self.ticker = ticker
        
    def chg_interval(self,dtIni,dtEnd):
        
        if type(dtIni) == type('asd'):
            dtIni = pd.Timestamp(dtIni)
        if type(dtEnd) == type('asd'):
            dtEnd = pd.Timestamp(dtEnd)
        
        self.dtEnd     = dtEnd
        self.dtIni     = dtIni
        self.dtEndUnix = (dtEnd - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
        self.dtIniUnix = (dtIni - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    
    def get_data(self,ticker):
        self.ticker = ticker
        tickerurlencoded = urllib.parse.quote_plus(self.ticker)
        headers_request = {
                'host':'query1.finance.yahoo.com',
                'user-agent':'mozilla/5.0 (x11; ubuntu; linux x86_64; rv:126.0) gecko/20100101 firefox/126.0',
                'accept':'*/*',
                'accept-language':'pt-br,pt;q=0.8,en-us;q=0.5,en;q=0.3',
                'accept-encoding':'gzip, deflate, br, zstd',
                'referer':'https://finance.yahoo.com/quote/{tickerurlencoded}',
                'origin':'https://finance.yahoo.com',
                'connection':'keep-alive',
                'cookie':'A1=d=AQABBJ0TZWYCEHSNoZBDb-Q5uf6aUH9pQl4FEgEBAQFlZmZuZh6UxyMA_eMAAA&S=AQAAAuKMNV3Ge0Gda1U0pA5o2ZY; A3=d=AQABBJ0TZWYCEHSNoZBDb-Q5uf6aUH9pQl4FEgEBAQFlZmZuZh6UxyMA_eMAAA&S=AQAAAuKMNV3Ge0Gda1U0pA5o2ZY; cmp=t=1718240856&j=0&u=1---; axids=gam=y-3aU0E0lE2uLdwTSx9lUT901LczQS5B4b~A&dv360=eS12elAwNTNORTJ1RzI0SEk5QktYdGllaWxwV3pKZkJBOH5B&ydsp=y-Wfo6s65E2uJOdr43jqqGxqBHUD08jT2i~A&tbla=y-56ZB2jJE2uL15oKb19ww2WVQNoku1kAa~A; tbla_id=9ab3e279-51d5-4885-aaf1-e330c989310b-tuctd5e9923; PRF=t%3DYM%253DF%252BES%253DF%252B%255ESPX; A1S=d=AQABBJ0TZWYCEHSNoZBDb-Q5uf6aUH9pQl4FEgEBAQFlZmZuZh6UxyMA_eMAAA&S=AQAAAuKMNV3Ge0Gda1U0pA5o2ZY; gpp=DBAA; gpp_sid=-1',
                'sec-fetch-dest':'empty',
                'sec-fetch-mode':'cors',
                'sec-fetch-site':'same-site',
                'priority':'u=4',
                'te':'trailers'}            
        url = f'https://query1.finance.yahoo.com/v1/finance/quoteType/?symbol={self.ticker}&lang=en-US&region=US'
        # ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
        url = f'https://query2.finance.yahoo.com/v8/finance/chart/{tickerurlencoded}?period1={self.dtIniUnix}&period2={self.dtEndUnix}&interval=1d&includePrePost=true&events=div|split|earn&=&lang=en-US&region=US'
        # url = f'https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{tickerurlencoded}?merge=false&padTimeSeries=true&period1={self.dtIniUnix}&period2={self.dtEndUnix}&type=quarterlyMarketCap,trailingMarketCap,quarterlyEnterpriseValue,trailingEnterpriseValue,quarterlyPeRatio,trailingPeRatio,quarterlyForwardPeRatio,trailingForwardPeRatio,quarterlyPegRatio,trailingPegRatio,quarterlyPsRatio,trailingPsRatio,quarterlyPbRatio,trailingPbRatio,quarterlyEnterprisesValueRevenueRatio,trailingEnterprisesValueRevenueRatio,quarterlyEnterprisesValueEBITDARatio,trailingEnterprisesValueEBITDARatio&lang=en-US&region=US'
        
        r = requests.get(url,  headers=headers_request) # data=self.payload,
        asd = r.json()
        
        df0 = pd.DataFrame(asd['chart']['result'][0]['indicators']['quote'][0], index =asd['chart']['result'][0]['timestamp'] )
        df1 = pd.DataFrame(asd['chart']['result'][0]['indicators']['adjclose'][0], index =asd['chart']['result'][0]['timestamp'] )
        df0.index = [pd.Timestamp(x,unit='s') for x in df0.index]
        df1.index = [pd.Timestamp(x,unit='s') for x in df1.index]
        
        df = pd.concat([df0,df1],axis=1)
        
        return df


