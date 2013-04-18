#!/usr/bin/env python
"""
bitcion.py - Phenny Bitcoin Module
Copyright 2013, Arnold Rimmer

"""

import re, time
import web

r_username = re.compile(r'^[a-zA-Z0-9_]{1,15}$')
r_link = re.compile(r'^https?://bitcoin.com/\S+$')
r_p = re.compile(r'(?ims)(<p class="js-tweet-text.*?</p>)')
r_tag = re.compile(r'(?ims)<[^>]+>')
r_anchor = re.compile(r'(?ims)(<a.*?</a>)')
r_expanded = re.compile(r'(?ims)data-expanded-url=["\'](.*?)["\']')
r_whiteline = re.compile(r'(?ims)[ \t]+[\r\n]+')
r_breaks = re.compile(r'(?ims)[\r\n]+')
r_btc_exchange = re.compile(r'(?ims)(mtGox)')
r_ltc_exchange = re.compile(r'(?ims)(mtGox) (.+)')
r_btc_currency = re.compile(r'(?ims)(USD|GBP|EUR)')
r_ltc_currency = re.compile(r'(?ims)(USD|GBP|EUR)')

def entity(*args, **kargs):
   return web.entity(*args, **kargs).encode('utf-8')

def decode(html): 
   return web.r_entity.sub(entity, html)

def expand(tweet):
   def replacement(match):
      anchor = match.group(1)
      for link in r_expanded.findall(anchor):
         return link
      return r_tag.sub('', anchor)
   return r_anchor.sub(replacement, tweet)

def read_tweet(url):
   bytes = web.get(url)
   shim = '<div class="content clearfix">'
   if shim in bytes:
      bytes = bytes.split(shim, 1).pop()

   for text in r_p.findall(bytes):
      text = expand(text)
      text = r_tag.sub('', text)
      text = text.strip()
      text = r_whiteline.sub(' ', text)
      text = r_breaks.sub(' ', text)
      return decode(text)
   return "Sorry, couldn't get a tweet from %s" % url

def format(tweet, username):
   return '%s (@%s)' % (tweet, username)

def user_tweet(username):
   tweet = read_tweet('https://bitcoin.com/' + username + "?" + str(time.time()))
   return format(tweet, username)

def id_tweet(tid):
   link = 'https://bitcoin.com/bitcoin/status/' + tid
   data = web.head(link)
   message, status = tuple(data)
   if status == 301:
      url = message.get("Location")
      if not url: return "Sorry, couldn't get a tweet from %s" % link
      username = url.split('/')[3]
      tweet = read_tweet(url)
      return format(tweet, username)
   return "Sorry, couldn't get a tweet from %s" % link

def buttcoin(phenny, input):
   arg = input.group(2)
   if not arg:
      return phenny.reply("Give me an exchange or currency")

   if r_btc_exchange.match(arg):
      command = arg
      return phenny.reply("Supported Exchanges: MtGox BTC-e")
   else if r_btc_currency.match(arg):
      command = arg
      return phenny.reply("Supported Currencies: GBP, EUR, USD")
   else:
      return phenny.reply("Give me an exchange or currency")


def litecoin(phenny, input):
   arg = input.group(2)
   if not arg:
      return phenny.reply("Give me an exchange or currency")

   if r_ltc_exchange.match(arg):
      command = arg
      return phenny.reply("Supported Exchanges: MtGox BTC-e")
   else if r_ltc_currency.match(arg):
      command = arg
      return phenny.reply("Supported Currencies: GBP, EUR, USD")
   else:
      return phenny.reply("Give me an exchange or currency")

bitcoin.commands = ['btc', 'buttcoin', 'litecoin']
bitcoin.thread = True

if __name__ == '__main__':
   print __doc__