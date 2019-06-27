import pyodbc
import csv
import sys, os

def SQLtoCSV():
#author: alex@nokia
#description: exports sql server table to csv file
#date: 18/02/2019
#preconditions: connection is to sql server, location of saved file is accesible, table exists on SQL Server
#postconditions: csv file will be uploaded to another sql server
#revision history
#version: 01/18/02/2019

#connect to server
    conn_str = (
        r'Driver={SQL Server};'
        r'Server=135.239.8.244;'
        r'Database=TRM_REP;'
        r'Trusted_Connection=yes;'
        r'uid=nsn-intra\abran, pwd=[windows_pass];'
        )
    #cnxn = pyodbc.connect(conn_str)
    ##execute query for retreiving everything
    #cursor = cnxn.cursor()
    #sql = """Select [Engineer],[Approved by],[WBS Structure],[Comments],CONVERT(varchar, [Receive Date], 101),[Task comments],[Billable Hours],[Real Hours],[Engineer UPI],[Tasks] from dbo.ROMANIA_Report_TimeWriting"""
    #cursor.execute(sql)
    #row = cursor.fetchall()
    ##cursor to csv
    csvpath = r'C:\Users\abran\Desktop\developer version\mysite\Outputs\ROMANIA_Report_TimeWriting2.csv'
    ##print(csvpath)
    #with open(r'C:\Users\abran\Desktop\developer version\mysite\Outputs\ROMANIA_Report_TimeWriting.csv', 'w', 
    #            newline= '') as f:
    #    a = csv.writer(f, delimiter=',')
    #    a.writerow([i[0] for i in cursor.description])
    #    a.writerows(row)
    #cursor.close()
    print('done')
    CSVtoSQL(csvpath)

def CSVtoSQL(csvpath):
#author: alex@nokia
#description: imports csv to sql
#date: 18/02/2019
#preconditions: connection is to sql server, location of saved file is accesible, table exists on SQL Server, file contains data
#postconditions: other scripts will use the data uploaded into this table
#revision history
#version: 01/18/02/2019

#connect to server
    conn_str = (
        r'Driver={SQL Server};'
        r'Server=TCP:N-5CG63020XL\SQLEXPRESS,49172;'
        r'Database=Projects;'
        r'Trusted_Connection=yes;'
        r'uid=superuser, pwd=nokia2018;'
        )
    cnxn = pyodbc.connect(conn_str)
    cursor = cnxn.cursor()
    print('x')
    #delete everything in the table
    sql = """Delete from dbo.ROMANIA_Report_TimeWriting_Replicated"""
    cursor.execute(sql)
    #insert csv file
    cur = cnxn.cursor()
    with open(csvpath, 'r') as f:
        reader = csv.reader(f, delimiter =',')
        columns = next(reader) 
        query = 'insert into dbo.ROMANIA_Report_TimeWriting_Replicated([WBS Structure],[Tasks],[Engineer],[Engineer UPI],[Approved by],[Billable Hours],[HOUR_CODE],[Real Hours],[Receive Date],[Task comments])  values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        print(query)
        for row in reader:
            print(row)
            cur.execute(query, *row)   
            cur.commit()
    cursor.close() 