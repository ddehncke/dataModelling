# Daniel Dehncke & Gabriele Barlacchi
# !/usr/bin/python
import psycopg2
from config import config
from configparser import ConfigParser
import pandas as pd
import numpy as np
from random import shuffle

def common_member(a, b):
    a_set = set(a)
    b_set = set(b)
    if (a_set & b_set):
        return (a_set & b_set)
    else:
       return False

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
    file_data = 'yelp-dataset/' + 'yelp_business.csv'
    data = pd.read_csv(file_data)
    data = data[data['categories'].str.contains("Restaurants")]

    '''
    file_list = 'yelp-dataset/' + 'yelp restaurant categorys2.csv'
    list_cat = pd.read_csv(file_list)
    list_cat = list_cat['Categories'].tolist()

    data_to_insert = []
    for index, row in data.iterrows():
        categories = row['categories']
        split = categories.split(';')
        try:
            split.remove('Restaurants')
            split.remove('Food')
            split.remove('Comfort Food')
            split.remove('Salad')
        except:
            pass
        common = common_member(split, list_cat)
        if(common != False):
            commons = list(common)
            shuffle(commons)
            category = commons[0]
            id_business = row['business_id']
            object = {
                'id_business': id_business,
                'category': category
            }
            data_to_insert.append(object)
        else:
            pass

    for object in data_to_insert:
        business_id = object['id_business']
        category = object['category']
        query = "UPDATE restaurant SET category = '%s' WHERE id_business = '%s';" % (category, business_id)
        cur.execute(query)
        conn.commit()
    cur.close()
    '''
    # DELETE FROM DATABASE THE COLUMNS WITH CATEGORY NULL
    # retrieve all the restaurant with category NULL
    query = "SELECT id_business FROM restaurant WHERE category IS NULL;"
    cur.execute(query)
    rows = cur.fetchall()
    for business in rows:
        business = business[0]
        delete_checkin = "delete from checkin where checkin.business = '%s';" % (business)
        cur.execute(delete_checkin)
        conn.commit()

        delete_review = "delete from review where review.business = '%s';" % (business)
        cur.execute(delete_review)
        conn.commit()

        delete_tip = "delete from tip where tip.business = '%s';" % (business)
        cur.execute(delete_tip)
        conn.commit()

        delete_business = "delete from restaurant where id_business = '%s';" % (business)
        cur.execute(delete_business)
        conn.commit()



















    '''
    # dataset documentation https://www.kaggle.com/yelp-dataset/yelp-dataset/version/6#yelp_business_attributes.csv
    query = "SELECT rest.id_business, rest.geog, ST_X(rest.geog::geometry) as latitude, ST_Y(rest.geog::geometry) as longitude FROM restaurant rest;"
    cur.execute(query)
    rows = cur.fetchall()
    dataframe = pd.DataFrame(rows)
    spatial_index = [0,2,3]
    dataframe[spatial_index].to_csv('spatial_info.csv')
    '''


















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

    # INSERT RESTAURANT

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


    # INSERT TIPS
    
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
    

    # INSERT REVIEW
    
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


















