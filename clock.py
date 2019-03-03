from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import os
import psycopg2
from functions import create_conn, getMembers, increment, sendMessage

def chore_switch():
    members = getMembers()
    conn = create_conn()
    cur = conn.cursor()
    query = "SELECT chore FROM chore_assignment"
    cur.execute(query)
    past_assignment = cur.fetchall()

    query = "SELECT name, num_helper FROM chores"
    cur.execute(query)
    chore_list = cur.fetchall()

    if not past_assignment:
        index = 0
        for chore in chore_list:
            name = chore[0]
            num_helper = int(chore[1])
            while num_helper > 0:
                query = "INSERT INTO chore_assignment(name, chore) VALUES('" + members[index] + "', '" + name + "')"
                cur.execute(query)
                conn.commit()
                index = increment(index, len(members))
                num_helper -= 1 

    else:
        list = []
        for chore in past_assignment:
            list.append(chore[0])
        current = []
        for chore in chore_list:
            current.append(chore[0])
            if chore[0] not in list:
                num = int(chore[1])
                while num > 0:
                    list.append(chore[0])
        item = list[0]
        list.remove(item)
        list.append(item)

        query = "DELETE FROM chore_assignment"
        cur.execute(query)
        conn.commit()

        index = 0
        for chore in list:
            query = "INSERT INTO chore_assignment(name, chore) VALUES('" + members[index] + "', '" + chore + "')"
            cur.execute(query)
            conn.commit()
            index = increment(index, len(members))

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
    sched = BlockingScheduler()
    sched.add_job(chore_switch, 'cron', day_of_week='sun', hour='0')

sched.start()