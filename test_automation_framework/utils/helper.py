import os
import random
from psycopg2 import Error
from typing import cast

import psycopg2
import csv
import json


from datetime import datetime

class util:

    def __init__(self):  pass

    def GUID(self):
        guid= ""
        szTemp = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
        szHex = "0123456789abcdef-"
        nLen = len(szTemp)

        for num in range(0, nLen):
            r = random.randint(0, 100) % 16
            c = ' '

            match (szTemp[num]):
                case 'x':
                    c = szHex[r]
                case 'y':
                    c = szHex[r & 0x03 | 0x08]
                case '-':
                    c = '-'
                case '4':
                    c = '4'

            c = c if num < nLen else '0'
            guid = guid[:num] + c + guid[num+1:]

        print(datetime.now().strftime('(%Y-%m-%d %H:%M:%S)') , " Generated GUID:", guid)
        return guid
    @staticmethod
    def sortStr(source) -> str:
        i=0
        j=i+1
        tmp=0
        small_char=''
        try:
            while i < len(source) :
                while(j<len(source)):
                    if(source[tmp]>source[j]):
                        tmp=j
                    j+=1
                if i != tmp:
                    small_char = source[tmp]
                    source = source[:tmp] + source[i] + source[tmp+1:]
                    source = source[:i] + small_char + source[i+1:]
                i+=1
                j=i+1
        except Exception as e:
            print(f"An error occurred: {e}")
        return source
    @staticmethod
    def replaceStr(source,target, new )-> str:
        try:
            i=j=start=i_save=0
            while( i < len(source)):
                while(j < len(target) and source[i]==target[j]):
                    if(start==0):
                        start=1
                        i_save=i
                    i+=1
                    j+=1
                if(j==len(target)):
                    j=0
                    i=i_save
                    while(j<len(target)):
                        source = source[:i] + new[j] + source[i+1:]
                        i+=1
                        j+=1
                if(start==1):
                    start=0
                    i=i_save
                    j=0
                i+=1
        except Exception as e:
            print(f"An error occurred: {e}")
        return source
    @staticmethod
    def calcListItems(content):
        datalist=content.split(" ")
        dataDict = {}
        for listItem in datalist:
            if listItem in dataDict:
                dataDict[listItem]+=1
            else:
                dataDict[listItem]=1
        return dataDict

class connection:
    def __init__(self,_host,_dbname,_username,_password,_port,_sid):
        self.host = _host
        self.dbname=_dbname
        self.username = _username
        self.password = _password
        self.port = _port
        self.sid_db = _sid
        self.conn = None
        self.cur = None

    def pg_connect(self):
        try:
            self.conn = psycopg2.connect(dbname=self.dbname, user=self.username, password=self.password, host=self.host, port=self.port)
            print("Connected to PostgreSQL successfully!")

            self.cur = self.conn.cursor()
            self.cur.execute("SELECT version();")

            db_version = self.cur.fetchone()
            print(f"PostgreSQL version: {db_version}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def pg_disconect(self) -> None:
        # Close the cursor and connection
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def insertRow(self):
        sequence_name='PUT_LR_POSTGRES_TABLE_SEQ'
        try:

            self.cur.execute(f"SELECT nextval('{sequence_name}');")
            next_value = self.cur.fetchone()[0]
            print(f"Next value of the sequence '{sequence_name}': {next_value}")

            with self.conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO LR_POSTGRES_TABLE (RLO, CUSTOMER_ID)
                    VALUES (%s, %s)
                """, (next_value-1, 1225434) )
            self.conn.commit()
        except (Exception, Error) as error:
            print(f"Error: {error}")

class file():
    def __init__(self):  pass
    @staticmethod
    def writeToFile( path, content) -> None:
        try:
            if not os.path.exists(path):
                with open(path, "w") as file:
                    file.write(content)
                    file.write("\n")
            else:
                with open(path, "a") as file:
                    file.write(content)
                    file.write("\n")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            file.close()
    @staticmethod
    def readFile(path) -> str :
        with open(path, 'r') as file:
            content = file.read()
        return content
    @staticmethod
    def readListLines(path) -> list:
        with open(path, 'r') as file:
            lines = file.readlines()
        return lines
    @staticmethod
    def readCvsFile(path) :
        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            # for row in csv_reader:
            #     print(row)  # Each row is a list
        return csv_reader
    @staticmethod
    def readJsonFile(path):
        with open(path, 'r') as file:
            data = json.load(file)  # Converts JSON to Python dictionary
        return data
    @staticmethod
    def writeJsonFile(path,content):
        # Save JSON data to file
        try:
            with open(path, "w",encoding="utf-8") as json_file:
                json.dump(content,  json_file ,indent=4)
        except Exception as e:
            print(f"An error occurred: {e}")

class Jason_util:
    @staticmethod
    def find_value(data, target):
        if isinstance(data, dict):
            for key, value in data.items():
                if value == target:
                    return key, value
                elif isinstance(value, (dict, list)):
                    result = Jason_util.find_value(value, target)
                    if result:
                        return result
        elif isinstance(data, list):
            for item in data:
                result = Jason_util.find_value(item, target)
                if result:
                    return result
        return None

    @classmethod
    def update_value(cls,data, key, target_value, new_value):
        if isinstance(data, dict):
            for k, v in data.items():
                if k == key and v == target_value:
                    data[k] = new_value
                elif isinstance(v, (dict, list)):
                    cls.update_value(v, key, target_value, new_value)
        elif isinstance(data, list):
            for item in data:
                cls.update_value(item, key, target_value, new_value)
