from flask import Flask, request
import requests
import os
import psycopg2
import random
from helper import create_conn, getMembers, sendMessage

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    text = data['text'].split(' ')
    command = text[0]
    if command == '/add':

        num_helper = text[len(text) - 1]
        if len(text) == 3:
            chore = text[1]
        else:
            chore = ' '.join(text[1:len(text) - 1])

        conn = create_conn()
        cur = conn.cursor()
        query = "INSERT INTO chores(name, num_helper) VALUES('" + chore + "', '" + num_helper + "')"
        cur.execute(query)
        conn.commit()
        conn.close()

        sendMessage(chore.upper() + " with " + num_helper + " helper(s) has been added to your chore list.")

    elif data['text'] == '/show chore list':
        conn = create_conn()
        cur = conn.cursor()
        query = "SELECT id, name, num_helper FROM chores"
        cur.execute(query)
        results = cur.fetchall()
        conn.close()

        if not results:
            sendMessage("Chore list is empty.")
        else:
            message = ''
            for entry in results:
                message += str(entry[0]) + '. ' + entry[1].upper() + '\nNumber of helpers: ' + str(entry[2]) + '\n'
            sendMessage(message)

    elif command == '/delete':
        conn = create_conn()
        cur = conn.cursor()
        query = "SELECT name FROM chores WHERE id = " + text[1]
        cur.execute(query)
        results = cur.fetchall()
        if not results:
          sendMessage("Oops! chore does not exist.")
        else:
          chore = results[0][0]
          query = "DELETE FROM chores WHERE id = " + text[1]
          cur.execute(query)

          query = "DELETE FROM chore_assignment WHERE chore = '" + chore + "'"
          cur.execute(query)

          conn.commit()
          conn.close()

          message = chore.upper() + " has been removed from the chore list."
          sendMessage(message)

    elif command == '/reset':
        id = text[1]
        new_num = text[2]
        conn = create_conn()
        cur = conn.cursor()
        query = "SELECT name FROM chores WHERE id = " + id
        cur.execute(query)
        results = cur.fetchall()
        if not results:
          sendMessage("Oops! Chore does not exist.")
        else:
          chore = results[0][0]
          query = "UPDATE chores SET num_helper = " + new_num + " WHERE id = " + id
          cur.execute(query)
          conn.commit()
          conn.close()

          message = chore.upper() +" will need " + new_num + " helper(s) from now on!"
          sendMessage(message)

    elif data['text'] == '/our chores':
        conn = create_conn()
        cur = conn.cursor()
        members = getMembers()
        message = ''

        query = "SELECT chore FROM chore_assignment WHERE name = '" + member + "'"
        cur.execute(query)
        results = cur.fetchall()
        if not results:
            sendMessage("No chores have been assigned yet.")

        for member in members:
            message += member + ': '
            for chore in results:
                message += chore[0] + '\n'

        sendMessage("The chore assignment for this week is as below:\n" + message)

    elif data['text'] == '/my chore':
        conn = create_conn()
        cur = conn.cursor()
        query = "SELECT chore FROM chore_assignment WHERE name = '" + data['name'] + "'"
        cur.execute(query)
        results = cur.fetchall()
        if not results:
            sendMessage("No chores have been assigned to you yet.")
        else: 
            message = ''
            for chore in results:
                message += chore[0] + '\n'

            sendMessage("This week you are responsible for " + message)
       
    return data['text']

