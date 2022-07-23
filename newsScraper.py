from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import smtplib
import datetime


now = datetime.datetime.now()
# Email content placeholder
content = ''

# Extract Hacker News Stories
def extract_news(url):
    print('Extracting Hacker News Stories.....')
    cont = ''
    cont += ('<b>Hacker News Top Stories:</b>\n' + '<br>' + '-'*50 + '<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
        cont += ((str(i+1) + ' :: ' + tag.text + '\n' + '<br>') if tag.text != 'More' else '')
    return cont

content += extract_news('https://news.ycombinator.com/')
content += ('<br>-------------br>')
content += ('<br><br>End of Message')

# Sending Email
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = 'owaisbhat996@gmail.com'
PASSWORD = ''
TO = ''

print('Composing Email...')

msg = MIMEMultipart()
msg['Subject'] = 'Top News Stories HN [Automated Email] ' + str(now.day) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO
msg.attach(MIMEText(content, 'html'))

print('Initiating Server....')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASSWORD)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()
