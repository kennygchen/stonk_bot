from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
import discord
import requests
import json
import string
from replit import db
from keep_alive import keep_alive

client = discord.Client()
# url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
# parameters = {'symbol': coin}
# headers = {
#     'Accepts': 'application/json',
#     'X-CMC_PRO_API_KEY': os.environ['COIN'],
# }
# session = Session()
# session.headers.update(headers)

def get_quote():
  url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
  parameters = {'symbol': coin}
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': os.environ['COIN'],
  }
  session = Session()
  session.headers.update(headers)
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  if data['status']['error_code'] == 0:
    global crypto_name
    global current_price
    global percent_chenge_1h
    global percent_chenge_24h
    global coin_slug
    global coin_id
    crypto_name = data['data'][coin][0]['name']
    current_price = data['data'][coin][0]['quote']['USD']['price']
    percent_chenge_1h = data['data'][coin][0]['quote']['USD']['percent_change_1h']
    percent_chenge_24h = data['data'][coin][0]['quote']['USD']['percent_change_24h']
    coin_slug = data['data'][coin][0]['slug']
    coin_id = data['data'][coin][0]['id']
    return True
  else:
    return False


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$'):
        global coin
        coin = message.content.split("$", 1)[1]
        print(coin)
        quote = get_quote()
        if (quote):
            embed = discord.Embed(title="$ " + str(f"{current_price:.8f}"), url="https://coinmarketcap.com/currencies/" + coin_slug, color=discord.Color.blue())
            embed.add_field(name="1h Change", value=str(round(percent_chenge_1h, 2)) + "%", inline=True)
            embed.add_field(name="24h Change", value=str(round(percent_chenge_24h, 2)) + "%", inline=True)
            embed.set_author(name=crypto_name, url="https://coinmarketcap.com/currencies/" + coin_slug, icon_url="https://s2.coinmarketcap.com/static/img/coins/64x64/" + str(coin_id) + ".png")
            await message.channel.send(embed=embed)
        else:
            fail_message = ":x: "+ "Can't find " + coin + "\nMake sure you enter **capital letters**"
            await message.channel.send(fail_message) 
keep_alive()

client.run(os.environ['TOKEN'])
