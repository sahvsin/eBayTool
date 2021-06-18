import smtplib, ssl, getpass
from socket import gaierror
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders



smtp_server = "smtp.gmail.com"
smtp_ports = {'gmail': 587, 'aol': 587, 'local': 1025}
subject = "ALERT! Cheap eBay listing(s) in past 15 minutes!" 




def build_message_with_attachments(sender, destination, text, attachments):
    '''

    '''

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = destination
    message["Subject"] = "ALERT! Cheap eBay Listing(s)!"
    message["Bcc"] = destination

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open("./" + attachments, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=attachments)
    message.attach(part)
    
    return message



def send_email(sender, destination, message, attachments=None, test=None):
    '''
    logs in to the passed email using TLS encryption and sends message to the destination
    '''
    print("Starting UP!\n")
    
    #send to locally (test) 
    if(test):
        try:
            with smtplib.SMTP('localhost', 1025) as server:
                server.sendmail('sender@email.com', 'destination@email.com', subject)
                print("\n\nSENT!\n")

        except ConnectionRefusedError:
            print("Failed to establish a connection! Make sure to have a mail server running before trying this (i.e. postfix, sendmail, simple SMTP)!")


    else:

        if(attachments):
            message = build_message_with_attachments(sender, destination, message, attachments)

        #get the port number most used by the client associated with the email
        client = sender.split('@')[1][:-4]
        port = smtp_ports[client]

        password = getpass.getpass()

        #create the SSL context
        context = ssl.create_default_context()


        try:
            
            #open a connection to the emailing server
            server = smtplib.SMTP(smtp_server, port)
            
            #first encrypt connection
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()

            #login to your account (sender)
            server.login(sender, password)

            #send the email
            server.sendmail(sender, destination, message.as_string())

            print('\nSent\n')
    
        except smtplib.SMTPServerDisconnected as e:
            print('Failed to connect to the server. Wrong user/password to login?')
            print(str(e))
        except(gaierror, ConnectionRefusedError):
            print('Failed to connect to the server. Bad connection settings?')
        except smtplib.SMTPException as e:
            print('SMTP error occured: ' + str(e))
        finally:
            server.quit()

#send_email()
