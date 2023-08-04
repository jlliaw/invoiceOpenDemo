import pymssql
import sys
import traceback
#from mylogging import GetLogger
'''
#logging file initial
'''
#log = GetLogger('logcfg.json', 'specified_logger')


class MssqlDB:

    def __init__(self, server, user, password, dbname):                   
        self.__conn = None
        self.__server = server
        self.__user = user
        self.__password = password
        self.__dbname = dbname        

        try:
            '''
            # pymssql
            '''
            self.__conn = pymssql.connect(server=self.__server, user = self.__user, password= self.__password, database = self.__dbname, charset="utf8") 

            '''
            # pyodbc
            '''
            #cnstr = 'DRIVER={{SQL Server}}; SERVER={0},1433; DATABASE={1}; UID={2}; PWD={3}'
            #cnstr = cnstr.format(self.__server, self.__dbname, self.__user, self.__password)
            #self.__conn = pyodbc.connect(cnstr)
        except Exception as e:
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            #traceback.format_exc() #完整的callstack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料            
            fileName = lastCallStack[0] #取得發生的檔案名稱 lastCallStack.filename
            lineNum = lastCallStack[1] #取得發生的行號 lastCallStack.lineno
            funcName = lastCallStack[2] #取得發生的函數名稱 lastCallStack.name
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            #log.error(errMsg)

    def __enter__(self):        
        return self

    def __exit__(self, type, value, traceback):
        self.__closeConn()

    def __closeConn(self):
        if (self.__isOpen):
            self.__conn.close()
        pass

    def closeConn(self):
        self.__closeConn()

    def getConn(self):
        retconn = None
        if (self.isOpen()):
            retconn = self.__conn

        return retconn

    def fetchData(self, sql, **kwargs):
        rows = None
        desc = None

        

        with self.__conn.cursor() as cur:
            #cur.execute(sql, kwargs)   
            if kwargs == None:
                cur.execute(sql)
            else:
                cur.execute(sql, tuple(kwargs.values()))

            rows = cur.fetchall()        

            # call by assignment / call by reference / call by value
            # inurl:986006 site:stackoverflow.com
            #for c in cur.description:
            #    des.append(c[0])
            desc = [c[0] for c in cur.description]                    

        '''
        # combin column name and tuple value
        # inurl:python-convert-two-lists-into-a-dictionary site:geeksforgeeks.org
        objdic = {}
        objlist =[]        
        for r in rows:
            objdic = {desc[i]: r[i] for i in range(len(desc))}
            objlist.append(objdic)
        '''

        #產生可initial dataframe 的物件格式:{'col1': [1, 2], 'col2': [3, 4]}
        objlist = {}
        for d in desc:
            objlist[d] = [r[desc.index(d)] for r in rows]
        ''''''
        
        return objlist

    def __isOpen(self):
        isopen = False
        try:
            self.__conn.VERSION
            isopen = True
        except Exception as e:
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            #traceback.format_exc() #完整的callstack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料            
            fileName = lastCallStack[0] #取得發生的檔案名稱 lastCallStack.filename
            lineNum = lastCallStack[1] #取得發生的行號 lastCallStack.lineno
            funcName = lastCallStack[2] #取得發生的函數名稱 lastCallStack.name
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            #log.error(errMsg)
            
        return isopen

    def isOpen(self):
        return self.__isOpen()


class SQLServiceModel:
    def __init__(self):
        pass

    def fetch_ews_by_caseno(self, **kwargs):   
        '''
        params: hhisnum, hcaseno
        sql server的paramerter處理方式是轉成tuple.....因此kwargs要先排定sql 對應的順序
        '''
        sql = """
        select * from ews_score where  HHISNUM = %s and HCASENO = %s
        """ 

        lstRet = []

        try:
            with MssqlDB('172.22.249.47', 'apcc4f', 'apcc4f', 'EWS') as db:
                lstRet = db.fetchData(sql, **kwargs)
        except Exception as e:
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            #traceback.format_exc() #完整的callstack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料            
            fileName = lastCallStack[0] #取得發生的檔案名稱 lastCallStack.filename
            lineNum = lastCallStack[1] #取得發生的行號 lastCallStack.lineno
            funcName = lastCallStack[2] #取得發生的函數名稱 lastCallStack.name
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            #log.error(errMsg)

        return lstRet
        

    def fetch_sms_status(self, to_phone, send_time, send_time_next, hhisnum):
        '''
        取得床位資料及caseno最近一次住院時間
        '''
        sql = """
        select
            FromUserID,	ToUserID,	FromPhone,	ToPhone,	MessageBody,	SendTime,	isSend
        from
            SendMessage 
        where
            tophone = %s
            and SendTime >= %s
            and SendTime < %s
            and isSend = 1
            and MessageBody like '%' + 'CKD&ECKD' +'%{0}%'
        order by
            sendtime        
        """        
        sql = sql.format(hhisnum)
        lstRet = []

        try:
            with MssqlDB('172.22.253.34', 'pivr', 'pivrvghtc', 'chtsms') as db:                    
                lstRet = db.fetchData(sql, (to_phone, send_time, send_time_next))
        except Exception as e:
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            #traceback.format_exc() #完整的callstack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料            
            fileName = lastCallStack[0] #取得發生的檔案名稱 lastCallStack.filename
            lineNum = lastCallStack[1] #取得發生的行號 lastCallStack.lineno
            funcName = lastCallStack[2] #取得發生的函數名稱 lastCallStack.name
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            #log.error(errMsg)

        return lstRet

    def add_ews_score(self, waitinsert: list):
        
        sql = """
        INSERT INTO ews_score 
        (STAT_DT, HCASENO, HHISNUM, COMA_V, COMA_S, RESP_V, RESP_S, PULSE_V, PULSE_S, TEMP_V, TEMP_S, SBP_V, SBP_S, SPO2_V, SPO2_S, O2_V, O2_S, TOT_SC, NURBED, PRE_SC, STATUS, AGE, DBP_V, ORIGIN, DATA_TIME)
        VALUES 
        ('2021-05-09 15:00:00.000', '03598855', '001908594A', NULL, 0, 16, 0, 80, 0, 36.7, 0, 140, 0, 96, 0, 1, 2, 2, 'W62-095', NULL, '', 86, 73, NULL, NULL)
        """

        try:
            with MssqlDB('172.22.249.47', 'apcc4f', 'apcc4f', 'EWS') as db:                   
                for w in waitinsert: 
                    db.executeSql(sql, **w)                
        except Exception as e:
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            #traceback.format_exc() #完整的callstack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料            
            fileName = lastCallStack[0] #取得發生的檔案名稱 lastCallStack.filename
            lineNum = lastCallStack[1] #取得發生的行號 lastCallStack.lineno
            funcName = lastCallStack[2] #取得發生的函數名稱 lastCallStack.name
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            #log.error(errMsg)