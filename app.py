import streamlit as st
import pandas as pd
import pyodbc
import os

st.title("Budget Dashboard")

conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={os.getenv['DB_SERVER']};"
    f"DATABASE={os.getenv['DB_NAME']};"
    f"UID={os.getenv['DB_USER']};"
    f"PWD={os.getenv['DB_PASSWORD']};"
    "TrustServerCertificate=yes;"
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
