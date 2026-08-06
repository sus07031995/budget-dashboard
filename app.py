import streamlit as st
import pandas as pd
import pymssql
import os

st.title("Budget Dashboard")

conn = pymssql.connect(
    server=os.getenv("DB_SERVER").split(",")[0],
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

query = """
SELECT
    FORMAT(StartDate, 'MMM-yyyy') AS Month_Year,
    SUM(Amount) AS Total_Budget,
    SUM(UtilizedAmount) AS Utilized_Amount,
    SUM(Amount) - SUM(UtilizedAmount) AS Variance
FROM Budget
WHERE StartDate IS NOT NULL
    AND CurrencyCode = 'MYR'
    
GROUP BY
    YEAR(StartDate),
    MONTH(StartDate),
    FORMAT(StartDate, 'MMM-yyyy')
ORDER BY
    YEAR(StartDate),
    MONTH(StartDate)
"""

df = pd.read_sql(query, conn)

st.dataframe(df)

conn.close()
