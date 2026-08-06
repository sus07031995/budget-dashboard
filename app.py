import streamlit as st
import pandas as pd
import pyodbc

st.title("Budget Dashboard")

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=odinternal.cgjacecjgzwt.ap-southeast-1.rds.amazonaws.com,1433;"
    "DATABASE=catering_db;"
    "UID=cateringdev-user;"
    "PWD=uh4IMbR8O5ykP2HQAufM;"
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