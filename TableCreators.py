import pandas as pd
import pyodbc
import os
import numpy as np
from html import escape
import workdays as wd
import datetime as dt

def CapacityTaskExtractor():
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=TCP:N-5CG63020XL\SQLEXPRESS,49172;"
                      "Database=Projects;"
                      "Uid=superuser;Pwd=nokia2018;")


    df = pd.read_sql_query("SELECT * FROM [NORMS_CAPACITY]",  cnxn)
    df.Capacity = df.Capacity.str.encode('utf-8')
    df.to_html(os.getcwd() + "\\myMsgApp\\templates\\myMsgApp\\capacitytaskstable.html", index = False)
    escape(os.getcwd() + "\\myMsgApp\\templates\\myMsgApp\\reportedhourstable.html")