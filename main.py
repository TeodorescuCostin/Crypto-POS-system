import json
import os.path as op
import os
import sys
import subprocess
import glob
from os import path
import secrets
import time
import random
import requests
import kivy
import blockcypher
import pymongo
from pymongo import MongoClient
from bitcoin import *
from kivymd.app import MDApp
from pymongo import MongoClient
from kivy import *
from kivy.clock import Clock
from pywallet import wallet
from kivy.properties import NumericProperty
from kivy.uix.button import ButtonBehavior
from kivymd.uix.button import MDRectangleFlatButton
from forex_python.converter import CurrencyRates
from kivy_garden.qrcode import QRCodeWidget
from kivy.app import App
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import Config
from escpos import BluetoothConnection
from escpos.impl.epson import GenericESCPOS
from kivy.properties import (StringProperty, NumericProperty, BooleanProperty)
from kivy.uix.togglebutton import ToggleButton
from kivy.animation import Animation
from kivy.core.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle,Canvas,Line
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, FadeTransition



global password_text
password_text = ""

############################################
# First screen where you introduce the sum #
############################################

class WindowSum(Screen):
    entry = ObjectProperty(None)
    button1 = ObjectProperty(None)
    button2 = ObjectProperty(None)
    button3 = ObjectProperty(None)
    button4 = ObjectProperty(None)
    button5 = ObjectProperty(None)
    button6 = ObjectProperty(None)
    button7 = ObjectProperty(None)
    button8 = ObjectProperty(None)
    button9 = ObjectProperty(None)
    button0 = ObjectProperty(None)
    buttonerase = ObjectProperty(None)
    plata = ObjectProperty(None)

    buttonbtc = ObjectProperty(None)
    buttoneth = ObjectProperty(None)
    buttonltc = ObjectProperty(None)
    buttontrx = ObjectProperty(None)
    buttonusdt = ObjectProperty(None)
    buttonsks = ObjectProperty(None)
    labelbtc = ObjectProperty(None)
    labeleth = ObjectProperty(None)
    labelltc = ObjectProperty(None)
    labeltrx = ObjectProperty(None)
    labelusdt = ObjectProperty(None)
    labelsks = ObjectProperty(None)


################################################
# Function for buttons to add in the text area #
################################################


    def btn(self, text):
        priv = self.ids.entry.text
        priv = str(priv)
        if priv[:1] == "0":
            s = priv[-2:-1] + "." + priv[-1:] + f'{text}'
            self.ids.entry.text = s
        else:
            s = priv[:-3] + priv[-2:-1] + "." + priv[-1:] + f'{text}'
            self.ids.entry.text = s


####################################################
# Function for button to delete from the text area #
####################################################


    def btners(self):
        priv = self.ids.entry.text
        priv = str(priv)
        if len(priv) == 4:
            self.ids.entry.text = "0" + "." + priv[-4:-3] + priv[-2:-1]
        else:
            self.ids.entry.text = priv[:-4] + "." + priv[-4:-3] + priv[-2:-1]


################################################################################
# Function that calls all the functions wich call the apis for the coin prices #
################################################################################


    def all(self, *args):
        btc(self)
        eth(self)
        ltc(self)
        dash(self)
        usdt(self)
        sks(self)

###########################################################################################################################
# Function wich verifies the sum and then calls the function wich changes the screen and the function wich calls the apis #
###########################################################################################################################


    def b(self):
        l = float(self.manager.get_screen('wsum').ids.entry.text)
        if l >= 10:
            open('info.txt', 'w').close()
            Clock.schedule_once(self.all, 0.8)
            Clock.schedule_once(self.ch, 5)
        else:
            self.manager.current = 'eroare'


####################################
# Function wich changes the screen #
####################################


    def ch(self, *args):
        if self.manager.get_screen('wcoin').ids.labelbtc.text != '':
            self.manager.current = 'wcoin'

    pass

########################################################################
# Second screen where it will be a photo untill the third screen loads #
########################################################################

class LoadingScreen(Screen):
    pass

################################################################################
# The class wich helps with getting the data about the curent price of RON/USD #
################################################################################

url = 'https://api.exchangerate-api.com/v4/latest/USD'

class CurrencyConverter():
    def __init__(self,url):
        self.data= requests.get(url).json()
        self.currencies = self.data['rates']


    def convert(self, from_currency, to_currency, amount):
        # first convert it into USD
        amount = amount / self.currencies[from_currency]

        # limiting the precision to 4 decimal places
        amount = round(amount * self.currencies[to_currency], 4)
        return amount



###########################################################################################################
# Function wich gets the price of the crypto/fiat given and then returns the price for the sum you decide #
###########################################################################################################

def convertToFiat(crypto, fiat, amount):
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=" + fiat + "&ids=" + crypto
    s = requests.get(url)
    if s.status_code == 200:
        data = s.text
        jdata = json.loads(data)
        conversionRate = jdata[0]['current_price']
        price = amount / conversionRate
        return price



###############################################
# Function wich converts the sum into Bitcoin #
###############################################

def btc(self):
    s = self.manager.get_screen('wsum').ids.entry.text
    g = float(s) * 100
    converter = CurrencyConverter(url)
    amount = converter.convert('RON', 'USD', g)
    response = convertToFiat("bitcoin", "usd", amount)
    p = str(response)[:8]
    m = p[:2] + "00" + p[2:]
    self.manager.get_screen('wcoin').ids.labelbtc.text = m
    return p

################################################
# Function wich converts the sum into Ethereum #
################################################

def eth(self):
    s = self.manager.get_screen('wsum').ids.entry.text
    g = float(s)
    converter = CurrencyConverter(url)
    amount = converter.convert('RON', 'USD', g)
    response = convertToFiat("ethereum", "usd", amount)
    p = str(response)[:10]
    self.manager.get_screen('wcoin').ids.labeleth.text = p
    return p

################################################
# Function wich converts the sum into Litecoin #
################################################

def ltc(self):
    s = self.manager.get_screen('wsum').ids.entry.text
    g = float(s)
    converter = CurrencyConverter(url)
    amount = converter.convert('RON', 'USD', g)
    response = convertToFiat("litecoin", "usd", amount)
    p = str(response)[:10]
    self.manager.get_screen('wcoin').ids.labelltc.text = p
    return p

############################################
# Function wich converts the sum into DASH #
############################################

def dash(self):
    s = self.manager.get_screen('wsum').ids.entry.text
    g = float(s)
    converter = CurrencyConverter(url)
    amount = converter.convert('RON', 'USD', g)
    response = convertToFiat("dash", "usd", amount)
    p = str(response)[:10]
    self.manager.get_screen('wcoin').ids.labeldash.text = p
    return p

############################################
# Function wich converts the sum into USDT #
############################################

def usdt(self):
    s = self.manager.get_screen('wsum').ids.entry.text
    g = float(s)
    converter = CurrencyConverter(url)
    amount = converter.convert('RON', 'USD', g)
    p = str(amount)[:10]
    self.manager.get_screen('wcoin').ids.labelusdt.text = p
    return p

###########################################
# Function wich converts the sum into SKS #
###########################################

def sks(self):
    s = self.manager.get_screen('wsum').ids.entry.text
    g = float(s)
    converter = CurrencyConverter(url)
    amount = converter.convert('RON', 'USD', g)/10
    p = str(amount)[:10]
    self.manager.get_screen('wcoin').ids.labelsks.text = p
    return p


##############################
# Screen if an error occures #
##############################

class Eroare(Screen):

    texterror = ObjectProperty(None)

########################################################
# Function wich restarts all the parameters in the app #
########################################################

    def restart(self):
        self.manager.get_screen('wsum').ids.entry.text = "0.00"
        self.manager.get_screen('wcoin').ids.labelbtc.text = ""
        self.manager.get_screen('wcoin').ids.labeleth.text = ""
        self.manager.get_screen('wcoin').ids.labelltc.text = ""
        self.manager.get_screen('wcoin').ids.labeldash.text = ""
        self.manager.get_screen('wcoin').ids.labelusdt.text = ""
        self.manager.get_screen('wqr').ids.wallet.text = ""
        self.manager.get_screen('wqr').ids.qrlog.data = ""
        self.manager.get_screen('wqr').ids.coinverify.text = ""
        self.manager.get_screen('wcoin').ids.buttonbtc.state = "normal"
        self.manager.get_screen('wcoin').ids.buttoneth.state = "normal"
        self.manager.get_screen('wcoin').ids.buttonltc.state = "normal"
        self.manager.get_screen('wcoin').ids.buttondash.state = "normal"
        self.manager.get_screen('wcoin').ids.buttonusdt.state = "normal"

    pass

###############################################################################################
# Third screen where you will see the sum convertetd in each coin and you can choose the coin #
###############################################################################################

class WindowCoin(Screen):
    buttonbtc = ObjectProperty(None)
    buttoneth = ObjectProperty(None)
    buttonltc = ObjectProperty(None)
    buttondash = ObjectProperty(None)
    buttonusdt = ObjectProperty(None)
    buttonsks = ObjectProperty(None)
    labelbtc = ObjectProperty(None)
    labeleth = ObjectProperty(None)
    labelltc = ObjectProperty(None)
    labeldash = ObjectProperty(None)
    labelusdt = ObjectProperty(None)
    labelsks = ObjectProperty(None)

    coinverify = ObjectProperty(None)
    qrlog = ObjectProperty(None)
    wallet = ObjectProperty(None)
    platit = ObjectProperty(None)

    back = ObjectProperty(None)

####################################################
# Change the toggle state in favour for btc button #
####################################################

    def buttonstatebtc(self):
        self.manager.get_screen('wcoin').ids.buttoneth.state = "normal"
        self.manager.get_screen('wcoin').ids.buttonltc.state = "normal"
        self.manager.get_screen('wcoin').ids.buttondash.state = "normal"
        self.manager.get_screen('wcoin').ids.buttonusdt.state = "normal"

####################################################
# Change the toggle state in favour for eth button #
####################################################

    def buttonstateeth(self):
        self.manager.get_screen('wcoin').ids.buttonbtc.state = "normal"
        self.manager.get_screen('wcoin').ids.buttonltc.state = "normal"
        self.manager.get_screen('wcoin').ids.buttondash.state = "normal"
        self.manager.get_screen('wcoin').ids.buttonusdt.state = "normal"

####################################################
# Change the toggle state in favour for ltc button #
####################################################

    def buttonstateltc(self):
        self.manager.get_screen('wcoin').ids.buttonbtc.state = "normal"
        self.manager.get_screen('wcoin').ids.buttoneth.state = "normal"
        self.manager.get_screen('wcoin').ids.buttondash.state = "normal"
        self.manager.get_screen('wcoin').ids.buttonusdt.state = "normal"

#####################################################
# Change the toggle state in favour for dash button #
#####################################################

    def buttonstatedash(self):
        self.manager.get_screen('wcoin').ids.buttonbtc.state = "normal"
        self.manager.get_screen('wcoin').ids.buttoneth.state = "normal"
        self.manager.get_screen('wcoin').ids.buttonltc.state = "normal"
        self.manager.get_screen('wcoin').ids.buttonusdt.state = "normal"

#####################################################
# Change the toggle state in favour for usdt button #
#####################################################

    def buttonstateusdt(self):
        self.manager.get_screen('wcoin').ids.buttonbtc.state = "normal"
        self.manager.get_screen('wcoin').ids.buttoneth.state = "normal"
        self.manager.get_screen('wcoin').ids.buttonltc.state = "normal"
        self.manager.get_screen('wcoin').ids.buttondash.state = "normal"

####################################################################################################
# Generates the Bitcoin wallet and then send it into the .txt file and after it updates the labels #
####################################################################################################

    def btcwall(self):

        seed = wallet.generate_mnemonic()
        w = wallet.create_wallet(network="BTC", seed=seed, children=1)
        f = open("info.txt", "a")
        f.write(str(w))
        f.write('\n')
        f.close()
        with open('info.txt', 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            my_string = str(last_line)

            spl_word = "'address': '"
            res = my_string.partition(spl_word)[2]
            split_string = res.split("'", 1)
            substring = split_string[0]

            print(w)
            ad = "usdt:"
            qr = substring
            am = "?amount="
            rs = self.manager.get_screen('wcoin').ids.labelbtc.text
            tot = ad + qr + am + rs
            self.manager.get_screen('wqr').ids.wallet.text = substring
            self.manager.get_screen('wqr').ids.qrlog.data = tot
            self.manager.get_screen('wqr').ids.coinverify.text = "BITCOIN"

#####################################################################################################
# Generates the Ethereum wallet and then send it into the .txt file and after it updates the labels #
#####################################################################################################

    def ethwall(self):


        seed = wallet.generate_mnemonic()
        w = wallet.create_wallet(network="ETH", seed=seed, children=1)
        f = open("info.txt", "a")
        f.write(str(w))
        f.write('\n')
        f.close()
        with open('info.txt', 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            my_string = str(last_line)

            spl_word = "'address': '"
            res = my_string.partition(spl_word)[2]
            split_string = res.split("'", 1)
            substring = split_string[0]

            print(w)
            ad = "usdt:"
            qr = substring
            am = "?amount="
            rs = self.manager.get_screen('wcoin').ids.labeleth.text
            tot = ad + qr + am + rs
            self.manager.get_screen('wqr').ids.wallet.text = substring
            self.manager.get_screen('wqr').ids.qrlog.data = tot
            self.manager.get_screen('wqr').ids.coinverify.text = "ETHEREUM"

#################################################################################################
# Generates the DASH wallet and then send it into the .txt file and after it updates the labels #
#################################################################################################

    def dashwall(self):


        seed = wallet.generate_mnemonic()
        w = wallet.create_wallet(network="DASH", seed=seed, children=1)
        f = open("info.txt", "a")
        f.write(str(w))
        f.write('\n')
        f.close()
        with open('info.txt', 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            my_string = str(last_line)

            spl_word = "'address': '"
            res = my_string.partition(spl_word)[2]
            split_string = res.split("'", 1)
            substring = split_string[0]

            print(w)
            ad = "usdt:"
            qr = substring
            am = "?amount="
            rs = self.manager.get_screen('wcoin').ids.labeldash.text
            tot = ad + qr + am + rs
            self.manager.get_screen('wqr').ids.wallet.text = substring
            self.manager.get_screen('wqr').ids.qrlog.data = tot
            self.manager.get_screen('wqr').ids.coinverify.text = "DASH"

#####################################################################################################
# Generates the Litecoin wallet and then send it into the .txt file and after it updates the labels #
#####################################################################################################

    def ltcwall(self):

        seed = wallet.generate_mnemonic()
        w = wallet.create_wallet(network="LTC", seed=seed, children=1)
        f = open("info.txt", "a")
        f.write(str(w))
        f.write('\n')
        f.close()
        with open('info.txt', 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            my_string = str(last_line)

            spl_word = "'address': '"
            res = my_string.partition(spl_word)[2]
            split_string = res.split("'", 1)
            substring = split_string[0]

            print(w)
            ad = "usdt:"
            qr = substring
            am = "?amount="
            rs = self.manager.get_screen('wcoin').ids.labelltc.text
            tot = ad + qr + am + rs
            self.manager.get_screen('wqr').ids.wallet.text = substring
            self.manager.get_screen('wqr').ids.qrlog.data = tot
            self.manager.get_screen('wqr').ids.coinverify.text = "LITECOIN"

#################################################################################################
# Generates the USDT wallet and then send it into the .txt file and after it updates the labels #
#################################################################################################

    def usdtwall(self):


        seed = wallet.generate_mnemonic()
        w = wallet.create_wallet(network="OMNI", seed=seed, children=1)
        f = open("info.txt", "a")
        f.write(str(w))
        f.write('\n')
        f.close()
        with open('info.txt', 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            my_string = str(last_line)

            spl_word = "'address': '"
            res = my_string.partition(spl_word)[2]
            split_string = res.split("'", 1)
            substring = split_string[0]

            print(w)
            ad = "usdt:"
            qr = substring
            am = "?amount="
            rs = self.manager.get_screen('wcoin').ids.labelusdt.text
            tot = ad + qr + am + rs
            self.manager.get_screen('wqr').ids.wallet.text = substring
            self.manager.get_screen('wqr').ids.qrlog.data = tot
            self.manager.get_screen('wqr').ids.coinverify.text = "USDT"

    pass

##############################################################################
# Function wich verifies the sum from the Bitcoin wallet address for 6 times #
##############################################################################

def verifbtc(self):
    address = self.manager.get_screen('wqr').ids.wallet.text
    sum = self.manager.get_screen('wcoin').ids.labelbtc.text

    count = 0
    while True:
        if count < 6:
            if float(blockcypher.get_total_balance(address, coin_symbol='btc')) >= float(sum[:-3]):
                count = count + 1
                print(count)
                print("a")
                self.manager.current = 'wvrft'
                Clock.schedule_once(self.bun, 3)
                Clock.schedule_once(self.sup, 1)
                break
            else:
                count = count + 1
                print(count)
                time.sleep(6)


        else:

            print("enter2")
            Clock.schedule_once(self.grst, 6)

            break

###############################################################################
# Function wich verifies the sum from the Ethereum wallet address for 6 times #
###############################################################################

def verifeth(self):
    address = self.manager.get_screen('wqr').ids.wallet.text
    sum = self.manager.get_screen('wcoin').ids.labeleth.text

    count = 0
    while True:
        if count < 6:
            if float(blockcypher.get_total_balance(address, coin_symbol='btc')) >= float(sum[:-3]):
                count = count + 1
                print(count)
                print("a")
                self.manager.current = 'wvrft'
                Clock.schedule_once(self.bun, 3)
                Clock.schedule_once(self.sup, 1)
                break
            else:
                count = count + 1
                print(count)
                time.sleep(6)

        else:

            print("enter2")
            Clock.schedule_once(self.grst, 6)
            break

###############################################################################
# Function wich verifies the sum from the Litecoin wallet address for 6 times #
###############################################################################

def verifltc(self):
    address = self.manager.get_screen('wqr').ids.wallet.text
    sum = self.manager.get_screen('wcoin').ids.labelltc.text

    count = 0
    while True:
        if count < 6:
            if float(blockcypher.get_total_balance(address, coin_symbol='btc')) >= float(sum[:-3]):
                count = count + 1
                print(count)
                print("a")
                self.manager.current = 'wvrft'
                Clock.schedule_once(self.bun, 3)
                Clock.schedule_once(self.sup, 1)
                break
            else:
                count = count + 1
                print(count)
                time.sleep(6)

        else:

            print("enter2")
            Clock.schedule_once(self.grst, 6)
            break

###########################################################################
# Function wich verifies the sum from the DASH wallet address for 6 times #
###########################################################################

def verifdash(self):
    address = self.manager.get_screen('wqr').ids.wallet.text
    sum = self.manager.get_screen('wcoin').ids.labeldash.text


    count = 0
    while True:
        if count < 6:
            if float(blockcypher.get_total_balance(address, coin_symbol='btc')) >= float(sum[:-3]):
                count = count + 1
                print(count)
                print("a")
                self.manager.current = 'wvrft'
                Clock.schedule_once(self.bun, 3)
                Clock.schedule_once(self.sup, 1)
                break
            else:
                count = count + 1
                print(count)
                time.sleep(6)

        else:
            print("enter2")
            Clock.schedule_once(self.grst, 6)
            break

###########################################################################
# Function wich verifies the sum from the USDT wallet address for 6 times #
###########################################################################

def verifusdt(self):
    address = self.manager.get_screen('wqr').ids.wallet.text
    sum = self.manager.get_screen('wcoin').ids.labelusdt.text

    count = 0
    while True:
        if count < 6:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            data = [
                ('addr', address)
            ]

            response = requests.post('https://api.omniwallet.org/v2/address/addr/', headers=headers, data=data)
            my_string = str(response.json())
            spl_word = "'value': '"
            res = my_string.partition(spl_word)[2]
            split_string = res.split("'", 1)
            substring = split_string[0]
            if float(substring)  >= float(sum[:-3]):
                count = count + 1
                print(count)
                print("a")
                self.manager.current = 'wvrft'
                Clock.schedule_once(self.bun, 3)
                Clock.schedule_once(self.sup, 1)
                break
            else:
                count = count + 1
                print(count)
                time.sleep(6)

        else:

            print("enter2")
            Clock.schedule_once(self.grst, 6)
            break

###############################################################
# Verify screen wich shows if the money entered in the wallet #
###############################################################

class WindowVeriftick(Screen):
    pass

###########################################################
# Cross screen when the money do not entere in the wallet #
###########################################################

class WindowVerifcros(Screen):
    pass

################################################################
# Waiting screen to see if the money had entered in the wallet #
################################################################

class WindowVerifmain(Screen):
    pass

#######################################################
# Password screen wich permits you to restart the app #
#######################################################

class WindowPassword(Screen):

    eentry = ObjectProperty(None)
    bbutton1 = ObjectProperty(None)
    bbutton2 = ObjectProperty(None)
    bbutton3 = ObjectProperty(None)
    bbutton4 = ObjectProperty(None)
    bbutton5 = ObjectProperty(None)
    bbutton6 = ObjectProperty(None)
    bbutton7 = ObjectProperty(None)
    bbutton8 = ObjectProperty(None)
    bbutton9 = ObjectProperty(None)
    bbutton0 = ObjectProperty(None)
    bbuttonerase = ObjectProperty(None)
    sterge = ObjectProperty(None)

########################################################
# Function wich restarts all the parameters in the app #
########################################################

    def restart(self, *args):
        global password_text
        password_text = ""
        self.ids.eentry.text = ""
        self.manager.get_screen('wsum').ids.entry.text = "0.00"
        self.manager.get_screen('wcoin').ids.labelbtc.text = ""
        self.manager.get_screen('wcoin').ids.labeleth.text = ""
        self.manager.get_screen('wcoin').ids.labelltc.text = ""
        self.manager.get_screen('wcoin').ids.labeldash.text = ""
        self.manager.get_screen('wcoin').ids.labelusdt.text = ""
        self.manager.get_screen('wqr').ids.wallet.text = ""
        self.manager.get_screen('wqr').ids.qrlog.data = ""
        self.manager.get_screen('wqr').ids.coinverify.text = ""
        self.manager.current = 'wsum'
        self.manager.get_screen('wcoin').ids.buttonbtc.state = "normal"
        self.manager.get_screen('wcoin').ids.buttoneth.state = "normal"
        self.manager.get_screen('wcoin').ids.buttonltc.state = "normal"
        self.manager.get_screen('wcoin').ids.buttondash.state = "normal"
        self.manager.get_screen('wcoin').ids.buttonusdt.state = "normal"

#######################################################
# Function writes into the text input of the password #
#######################################################

    def comp(self, text):
        global password_text
        priv = self.ids.eentry.text
        if len(password_text) < 4:
            password_text = password_text + f'{text}'
            self.ids.eentry.text = f'{priv}*'

########################################################
# Function deletes from the text input of the password #
########################################################

    def ster(self):
        global password_text
        p = self.ids.eentry.text
        if len(self.ids.eentry.text) > 1:
            p = p[:-1]
            self.ids.eentry.text = p
            password_text = password_text[:-1]
        else:
            password_text = ""
            self.ids.eentry.text = ""

#############################################
# Function verifies if the password is good #
#############################################

    def ver(self):
        global password_text
        comp = "1234"
        if password_text == comp:
            Clock.schedule_once(self.restart, 0)
            self.manager.current = 'wsum'


    pass

####################################################################
# Fourth screen on wich it will be displaied the QR and the wallet #
####################################################################

class WindowQr(Screen):

    buttonbtc = ObjectProperty(None)
    buttoneth = ObjectProperty(None)
    buttonltc = ObjectProperty(None)
    buttonxrp = ObjectProperty(None)
    buttonusdt = ObjectProperty(None)
    buttonsks = ObjectProperty(None)

    coinverify = ObjectProperty(None)
    qrlog = ObjectProperty(None)
    wallet = ObjectProperty(None)
    platit = ObjectProperty(None)
    cancel = ObjectProperty(None)


    def sup(self, *args):
        Clock.schedule_once(self.restart, 1)

    def bun(self, *args):
        self.manager.current = 'wsum'

    def grst(self, *args):
        self.manager.current = 'wvrfc'
        Clock.schedule_once(self.test, 3)


    def test(self, *args):
        self.manager.current = 'wqr'



########################################################
# Function wich restarts all the parameters in the app #
########################################################

    def restart(self, *args):
        global password_text
        password_text = ""
        self.manager.get_screen('wsum').ids.entry.text = "0.00"
        self.manager.get_screen('wcoin').ids.labelbtc.text = ""
        self.manager.get_screen('wcoin').ids.labeleth.text = ""
        self.manager.get_screen('wcoin').ids.labelltc.text = ""
        self.manager.get_screen('wcoin').ids.labeldash.text = ""
        self.manager.get_screen('wcoin').ids.labelusdt.text = ""
        self.manager.get_screen('wqr').ids.wallet.text = ""
        self.manager.get_screen('wqr').ids.qrlog.data = ""
        self.manager.get_screen('wqr').ids.coinverify.text = ""
        self.manager.get_screen('wcoin').ids.buttonbtc.state = "normal"
        self.manager.get_screen('wcoin').ids.buttoneth.state = "normal"
        self.manager.get_screen('wcoin').ids.buttonltc.state = "normal"
        self.manager.get_screen('wcoin').ids.buttondash.state = "normal"
        self.manager.get_screen('wcoin').ids.buttonusdt.state = "normal"



    def decide(self, *args):
        if self.manager.get_screen('wqr').ids.coinverify.text == "BITCOIN":
            verifbtc(self)
        elif self.manager.get_screen('wqr').ids.coinverify.text == "ETHEREUM":
            verifeth(self)
        elif self.manager.get_screen('wqr').ids.coinverify.text == "DASH":
            verifdash(self)
        elif self.manager.get_screen('wqr').ids.coinverify.text == "LITECOIN":
            verifltc(self)
        elif self.manager.get_screen('wqr').ids.coinverify.text == "USDT":
            verifusdt(self)


    def clk(self):
        Clock.schedule_once(self.decide, 3)

    pass


class WindowManager(ScreenManager):
    pass


Window.size = (720, 1240)
kv = Builder.load_file('my.kv')


class myapp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        return kv




if __name__ == '__main__':
    myapp().run()