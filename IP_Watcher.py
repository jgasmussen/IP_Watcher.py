#!/usr/bin/env python

######################################################
#                   IP_Watcher.py                    #
#----------------------------------------------------#
#           Written by: John G. Asmussen             #
#         EGA Technology Specialists, LLC.           #
#                   GNU GPL v3.0                     #
######################################################

from bs4 import BeautifulSoup
from email.mime.text import MIMEText
import urllib.request, urllib.error, urllib.parse
import re
import smtplib

logFile = '/var/log/IP_Watcher.log'

request = urllib.request.urlopen('https://checkip.amazonaws.com').read()

soup = BeautifulSoup(request, "html.parser")
ipaddress = re.search('[0-9]+.[0-9]+.[0-9]+.[0-9]+', str(request)).group(0)

prevIp = 'ipaddress'

try:
    with open(logFile,'r') as log:
        prevIp = log.readline()
        log.close()

except IOError:
    pass

if (ipaddress != prevIp):
    for recipient in ['<[EMAIL ADDRESS GOES HERE]>']:
        msg = MIMEText('The NEW IP Address of [MACHINE NAME GOES HERE] is: '+ipaddress)
        msg['Subject'] = 'The IP Address of [MACHINE NAME GOES HERE] has changed.'
        msg['From'] = '<[FROM EMAIL ADDRESS GOES HERE]>'
        msg['To'] = '<[TO EMAIL ADDRESS GOES HERE]>'

        mailServer = smtplib.SMTP('smtp.gmail.com', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login('[USERNAME OF FROM EMAIL ADDRESS]','[PASSWORD OF FROM EMAIL ADDRESS]')
        mailServer.sendmail(msg['From'], msg['To'], msg.as_string())
        mailServer.close()

with open(logFile, 'w') as log:
        log.write(ipaddress)
        log.close()
