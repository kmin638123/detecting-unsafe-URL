from logging import debug
from flask import Flask, render_template, request, jsonify, make_response
import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd 

import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

from urllib.parse import urlparse
from tld import get_tld

import tensorflow as tf
from keras.models import Sequential
import keras.optimizers
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint


import requests
from bs4 import BeautifulSoup
app = Flask(__name__)


def fd_length(url):
    urlpath= urlparse(url).path
    try:
        return len(urlpath.split('/')[1])
    except:
        return 0
def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits

def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters


def no_of_dir(url):
    urldir = urlparse(url).path
    return urldir.count('/')

def having_ip_address(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        # print match.group()
        return -1
    else:
        # print 'No matching pattern found'
        return 1
def shortening_service(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return -1
    else:
        return 1



@app.route('/', methods = ["GET","POST"])
def index():
    urls = request.form.get('urls').split(',')
    
    normal = request.form.get('test')
    print(normal)
    #print(len(urls))
    urldata = pd.DataFrame(urls, columns=["url"])
    
    urldata['url_length'] = urldata['url'].apply(lambda i: len(str(i)))
    urldata['hostname_length'] = urldata['url'].apply(lambda i: len(urlparse(i).netloc))
    urldata['path_length'] = urldata['url'].apply(lambda i: len(urlparse(i).path))
    urldata['fd_length'] = urldata['url'].apply(lambda i: fd_length(i))
    urldata['count-'] = urldata['url'].apply(lambda i: i.count('-'))
    urldata['count@'] = urldata['url'].apply(lambda i: i.count('@'))
    urldata['count?'] = urldata['url'].apply(lambda i: i.count('?'))
    urldata['count%'] = urldata['url'].apply(lambda i: i.count('%'))
    urldata['count.'] = urldata['url'].apply(lambda i: i.count('.'))
    urldata['count='] = urldata['url'].apply(lambda i: i.count('='))
    #urldata['count-http'] = 0 #urldata['url'].apply(lambda i : i.count('http'))
    #urldata['count-https'] = 0 #urldata['url'].apply(lambda i : i.count('https'))
    #urldata['count-www'] = urldata['url'].apply(lambda i: i.count('www'))
    urldata['count-digits']= urldata['url'].apply(lambda i: digit_count(i))
    urldata['count-letters']= urldata['url'].apply(lambda i: letter_count(i))
    urldata['count_dir'] = urldata['url'].apply(lambda i: no_of_dir(i))
    urldata['use_of_ip'] = urldata['url'].apply(lambda i: having_ip_address(i))
    urldata['short_url'] = urldata['url'].apply(lambda i: shortening_service(i))

    url_data = urldata[['hostname_length',
       'path_length', 'fd_length', 'count-', 'count@', 'count?',
       'count%', 'count.', 'count=','count-digits',
       'count-letters', 'count_dir', 'use_of_ip']]
    #print(url_data['count-www'])
    links = []
    model = keras.models.load_model('./url_MLP_no_www_shuffle.h5')
    #print(urldata)
    #checkpoint = ModelCheckpoint('url_MLP.h5', monitor = 'val', mode  ='max', verbose = 2, save_best_only=True)

    #url_data = url_data.to_numpy().astype(str)
    state =  model.predict(url_data)
    state = state.squeeze()
    print(state)
    
    if normal=="true": ##safety
        state[state<0.7]=0
        state[state>=0.7]=1
    else: ##normal
        state[state<0.55]=0
        state[state>=0.55]=1
    #
    #print(state)
    
    #for e in url_data:
    #    state = model.predict(e)
    #    print(e)
        
    #for e in urldata:
    #    print(model.predict(e.numpy()))
    #print(state)

    return build_actual_response(jsonify(list(state.astype(str)))),200  # serialize and use JSON headers

def build_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def build_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 1024, debug = True)