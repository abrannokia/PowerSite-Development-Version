import pandas as pd
import pyodbc
import os

#from Python.Display import HTML

def TaskCalculation():

    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=TCP:N-5CG63020XL\SQLEXPRESS,49172;"
                      "Database=Projects;"
                      "Uid=superuser;Pwd=nokia2018;")

    df = pd.read_sql_query(" SELECT * FROM (SELECT [SUB-PROJECT], MONTH([RECEIVE DATE]) AS MOUNTH, SUM([BILLABLE HOURS]) AS SUMBILLLABLE FROM "
                           " ((SELECT [TASKS], [REAL HOURS], [BILLABLE HOURS], [RECEIVE DATE]  FROM [CAPACITY] WHERE [WBS CUSTOMER] = 'FRLI000642-FP-GNEC'"
                           " GROUP BY [TASKS], [REAL HOURS], [BILLABLE HOURS], [RECEIVE DATE]) AS SQL1 "
                           " LEFT JOIN (SELECT * FROM [Norms_Capacity]) AS SQL2"
                           " ON SQL1.[Tasks] = SQL2.[Capacity]) GROUP BY [SUB-PROJECT], [RECEIVE DATE]) AS BASETABLE "
                           " PIVOT (SUM([SUMBILLLABLE]) FOR [MOUNTH] in ([1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]) ) AS PIVOTTABLE "
                            , cnxn)

    print(df)
    
    
    # df.to_html(os.getcwd() + "\\myMsgApp\\templates\\myMsgApp\\test.html")

TaskCalculation()
