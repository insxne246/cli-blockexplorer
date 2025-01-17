from turtlecoin import TurtleCoind
import time
from time import sleep
from datetime import datetime
import json
import sys
from os import system, name  
import urllib.request

default_node_ip = "poolbay.fun"

#ask user if they want to use a custom node
user_node_selection = input("Would you like to use a custom node? y/n: ")
if user_node_selection == "y":

    # Request node IP from user
    while True:
        try:
            rpc_host = input('Daemon IP: ')
            break
        except ConnectionError:
            print("Connection error to node. Please try again.")

else:
    rpc_host = str(default_node_ip) 


#
# COIN CONFIG
#  
rpc_port = 43111
pixld = TurtleCoind(rpc_host, rpc_port)
coin_ticker = "PIXL"
version = "1.1.1"
menu = "0"

#The clear function used in the latest block feature
def clear(): 
  
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear') 


#main menu loop
while menu == "0":
    print("Copyright (c) 2019, The Oscillate developers")
    print(str(coin_ticker) + " Block Explorer v" + str(version))
    print("")
    print("|----------------Options----------------|")
    print("|_______________________________________|")
    print("|                                       |")
    print("|(1). Block Explorer                    |")
    print("|(2). View live current net statistics  |")
    print("|(3). View transaction data             |")
    print("|(4). View Pool Information             |")
    print("|(5). Exit                              |")
    print("|_______________________________________|")

    menu = input("Enter selection: ")

    #blockexplorer
    while menu == "1":

        clear()

        #Hash or Height?
        height_or_hash = input("Do you want to search for a block by height or by hash? (height/hash) : ")

        if height_or_hash == "height":
            # request blockheight from user
            block_height = input("Enter " + str(coin_ticker) + " Block Height: ")
            block_header = pixld.get_block_header_by_height(int(block_height))

            # load our Json for block height input
            block_header_dump = json.dumps(block_header)
            block_header_loads = json.loads(block_header_dump)
        else:
             #request hash from user
             user_block_hash = input("Block height to view: ")
             user_block_hash_data = pixld.get_block_header_by_hash(str(user_block_hash))

             # load our Json for bock hash input
             user_block_hash_data_dumps = json.dumps(user_block_hash_data)
             user_block_hash_data_loads = json.loads(user_block_hash_data_dumps)

        if height_or_hash == "height":

             # use the data from the JSON for height input
             block_size = block_header_loads['result']['block_header']['block_size']
             block_hash = block_header_loads['result']['block_header']['hash']
             block_reward = block_header_loads['result']['block_header']['reward']
             block_tx_count = block_header_loads['result']['block_header']['num_txes']
             block_hashrate = round(block_header_loads['result']['block_header']['difficulty'] / 60 / 1000, 2)
             block_timestamp = block_header_loads['result']['block_header']['timestamp']

        else:
            # use the data from the JSON for hash input
             block_height = user_block_hash_data_loads['result']['block_header']['height']
             block_size = user_block_hash_data_loads['result']['block_header']['block_size']
             block_hash = user_block_hash_data_loads['result']['block_header']['hash']
             block_reward = user_block_hash_data_loads['result']['block_header']['reward']
             block_tx_count = user_block_hash_data_loads['result']['block_header']['num_txes']
             block_hashrate = round(user_block_hash_data_loads['result']['block_header']['difficulty'] / 60 / 1000, 2)
             block_timestamp = user_block_hash_data_loads['result']['block_header']['timestamp']
        

        # convert timestamp to UTC
        timestamp = block_timestamp
        block_date = datetime.fromtimestamp(timestamp)

        clear()

        # Block Explorer GUI, but its CLI
        print("")
        print("                        " + str(coin_ticker) + " Block " + str(block_height) + " Info")
        print("_________________________________________________________________________________")
        print("[-------------------------------------------------------------------------------]")
        print("[         Size: " + str(block_size) + " bytes")
        print("[-------------------------------------------------------------------------------]")
        print("[         Hash: " + str(block_hash))
        print("[-------------------------------------------------------------------------------]")
        print("[         Reward: " + str(block_reward) + " atomic units")
        print("[-------------------------------------------------------------------------------]")
        print("[         Transaction count: " + str(block_tx_count))
        print("[-------------------------------------------------------------------------------]")
        print("[         Net Hashrate: " + str(block_hashrate) + "kh/s")
        print("[-------------------------------------------------------------------------------]")
        print("[         Date: " + str(block_date))
        print("[-------------------------------------------------------------------------------]")
        print("_________________________________________________________________________________")

        # yeet or skeet
        menu = input("Press 1 to check another block, 0 to go back to the menu: ")

        clear()

    #current block information
    while menu == "2":

        clear()

        #Request time interval
        update_time = input("How often do you want to update the info? In seconds: ")

        #so the user doesnt crash their PC
        if update_time == "0":
            print("Update time cannot be zero, setting to 1.")
            update_time = "1"
    
        #loop this shit
        while True:
            #snag that block
            try:
                last_block = pixld.get_last_block_header()
            except(ConnectionError):
                print("Error connecting to daemon!")
                menu = 0

            #load that JSON stuff
            last_block_dump = json.dumps(last_block)
            last_block_loads = json.loads(last_block_dump)

            #then load this stuff
            last_block_height = last_block_loads['result']['block_header']['height']
            last_block_size = last_block_loads['result']['block_header']['block_size']
            last_block_hash = last_block_loads['result']['block_header']['hash']
            last_block_reward = last_block_loads['result']['block_header']['reward']
            last_block_tx_count = last_block_loads['result']['block_header']['num_txes']
            last_block_hashrate = round(last_block_loads['result']['block_header']['difficulty'] / 60 / 1000, 2)
            last_block_timestamp = last_block_loads['result']['block_header']['timestamp']

            clear()

            #yeah. this looks cool
            print("")
            print("                         Latest " + str(coin_ticker) + " Block Data (" + str(last_block_height) + ") Info")
            print("                           Data refreshes every " + update_time + " seconds")
            print("_________________________________________________________________________________")
            print("[-------------------------------------------------------------------------------]")
            print("[         Size: " + str(last_block_size) + " bytes")
            print("[-------------------------------------------------------------------------------]")
            print("[         Hash: " + str(last_block_hash))
            print("[-------------------------------------------------------------------------------]")
            print("[         Reward: " + str(last_block_reward) + " atomic units")
            print("[-------------------------------------------------------------------------------]")
            print("[         Transaction count: " + str(last_block_tx_count))
            print("[-------------------------------------------------------------------------------]")
            print("[         Net Hashrate: " + str(last_block_hashrate) + "kh/s")
            print("[-------------------------------------------------------------------------------]")
            print("_________________________________________________________________________________")
            
            #chill for however long the user said
            time.sleep(int(update_time))
            
            clear()

    while menu == "3":

        #user input
         txn_hash = input("Enter " + str(coin_ticker) + " TXN hash: ")

         # send that data to the daemon, and get the response back
         txn_hash_data = pixld.get_transaction(txn_hash)

        #JSON load
         txn_hash_dump = json.dumps(txn_hash_data)
         txn_hash_loads = json.loads(txn_hash_dump)

        #Information harvest
         txn_amount = txn_hash_loads["result"]["txDetails"]["amount_out"]
         txn_fee = txn_hash_loads["result"]["txDetails"]["fee"]
         txn_block = txn_hash_loads["result"]["block"]["height"]
         txn_size = txn_hash_loads["result"]["txDetails"]["size"]
         txn_size_percentage = round(100 / txn_hash_loads["result"]["block"]["cumul_size"] * txn_size)

        #TXN info gui but cli, you feel?
         print("")
         print("--------Transaction Information----------")
         print("")
         print("Amount: " + str(txn_amount) + " atomic units")
         print("Fee: " + str(txn_fee))
         print("Block: " + str(txn_block))
         print("Size: " + str(txn_size) + " bytes")
         print("Size Percentage of block: " + str(txn_size_percentage) + "%")
         print("")

         menu = input("Press 3 to check another TXN, 0 to go back to the menu: ")
         clear()

    while menu == "4":

        print("Loading pool data.... please wait...")

        pool1 = "https://webpxl.semipool.com/api/pool/stats" #SemiPool (Bobbie)
        pool2 = "http://pool.pxl.pubnodes.com/api/stats" #Pubnodes (Hooftly)
        pool3 = "http://158.69.207.25:8117/stats" #Vano (???)
        pool4 = "http://pxlpool.hopto.org:8117/stats" #Hopto (???)
        pool5 = "https://cnpool.cc/api/pxl/stats" #cnpool (???)
        pool6 = "https://spookypool.nl:8618/stats" #SpookyPool (MunchieHigh420)
        pool7 = "https://pxl.miningpool.fun:8131/stats" #miningpool.fun (???)
        pool8 = "http://poolbay.fun:9000/stats" #POOLBAYYYYY (pxckets)

        pool1_response = urllib.request.urlopen(pool1)
        pool2_response = urllib.request.urlopen(pool2)
        pool3_response = urllib.request.urlopen(pool3)
        pool4_response = urllib.request.urlopen(pool4)
        pool5_response = urllib.request.urlopen(pool5)
        pool6_response = urllib.request.urlopen(pool6)
        pool7_response = urllib.request.urlopen(pool7)
        pool8_response = urllib.request.urlopen(pool8)

        pool1_data = json.loads(pool1_response.read())
        pool2_data = json.loads(pool2_response.read())
        pool3_data = json.loads(pool3_response.read())
        pool4_data = json.loads(pool4_response.read())
        pool5_data = json.loads(pool5_response.read())
        pool6_data = json.loads(pool6_response.read())
        pool7_data = json.loads(pool7_response.read())
        pool8_data = json.loads(pool8_response.read())
        

        pool1_hashrate = pool1_data['pool_statistics']['hashRate'] / 1000
        pool1_miners = pool1_data['pool_statistics']['miners']

        pool2_hashrate = pool2_data['pool']['hashrate'] / 1000
        pool2_miners = pool2_data['pool']['miners']
        pool2_fee = pool2_data['config']['fee']

        pool3_hashrate = pool3_data['pool']['hashrate'] / 1000
        pool3_miners = pool3_data['pool']['miners']
        pool3_fee = pool3_data['config']['fee']

        pool4_hashrate = pool4_data['pool']['hashrate'] / 1000
        pool4_miners = pool4_data['pool']['miners']
        pool4_fee = pool4_data['config']['fee']

        pool5_hashrate = pool5_data['pool']['hashrate'] / 1000
        pool5_miners = pool5_data['pool']['miners']
        pool5_fee = pool5_data['config']['fee']

        pool6_hashrate = pool4_data['pool']['hashrate'] / 1000
        pool6_miners = pool6_data['pool']['miners']
        pool6_fee = pool6_data['config']['fee']

        pool7_hashrate = pool7_data['pool']['hashrate'] / 1000
        pool7_miners = pool7_data['pool']['miners']
        pool7_fee = pool7_data['config']['fee']
        
        pool8_hashrate = pool8_data['pool']['hashrate'] / 1000
        pool8_miners = pool8_data['pool']['miners']
        pool8_fee = pool8_data['config']['fee']

        clear()

        print("")
        print("----Semi-Pool---")
        print("Hash rate: " + str(pool1_hashrate) + "kh/s")
        print("Miners: " + str(pool1_miners))
        print("_______________________")
        print("")
        print("")
        print("----PubNodes----")
        print("Hash rate: " + str(pool2_hashrate) + "kh/s")
        print("Miners: " + str(pool2_miners))
        print("Fee: " + str(pool2_fee) + "%")
        print("_______________________")
        print("")
        print("")
        print("------Vano-----")
        print("Hash rate: " + str(pool3_hashrate) + "kh/s")
        print("Miners: " + str(pool3_miners))
        print("Fee: " + str(pool3_fee) + "%")
        print("_______________________")
        print("")
        print("")
        print("-----Hopto-----")
        print("Hash rate: " + str(pool4_hashrate) + "kh/s")
        print("Miners: " + str(pool4_miners))
        print("Fee: " + str(pool4_fee) + "%")
        print("_______________________")
        print("")
        print("")
        print("-----CNpool----")
        print("Hash rate: " + str(pool5_hashrate) + "kh/s")
        print("Miners: " + str(pool5_miners))
        print("Fee: " + str(pool5_fee) + "%")
        print("_______________________")
        print("")
        print("")
        print("---SpookyPool--")
        print("Hash rate: " + str(pool6_hashrate) + "kh/s")
        print("Miners: " + str(pool6_miners))
        print("Fee: " + str(pool6_fee) + "%")
        print("_______________________")
        print("")
        print("")
        print("--MiningPool--")
        print("Hash rate: " + str(pool7_hashrate) + "kh/s")
        print("Miners: " + str(pool7_miners))
        print("Fee: " + str(pool7_fee) + "%")
        print("_______________________")
        print("")
        print("")
        print("---PoolBay----")
        print("Hash rate: " + str(pool8_hashrate) + "kh/s")
        print("Miners: " + str(pool8_miners))
        print("Fee: " + str(pool8_fee) + "%")
        print("_______________________")
        print("")

        menu = input("Press 0 to go back to the main menu.")

        clear()
        
    # wow atleast recommend this to a friend.
    while menu == "5":
        print("")
        print("https://github.com/pxckets/cli-blockexplorer")
        print("Have a good day :)")
        print("Window will automatically close in 5 seconds...")
        time.sleep(5)
        quit()
menu = 0