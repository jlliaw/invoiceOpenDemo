  
from mssqldb import MssqlDB
import pandas as pd


sqlstr = """
SELECT yearNm, hsnNm, prizenm, count(invoiceAwardTotalCnt) cnt
FROM PrizeCity pc
group by yearNm,hsnNm, prizenm
"""
lstRet = {}
para = {}
with MssqlDB('192.168.56.1', 'invoiceUser', 'invoiceUser', 'DBInvoice') as db:
    lstRet = db.fetchData(sqlstr, **para)

df = pd.DataFrame(lstRet)
pass

df.to_csv('groupData.csv')
#conn = pymssql.connect(server='192.168.56.1', user='invoiceUser', password='invoiceUser', database='DBInvoice')  
# cursor = conn.cursor()  
# cursor.execute("INSERT SalesLT.Product (Name, ProductNumber, StandardCost, ListPrice, SellStartDate) OUTPUT INSERTED.ProductID VALUES ('SQL Server Express', 'SQLEXPRESS', 0, 0, CURRENT_TIMESTAMP)")  
# row = cursor.fetchone()  
# while row:  
#     print("Inserted Product ID : " +str(row[0]))
#     row = cursor.fetchone()  
# conn.commit()
#conn.close()

