import imaplib
import email
import time
import requests
import base64
import datetime
import MySQLdb

class Poller:
    def __init__(self, name, hostname, username, password, timeout, port):
        self.name = name
        self.hostname = hostname 
        self.username = username
        self.password = password
        self.timeout = timeout
        self.port = port
        self.enable = True
        self.select = 'inbox'
        self.flag = 'UNSEEN' #can be unseen, seen, all
        self.last_activity = datetime.datetime.now()
        self.db = MySQLdb.connect(host="localhost",    
                     user="dbname",         
                     passwd="pass", 
                     db="polling_handler")    
        self.cursor = db.cursor() 
        sql = "INSERT INTO poller(name, hostname, username, password, timeout, port, lastactivity) VALUES (%s, %s, %s, %s, %s, %s, %s)"  
        val = (name, hostname, username, password, timeout, port, last_activity)
        self.cursor.execute(sql, val)
        self.db.commit()

    def _open(self):
        try:
            self.mail = imaplib.IMAP4_SSL(hostname)
            self.mail.login(username, password)
            self.mail.list()
            self.mail.select(self.select)
            return True
        except:
            print("unable to connect host")
            return False

    def _read(self):
        result, data = self.mail.uid('search', None, self.flag)
        i = len(data[0].split())
        print("number of " + self.flag + " emails: " + str(i))
        for x in range(i):
            latest_email_uid = data[0].split()[x]
            result, email_data = self.mail.uid('fetch', latest_email_uid, '(RFC822)')
            raw_email = email_data[0][1]
            # print(raw_email)
            raw_email_string = raw_email.decode('utf-8')
            email_message = email.message_from_string(raw_email_string)
            parsed_email = email.message_from_bytes(raw_email)
            self._from = parsed_email['From']
            self._to = parsed_email['To']
            self._date = parsed_email['Date']
            try:
                self._cc = parsed_email['CC']
            except:
                #do nothing

            # print('From:', parsed_email['From'])
            # print('To:', parsed_email['To'])
            # print('Date:', parsed_email['Date'])
            myfile = open("save_string", 'a')
            myfile.write(email_message.decode('utf-8'))
            myfile.close()
            
            for part in email_message.walk():
                print(part.get_content_type())

                if part.get_content_type() == "text/html":
                    # print(part)
                    body = part.get_payload(decode=True)
                    save_string = str("mail" + str(x) + ".html")
                    myfile = open(save_string, 'a')
                    myfile.write(body.decode('utf-8'))
                    myfile.close()  