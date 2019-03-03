import requests
import os
import psycopg2

def create_conn():
    DATEBASE_URL =  'postgres://vzendgpylfezft:91651c1337e8e3f9865e09526f7ddf63c079db97656282f1c26e585cd0b2dbdf@ec2-54-83-44-4.compute-1.amazonaws.com:5432/d7dcuq9rk1pa20' #os.environ['DATABASE_URL']
    try:
      conn = psycopg2.connect(DATEBASE_URL, sslmode='require')
    except:
      print('Failed to connect.')

    return conn

def getMembers():
  request_params = {'token': '4ZcUfoSmfyTbUuvzTvQsYtzhfJu7ETrQ7nTE391k'} #{'token': os.environ['TOKEN']}
  response_members = requests.get('https://api.groupme.com/v3/groups/36047146', params = request_params).json()['response']['members']

  list = [];
  for member in response_members:
    list.append(member['nickname'])

  return list

def increment(index, length):
    if index + 1 == length:
        return 0
    return index + 1

def sendMessage(message):
    url = 'https://api.groupme.com/v3/bots/post'
    data = {
      'bot_id': '25aa378e0ef3f24c52600d01ba', # os.environ['BOT_ID'],
      'text': message
    }

    requests.post(url, params = data) 