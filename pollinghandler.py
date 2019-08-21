import imaplib
import email
import time
import requests
import base64





mail = imaplib.IMAP4_SSL('mail.something.com')
mail.login('mailaddress', 'pass')
api_token = 'token'
# api_url_base = 'base_url'
# headers = {
#         'Authorization': 'Bearer {0}'.format(api_token)
#         }
mail.list()
mail.select('inbox')
result, data = mail.uid('search', None, "ALL")
i = len(data[0].split())
print("number of unseen emails:" + str(i))
for x in range(i):
    latest_email_uid = data[0].split()[x]
    result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    raw_email = email_data[0][1]
    # print(raw_email)
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)
    parsed_email = email.message_from_bytes(raw_email)
    print('From:', parsed_email['From'])
    print('To:', parsed_email['To'])
    print('Date:', parsed_email['Date'])
    #apis

    # d = {'name':parsed_email['From'], 'pop3 attr':email_message}#???
    # res = requests.post(url=base_url+'/api/v1/handler', data= d)
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