import imaplib
import email

host = 'imap.gmail.com'
user_name = 'marcowandcut@gmail.com'
pass_word = '#nnConv224'



def get_index():
    mail = imaplib.IMAP4_SSL(host)
    mail.login(user_name, pass_word)
    mail.select("inbox")

    _ , search_data = mail.search(None, 'UNSEEN')
    my_index_read_msg = []
    for num in search_data[0].split():
        email_detial = {}
        _, data = mail.fetch(num,'(RFC822)')
        _ , bites = data[0]
        email_msg = email.message_from_bytes(bites)
        # print(email_msg)

        for header in ['subject', 'to', 'from','date']:
            print(f"{header} : {email_msg[header]} ")
            email_detial[header] = email_msg[header]

        for part in email_msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                # print(body)
                email_detial['body'] = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_detial['html_body'] = html_body.decode()
        my_index_read_msg.append(email_detial)
    
    return my_index_read_msg


if __name__ == "__main__":
    my_emails = get_index()
    print(my_emails)
