import pandas as pd
import pyodbc
import os
import numpy as np
from html import escape
import workdays as wd
import datetime as dt



def FTECaclulation():
#    StandardHoursUpdate()
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=TCP:N-5CG63020XL\SQLEXPRESS,49172;"
                      "Database=Projects;"
                      "Uid=superuser;Pwd=nokia2018;")

# query to create FTE dataframe - for the tasks which are invoiced based on the agreed no of FTE
    dfFTE = pd.read_sql_query(" SELECT * FROM (SELECT SQLM1.[MONTH], [Project], [SUB-PROJECT], ISNULL(ROUND([SUMBILLLABLE] / [STANDARD_HOURS],2),0) as FTE FROM ( "
                           " SELECT [Project],[SUB-PROJECT], MONTH([RECEIVE DATE]) AS MONTH, SUM([BILLABLE HOURS]) AS SUMBILLLABLE FROM "
                           " ((SELECT [TASKS], [REAL HOURS], [BILLABLE HOURS], [RECEIVE DATE]  FROM [ROMANIA_Report_TimeWriting_Replicated] WHERE [WBS Structure] = 'FRLI000642-FP-GNEC'"
                           " GROUP BY [TASKS], [REAL HOURS], [BILLABLE HOURS], [RECEIVE DATE]) AS SQL1 "
                           " LEFT JOIN (SELECT [Project],[Sub-Project], [Type],[Capacity] FROM [Norms_Capacity]) AS SQL2"
                           " ON SQL1.[TASKS] = SQL2.[Capacity]) WHERE [Type] = 'FTE' GROUP BY [Project], [SUB-PROJECT], [RECEIVE DATE]) AS SQLM1 "
                           " LEFT JOIN "
                           " (SELECT * FROM [StandardHoursCalculation]) as SQLM2 "
                           " ON SQLM2.[MONTH] = SQLM1.[MONTH]) AS BASETABLE "
                           " PIVOT (SUM([FTE]) FOR [MONTH] in ([1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]) ) AS PIVOTTABLE "
                            , cnxn)
# query to create FTE dataframe - for the tasks which are invoiced based on the agreed norm of each operation
    dfTask = pd.read_sql_query(" SELECT * FROM (SELECT SQLM1.[MONTH],[SUB-PROJECT], ROUND([SUMBILLLABLE] / [STANDARD_HOURS],2) as FTE FROM ( "
                           " SELECT [TASKS],[Project],[SUB-PROJECT], MONTH([RECEIVE DATE]) AS MONTH, SUM([BILLABLE HOURS]) AS SUMBILLLABLE FROM "
                           " ((SELECT [TASKS], [REAL HOURS], [BILLABLE HOURS], [RECEIVE DATE] FROM [ROMANIA_Report_TimeWriting_Replicated] WHERE [WBS Structure] = 'FRLI000642-FP-GNEC'"
                           " GROUP BY [TASKS], [REAL HOURS], [BILLABLE HOURS], [RECEIVE DATE]) AS SQL1 "
                           " LEFT JOIN (SELECT [Project],[Sub-Project], [Type], [Capacity] FROM [Norms_Capacity]) AS SQL2"
                           " ON SQL1.[TASKS] = SQL2.[Capacity])  WHERE [Type] = 'Task' GROUP BY [TASKS],[Project], [SUB-PROJECT], [RECEIVE DATE]) AS SQLM1 "
                           " LEFT JOIN "
                           " (SELECT * FROM [StandardHoursCalculation]) as SQLM2 "
                           " ON SQLM2.[MONTH] = SQLM1.[MONTH]) AS BASETABLE "
                           " PIVOT (SUM([FTE]) FOR [MONTH] in ([1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]) ) AS PIVOTTABLE "
                            , cnxn)   
# query to create FTE dataframe - for the main projects
    dfProject = pd.read_sql_query(" SELECT * FROM (SELECT SQLM1.[MONTH], [PROJECT], ROUND([SUMBILLLABLE] / [STANDARD_HOURS],2) as FTE FROM ( "
                           " SELECT [PROJECT], MONTH([RECEIVE DATE]) AS MONTH, SUM([BILLABLE HOURS]) AS SUMBILLLABLE FROM "
                           " ((SELECT [TASKS], [REAL HOURS], [BILLABLE HOURS], [RECEIVE DATE] FROM [ROMANIA_Report_TimeWriting_Replicated] WHERE [WBS Structure] = 'FRLI000642-FP-GNEC'"
                           " GROUP BY [TASKS], [REAL HOURS], [BILLABLE HOURS], [RECEIVE DATE]) AS SQL1 "
                           " LEFT JOIN (SELECT [Project], [Type],[Capacity] FROM [Norms_Capacity]) AS SQL2"
                           " ON SQL1.[TASKS] = SQL2.[Capacity]) GROUP BY [PROJECT], [RECEIVE DATE]) AS SQLM1 "
                           " LEFT JOIN "
                           " (SELECT * FROM [StandardHoursCalculation]) as SQLM2 "
                           " ON SQLM2.[MONTH] = SQLM1.[MONTH]) AS BASETABLE "
                           " PIVOT (SUM([FTE]) FOR [MONTH] in ([1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]) ) AS PIVOTTABLE "
                            , cnxn)   
# query to create FTE dataframe - for the main projects and sub-projects
    dfSubProject = pd.read_sql_query(" SELECT * FROM (SELECT SQLM1.[MONTH], [Project], [SUB-PROJECT], ISNULL(ROUND([SUMBILLLABLE] / [STANDARD_HOURS],2),0) as FTE FROM ( "
                           " SELECT [Project],[SUB-PROJECT], MONTH([RECEIVE DATE]) AS MONTH, SUM([BILLABLE HOURS]) AS SUMBILLLABLE FROM "
                           " ((SELECT [TASKS], [REAL HOURS], [BILLABLE HOURS], [RECEIVE DATE]  FROM [ROMANIA_Report_TimeWriting_Replicated] WHERE [WBS Structure] = 'FRLI000642-FP-GNEC'"
                           " GROUP BY [TASKS], [REAL HOURS], [BILLABLE HOURS], [RECEIVE DATE]) AS SQL1 "
                           " LEFT JOIN (SELECT [Project],[Sub-Project], [Type],[Capacity] FROM [Norms_Capacity]) AS SQL2"
                           " ON SQL1.[TASKS] = SQL2.[Capacity]) GROUP BY [Project], [SUB-PROJECT], [RECEIVE DATE]) AS SQLM1 "
                           " LEFT JOIN "
                           " (SELECT * FROM [StandardHoursCalculation]) as SQLM2 "
                           " ON SQLM2.[MONTH] = SQLM1.[MONTH]) AS BASETABLE "
                           " PIVOT (SUM([FTE]) FOR [MONTH] in ([1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]) ) AS PIVOTTABLE "
                            , cnxn)

    #calculate totals
    dfFTE.loc['Total']= dfFTE.sum()
    dfTask.loc['Total']= dfTask.sum()
    dfProject.loc['Total']= dfProject.sum()
    dfSubProject.loc['Total']= dfSubProject.sum()

    #rename row which contains totals value
    dfFTE.iloc[-1, 0] = 'Totals'
    dfTask.iloc[-1, 0] = 'Totals'
    dfProject.iloc[-1, 0] = 'Totals'
    dfSubProject.iloc[-1, 0] = 'Totals'

    #print to html
    dfFTE.to_html(os.getcwd() + "\\myMsgApp\\templates\\myMsgApp\\resoucecalculationFTE.html", index = False)
    dfTask.to_html(os.getcwd() + "\\myMsgApp\\templates\\myMsgApp\\reportedhourstable.html", index = False)
    dfProject.to_html(os.getcwd() + "\\myMsgApp\\templates\\myMsgApp\\FTEReportingTable.html", index = False)
    dfSubProject.to_html(os.getcwd() + "\\myMsgApp\\templates\\myMsgApp\\resoucecalculationsubproject.html", index = False)



def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + dt.timedelta(days=4)  # this will never fail
    return next_month - dt.timedelta(days=next_month.day)

def StandardHoursUpdate():
    sYear = 2019
    df3 = pd.DataFrame(columns=['START', 'END','STANDARD_HOURS', 'MONTH'])
    df3 = pd.DataFrame(columns=['START', 'END','STANDARD_HOURS', 'MONTH'])
    hollidays = ["2019-01-01"]
    for i in range(1,13):
        start = dt.date(sYear, i, 1)
        end = last_day_of_month(dt.date(sYear, i, 1))
        #hours = wd.networkdays(start, end, ["2019-01-01"])*8
        hours = networkdays(date(2009, 12, 24),date(2009, 12, 28), [ date(year=2009,month=12
,day=25)] )
        SR_row = pd.Series({'START':start,'END':end,'STANDARD_HOURS':hours, 'MONTH':i},name='STANDARD_HOURS')
        df3 = df3.append(SR_row)
        
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=TCP:N-5CG63020XL\SQLEXPRESS,49172;"
                      "Database=Projects;"
                      "Uid=superuser;Pwd=nokia2018;")
    cursor = cnxn.cursor()
    cursor.execute("DELETE FROM dbo.StandardHoursCalculation")
    
    for index,row in df3.iterrows():
        cursor.execute("INSERT INTO dbo.StandardHoursCalculation([MONTH], [STANDARD_HOURS], [START], [END]) values (?,?,?,?)", row['MONTH'],row['STANDARD_HOURS'],row['START'],row['END'] )
#        print(row['STANDARD_HOURS'])
    cnxn.commit()
    cursor.close()
    cnxn.close()



def ReportedHours():
    #StandardHoursUpdate()
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=TCP:N-5CG63020XL\SQLEXPRESS,49172;"
                      "Database=Projects;"
                      "Uid=superuser;Pwd=nokia2018;")

    df = pd.read_sql_query(" "
                           " SELECT * FROM ( "
                           " SELECT SQLM1.[MONTH], [Tasks], [SUMBILLLABLE]/[STANDARD_HOURS] as FTE FROM ( "
                           " SELECT  [TASKS], MONTH([RECEIVE DATE]) AS MONTH, SUM([REAL HOURS]) AS SUMBILLLABLE FROM "
                           " ((SELECT [TASKS], [REAL HOURS], [RECEIVE DATE] FROM [ROMANIA_Report_TimeWriting_Replicated] "
                           " WHERE [WBS STRUCTURE] = 'FRLI000642-FP-GNEC' "
                           " GROUP BY [TASKS], [REAL HOURS], [BILLABLE HOURS], [RECEIVE DATE]) AS SQL1 "
                           " LEFT JOIN (SELECT DISTINCT [Sub-Project], [Type], [Capacity] FROM [Norms_Capacity]) AS SQL2"
                           " ON SQL1.[Tasks] = SQL2.[Capacity]) GROUP BY [Tasks], [REAL HOURS], [RECEIVE DATE]) AS SQLM1 "
                           " LEFT JOIN "
                           " (SELECT * FROM [StandardHoursCalculation]) as SQLM2  "
                           " ON SQLM2.[MONTH] = SQLM1.[MONTH] " # GROUP BY  SQLM1.[MONTH] , [Tasks], [SUMBILLLABLE], [STANDARD_HOURS] "
                           " ) AS BASETABLE "
                           " PIVOT (SUM([FTE]) FOR [MONTH] in ([1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]) ) AS PIVOTTABLE "
                           " ",  cnxn)
    #df(encoding="utf-8-sig")
    #df.at[Capacity.encode("utf-8"), 'Capacity']
    df.Tasks = df.Tasks.str.encode('latin-1',  'ignore')
    df.loc['Total']= df.sum()
    df.iloc[-1, 0] = 'Totals'
    df.to_html(os.getcwd() + "\\myMsgApp\\templates\\myMsgApp\\reportedhourstable.html", index = False)
    escape(os.getcwd() + "\\myMsgApp\\templates\\myMsgApp\\reportedhourstable.html")

def WeeklyUtilisation():
#    StandardHoursUpdate()
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=TCP:N-5CG63020XL\SQLEXPRESS,49172;"
                      "Database=Projects;"
                      "Uid=superuser;Pwd=nokia2018;")


    df = pd.read_sql_query("  "
                                " SELECT * FROM ("
                                " SELECT sql2.Engineer, (sql2.s1 / (40 - sql3.s2)) AS CPAR, WEEK FROM ( "
                                "(SELECT distinct Engineer, sum([Billable Hours]) as s1, datepart(ww,[Receive Date]) AS WEEK from [ROMANIA_Report_TimeWriting_Replicated] WHERE "
                                "[WBS Structure] = 'FRLI000642-FP-GNEC' GROUP BY [Engineer], [Receive Date]) as sql2 "
                                "LEFT JOIN "
                                "(SELECT Engineer, sum([Billable Hours]) as s2, [Receive Date] from [ROMANIA_Report_TimeWriting_Replicated] WHERE "
                                "([WBS Structure] = 'NWH-RO-ABS-01' OR [WBS Structure] = 'ROU-MSD-CL') GROUP BY [Engineer], [Receive Date]) AS sql3 " 
	                            "ON sql2.Engineer = sql3.Engineer ) GROUP BY sql2.Engineer, sql3.s2, sql2.s1, sql2.[WEEK]"
                                " )t"
                               " PIVOT (AVG([CPAR]) FOR [WEEK] in ([1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12]) ) AS PIVOTTABLE "
                               " ",  cnxn)

    df.to_html(os.getcwd() + "\\myMsgApp\\templates\\myMsgApp\\weeklyutilisation.html", index = False)