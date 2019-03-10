import requests
import os
import psycopg2
from helper import create_conn, getMembers, increment, sendMessage 
import datetime

def chore_switch():
    members = getMembers()
    conn = create_conn()
    cur = conn.cursor()
    query = "SELECT name FROM chore_assignment"
    cur.execute(query)
    past_assignment = cur.fetchall()

    query = "SELECT name, num_helper FROM chores"
    cur.execute(query)
    chore_list = cur.fetchall()

    if past_assignment:
        # if a member from the previous week's assignment is still in the chat, add that member to curMembers
        curMembers = []
        for person in past_assignment:
            if person[0] in members:
                curMembers.append(person[0])

        # remove duplicates
        members = []
        for person in curMembers:
            if person not in members:
                members.append(person)

        # reorder curMember list
        member = members[0]
        members.remove(member)
        members.append(member)

        query = "DELETE FROM chore_assignment"
        cur.execute(query)
        conn.commit()


    index = 0
    count = 0
    for chore in chore_list:
        name = chore[0]
        num_helper = int(chore[1])
        count += num_helper
        while num_helper > 0:
            query = "INSERT INTO chore_assignment(name, chore) VALUES('" + members[index] + "', '" + name + "')"
            cur.execute(query)
            conn.commit()
            index = increment(index, len(members))
            num_helper -= 1 
    while count % len(members):
        query = "INSERT INTO chore_assignment(name, chore) VALUES('" + members[index] + "', 'NULL')"
        cur.execute(query)
        conn.commit()
        index = increment(index, len(members))
        count += 1

    message = ''
    for member in members:
        query = "SELECT chore FROM chore_assignment WHERE name = '" + member + "'"
        cur.execute(query)
        results = cur.fetchall()
        message += member + ': '
        for chore in results:
            message += chore[0] + '\n'

    sendMessage("The chore assignment for this week is as below:\n" + message)

    conn.close()

if __name__ == '__main__':

    today = datetime.datetime.today()
    if today.weekday() == 0:  #sunday
        chore_switch()
    