import imaplib
import email
from email.header import Header, decode_header, make_header
import time
import base64

mail = imaplib.IMAP4_SSL('mail.something.com',993)

mail.login('mail@something.com', 'password')

mail.select('INBOX')
# while True:
result, data = mail.uid('search', None, "ALL")
number = data[0].split()[:5]
print("number of unseen emails:" + str(data[0].split()[:5]))
if result == 'OK':
    for num in data[0].split()[:5]:
        print("#######################################################################################")
        result, data = mail.uid('fetch', num, '(RFC822)')
        # # print data
        if result == 'OK':
            parsed_email = email.message_from_bytes(data[0][1])
            print('From:', parsed_email['From'])
            print('To:', parsed_email['To'])
            print('Date:', parsed_email['Date'])
            print('Subject:', decode_header(parsed_email['Subject']))
            for part in parsed_email.walk():
                if part.is_multipart():
                    # maybe need also parse all subparts
                    continue
                elif part.get_content_maintype() == 'text':
                    text = part.get_payload(decode=True).decode(part.get_content_charset())
                    print('Text:\n', text)
                elif part.get_content_maintype() == 'application' and part.get_content_disposition() == 'attachment':
                    name = decode_header(part.get_filename())
                    body = part.get_payload(decode=True)
                    size = len(body)
                    print('Attachment: "{}", size: {} bytes, starts with: "{}"'.format(name, size, body[:50]))
                else:
                    print('Unknown part:', part.get_content_type())

#sleep(5)
mail.close()
mail.logout()