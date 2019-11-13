import email 
import imaplib

username = 'floatyboi2k19@gmail.com'
password = 'iamafloatyboi'

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(username, password)