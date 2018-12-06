# Daniel Dehncke & Gabriele Barlacchi
# !/usr/bin/python
import psycopg2
from config import config
from configparser import ConfigParser
import pandas as pd
import numpy as np

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()
        return cur, conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    # connect to the database
    cur, conn = connect()
    # get data from csv dataset
    file = 'yelp-dataset/' + 'yelp_checkin.csv'
    data = pd.read_csv(file)
    # dataset documentation https://www.kaggle.com/yelp-dataset/yelp-dataset/version/6#yelp_business_attributes.csv

    # INSERT USER DATA
    '''
    list_nedeed = ['user_id', 'name', 'average_stars', 'friends']
    data = data[list_nedeed]
    print(data.head())

    for index, row in data.iterrows():
        query = 'INSERT INTO user_guest(id_user,name,average_stars,friends) VALUES(%s, %s, %s, %s)'
        split = row['friends'].split(',')
        data_to_insert = (row['user_id'], row['name'], row['average_stars'], split,)
        cur.execute(query, data_to_insert)
        conn.commit()
    cur.close()
    '''

    # INSERT RESTAURANT

    '''
    # take only restaurants
    data = data[data['categories'].str.contains("Restaurants")]
    for index, row in data.iterrows():
        query = 'INSERT INTO restaurant(id_business, name, address, city, state, postal_code, is_open, cusine) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        split = row['categories'].split(';')
        if row['is_open'] == 1:
            row['is_open'] = True
        else:
            row['is_open'] = False
        data_to_insert = (row['business_id'], row['name'], row['city'], row['address'], row['state'], row['postal_code'], row['is_open'], split,)
        cur.execute(query, data_to_insert)
        conn.commit()
    cur.close()

    for index, row in data.iterrows():
        id_business = row['business_id']
        attributes = list()
        curr_row = row.to_dict()
        for key in curr_row:
            if (curr_row[key] == 'True'):
                attributes.append(key)
        query = "UPDATE restaurant SET attribute = %s WHERE id_business = %s"
        data_to_insert = ((attributes,),id_business)
        cur.execute(query, data_to_insert)
        conn.commit()
    cur.close()
    
    
    # INSERT LATITUDE AND LONGITUDE
    for index, row in data.iterrows():
        query_check = "SELECT id_business FROM restaurant WHERE id_business = '%s'" % (row['business_id'])
        cur.execute(query_check)
        if(cur.rowcount):
            query = "UPDATE restaurant SET geog = ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography WHERE id_business = '%s'" % (row['longitude'], row['latitude'], row['business_id'])
            cur.execute(query)
            conn.commit()
    cur.close()
    '''

    # INSERT TIPS
    '''
    for index, row in data.iterrows():
        print(row['business_id'])
        query_check = "SELECT id_business FROM restaurant WHERE id_business = '%s' " % (row['business_id'])  # cercare di mettere tutto in una query
        cur.execute(query_check)
        if(cur.rowcount):
            query = "INSERT INTO tip(id_tip, date, business, user_guest, text) VALUES (%s, %s, %s, %s, %s)"
            data_to_insert = (index, row['date'], row['business_id'], row['user_id'], row['text'])
            cur.execute(query, data_to_insert)
            conn.commit()
    cur.close()
    '''

    # INSERT REVIEW
    '''
    for index, row in data.iterrows():
        business, user = False, False
        query_check = "SELECT id_business FROM restaurant WHERE id_business = '%s'" % (row['business_id'])
        cur.execute(query_check)
        if (cur.rowcount):
            business = True
        query_check = "SELECT id_user FROM user_guest WHERE id_user = '%s'" % (row['user_id'])
        cur.execute(query_check)
        if (cur.rowcount):
            user = True
        if (user and business):
            query = "INSERT INTO review(id_review, evaluation, date, business, user_guest) VALUES (%s, %s, %s, %s, %s)"
            data_to_insert = (row['review_id'], row['stars'], row['date'], row['business_id'], row['user_id'])
            cur.execute(query, data_to_insert)
            conn.commit()
    cur.close()
    '''

    '''
    # INSERT CHECKIN
    for index, row in data.iterrows():
        query_check = "SELECT id_business FROM restaurant WHERE id_business = '%s'" % (row['business_id'])
        cur.execute(query_check)
        if (cur.rowcount):
            query = "INSERT INTO checkin(id_checkin, hour, guests, business, weekday) VALUES (%s, %s, %s, %s, %s)"
            data_to_insert = (index, row['hour'], row['checkins'], row['business_id'], row['weekday'])
            cur.execute(query, data_to_insert)
            conn.commit()
    cur.close()
    '''


















