# IP_Watcher.py #

### A simple Python3 script to check the current IP address. If the IP address has changed it will send an E-mail with the new IP address. ###

### Works on Windows, macOS, or Linux. ###

This python3 script uses a Gmail account to notify you if IP address has changed. This can be useful when you don't have a static IP address but you still need to remotely access your machine. This can be setup to run as a crontab job on Linux and macOS, or as a task scheduler on Windows.  

### Open the IP_Watcher.py file in your favorite text editor of choice. ###

Go to Line 17 > Change the path of the log file to the location of your choice.

Go to Line 35 > Add your "recipient" E-mail address (delete everything in between < >. Should look like = <your.email@goes.here>)

Go to Line 36 > Put the name of your server or machine here.

Go to Line 37 > Put the name of your server or machine here.

Go to Line 38 > Add your "sender" E-mail address (delete everything in between < >. Should look like = <your.email@goes.here>)

Go to Line 39 > Add your "recipient" E-mail address (delete everything in between < >. Should look like = <your.email@goes.here>)

Go to Line 45 > Put your username and passwod (delete everything in between ' '. Should look like = 'username','password'

### Save the file. ###

Setup the crontab job or task scheduler to run the IP_Watcher.py script every 15 minutes.

Note: If your mobile phone carrier supports E-mail via SMS you can even be notified by text message.
