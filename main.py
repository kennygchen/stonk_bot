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

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {'start': '1', 'limit': '500', 'convert': 'USD'}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': os.environ['COIN'],
}
session = Session()
session.headers.update(headers)


def get_quote():
	response = session.get(url, params=parameters).json()
	json_data = response['data']
	for x in json_data:
		if x['symbol'] == coin:
			global crypto_name
			crypto_name = x['name']
			global current_price
			current_price = x['quote']['USD']['price']
			global coin_slug
			coin_slug = x['slug']
			global coin_id
			coin_id = x['id']
			global percent_chenge_1h
			percent_chenge_1h = x['quote']['USD']['percent_change_1h']
			global percent_chenge_24h
			percent_chenge_24h = x['quote']['USD']['percent_change_24h']
			result = "succcessful"
			'''
      result = crypto_name + "Price:" + "\n" + "$ " + str(round(current_price, 4)) + "\n\n" + "1h Change: " + str(round(percent_chenge_1h, 2)) + "%" 
      '''
			return (result)
	result = "fail"
	# ":x:" + coin + " **is incorrect**\nMake sure you entered as**capital letters**"
	return (result)


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
		quote = get_quote()
		if quote == "succcessful":
			#await message.channel.send(quote)
			embed = discord.Embed(title="$ " + str(f"{current_price:.8f}"),
			                      url="https://coinmarketcap.com/currencies/" +
			                      coin_slug,
			                      color=discord.Color.blue())
			#embed.set_thumbnail(url="https://s2.coinmarketcap.com/static/img/coins/64x64/" + str(coin_id) + ".png")
			#embed.add_field(name="$ " + str(round(current_price, 4)),value="Current Price", inline=False)
			embed.add_field(name="1h Change",
			                value=str(round(percent_chenge_1h, 2)) + "%",
			                inline=True)
			embed.add_field(name="24h Change",
			                value=str(round(percent_chenge_24h, 2)) + "%",
			                inline=True)
			embed.set_author(
			    name=crypto_name,
			    url="https://coinmarketcap.com/currencies/" + coin_slug,
			    icon_url="https://s2.coinmarketcap.com/static/img/coins/64x64/"
			    + str(coin_id) + ".png")
			await message.channel.send(embed=embed)
		else:
			fail_message = ":x: "+ "Can't find " + coin + "\nMake sure you enter **capital letters**"
			await message.channel.send(fail_message)


keep_alive()

client.run(os.environ['TOKEN'])
