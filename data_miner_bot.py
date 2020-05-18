import time
import pandas as pd
import numpy as np
from datetime import datetime
import requests
import json
requests.packages.urllib3.disable_warnings()

while True:
    print("executing loop")
    try:
        #hit the API's to retrieve the data
        with requests.get('https://florincoin.info/api/getnetworkhashps', verify=False) as response:
            net_hash_ps = float(response.text)
        with requests.get('https://livenet.flocha.in/api/status?q=getInfo') as response:
            flocha_json = json.loads(response.text)
        with requests.get('https://api.bittrex.com/api/v1.1/public/getmarketsummary?market=btc-flo') as response:
            bitrex_json = json.loads(response.text)
        with requests.get('https://www.miningrigrentals.com/api/v2/info/algo/scrypt') as response:
            rental_json = json.loads(response.text)
        with requests.get('https://api.bittrex.com/api/v1.1/public/getmarketsummary?market=usd-btc') as response:
            bitrex2_json = json.loads(response.text)
        with requests.get('https://www.miningrigrentals.com/api/v2/info/algo/sha256') as response:
            sharental_json = json.loads(response.text)
        with requests.get('https://blockchain.info/q/getdifficulty') as response:
            btc_difficulty = float(response.text)
        with requests.get('https://blockchain.info/q/getblockcount') as response:
            btc_block = float(response.text)
        with requests.get('https://blockchain.info/q/hashrate') as response:
            btc_hashrate = int(response.text)
    

        #construct the current snapshot
        flo_diff = flocha_json['info']['difficulty']
        flo_blocks = flocha_json['info']['blocks']
        btc_diff = btc_difficulty
        btc_blocks = btc_block

        flo_vol = bitrex_json['result'][0]['Volume']
        flo_open_buy = bitrex_json['result'][0]['OpenBuyOrders']
        flo_open_sell = bitrex_json['result'][0]['OpenSellOrders']
        flo_low = bitrex_json['result'][0]['Low']
        flo_high = bitrex_json['result'][0]['High']
        flo_bid = bitrex_json['result'][0]['Bid']
        flo_ask = bitrex_json['result'][0]['Ask']
        flo_baseVol = bitrex_json['result'][0]['BaseVolume']


        btc_vol = bitrex2_json['result'][0]['Volume']
        btc_open_buy = bitrex2_json['result'][0]['OpenBuyOrders']
        btc_open_sell = bitrex2_json['result'][0]['OpenSellOrders']
        btc_low = bitrex2_json['result'][0]['High']
        btc_high = bitrex2_json['result'][0]['Low']
        btc_bid = bitrex2_json['result'][0]['Bid']
        btc_ask = bitrex2_json['result'][0]['Ask']
        btc_baseVol = bitrex2_json['result'][0]['BaseVolume']

        last_flo_btc = bitrex_json['result'][0]['Last']
        last_btc_usd = bitrex2_json['result'][0]['Last']

        scrypt_rent_price = rental_json['data']['suggested_price']['amount']
        scrypt_rigs_avail = rental_json['data']['stats']['available']['rigs']
        scrypt_rigs_rented = rental_json['data']['stats']['rented']['rigs']
        scrypt_30 = rental_json['data']['stats']['prices']['last_30']['amount']

        sha_rent_price = sharental_json['data']['suggested_price']['amount']
        sha_rigs_avail = sharental_json['data']['stats']['available']['rigs']
        sha_rigs_rented = sharental_json['data']['stats']['rented']['rigs']
        sha_30 = sharental_json['data']['stats']['prices']['last_30']['amount']

        cols = ['timestamp', 'FLONetworkHashesPs', 'FLOdifficulty',  'FLOblocks', 'BTChashrate', 'BTCdifficulty', 'BTCblocks',
        'FLOvolume', 'FLOopenBuy', 'FLOopenSell', 'FLOlow', 'FLOhigh', 'FLObid', 'FLOask', 'FLObaseVol',
        'BTCvolume', 'BTCopenBuy', 'BTCopenSell', 'BTClow', 'BTChigh', 'BTCbid', 'BTCask', 'BTCbaseVol',
        'FLOlast', 'BTClast', 'scrypt_price', 'scrypt_avail', 'scrypt_rented', 'scrypt_last30',
        'sha_price', 'sha_avail', 'sha_rented', 'sha_last30']

        #construct the dataframe
        df = pd.DataFrame(columns=cols)
        df.loc[0] = [datetime.utcnow(), net_hash_ps, flo_diff, flo_blocks, btc_hashrate, btc_diff, btc_blocks, flo_vol, flo_open_buy,
                    flo_open_sell, flo_low, flo_high, flo_bid, flo_ask, flo_baseVol, btc_vol, btc_open_buy, btc_open_sell,
                    btc_low, btc_high, btc_bid, btc_ask, btc_baseVol, last_flo_btc, last_btc_usd, scrypt_rent_price,
                    scrypt_rigs_avail, scrypt_rigs_rented, scrypt_30, sha_rent_price, sha_rigs_avail, sha_rigs_rented, sha_30]
        print('****************************')
        print("Last FLO price : " + str(df['FLOlast'][0]))
        print("Last BTC price : " + str(df['BTClast'][0]))
        print('****************************')
    except:
        print("Web query failure, attempting to restart in 30 seconds...")
        time.sleep(30)
        continue
    
    #Open the file, add our row, and save it back down
    existing_df = pd.read_csv('data/FLO_data_miner.csv', index_col=0)
    result_df = existing_df.append(df)
    result_df.to_csv('data/FLO_data_miner.csv')

    print('Added 1, current data point collected count is: '+ str(result_df.shape[0]))
    print("Going back to waiting 5 minutes...")
    time.sleep(60)
    print('4 minutes')
    time.sleep(60)
    print('3 minutes')
    time.sleep(60)
    print('2 minutes')
    time.sleep(60)
    print('1 mintue')
    time.sleep(60)