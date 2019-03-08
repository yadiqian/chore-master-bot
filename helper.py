import requests
import os
import psycopg2

def create_conn():
    DATEBASE_URL = os.environ['DATABASE_URL']
    try:
      conn = psycopg2.connect(DATEBASE_URL, sslmode='require')
    except:
      print('Failed to connect.')

    return conn

def getMembers():
  request_params = {'token': os.environ['TOKEN']}
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
      'bot_id': os.environ['BOT_ID'],
      'text': message
    }

    requests.post(url, params = data) 