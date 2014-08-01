#!/usr/bin/env python

"""
Created on 2014-08-01T11:24:43
"""

from __future__ import division, print_function
import sys
import argparse

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
import urllib
import urllib2

import mechanize
from bs4 import BeautifulSoup
import re

__author__ = "Matt Giguere (github: @mattgiguere)"
__maintainer__ = "Matt Giguere"
__email__ = "matthew.giguere@yale.edu"
__status__ = " Development NOT(Prototype or Production)"
__version__ = '0.0.1'


def determineProvider(num):
    """Determine the carrier and return the full address needed
    to email the number of interest."""
    # Browser
    br = mechanize.Browser()

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User-Agent (this is cheating, ok?)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; ' +
                      'en-US; rv:1.9.0.1) ' +
                     'Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    # The site we will navigate into, handling it's session
    br.open('http://www.freecarrierlookup.com')
    br.form['phonenum'] = str(num)
    br.submit()
    html = br.response().read()
    soup = BeautifulSoup(html)
    phoneTab = soup.find('div', {"class": "yellowbox"})
    columns = phoneTab.find_all('td')
    number = columns[7]
    m = re.findall('>(.*)<', str(number))
    return m[0].strip()


def getSuffix(prvdr):
    """Get the suffix if the provider is known."""
    if prvdr == 'att':
        return '@txt.att.net'
    elif prvdr == 'verizon':
        return '@vtext.com'
    elif prvdr == 'tmobile':
        return '@tmomail.net'
    elif prvdr == 'sprint':
        return '@pm.sprint.com'
    elif prvdr == 'uscellular':
        return '@email.uscc.net'
    elif prvdr == 'vmobile':
        return '@vmobl.com'


def sendSms(num, msg, emailaddr, pwd, prvdr, subj, smtp, port, uname):
    """PURPOSE: To send someone a text message"""

    #Testing
    print('num is: ', num)
    print('msg is: ', msg)
    print('emailaddr is: ', emailaddr)
    print('uname is: ', uname)
    #print('pwd is: ', pwd)
    print('smtp is: ', smtp)
    print('port is: ', port)
    print('prvdr is: ', prvdr)
    print('subj is: ', subj)

    #make sure prvdr is lowercase:
    prvdr = prvdr.lower()

    # Create a text/plain message
    msg = MIMEText(msg)

    if prvdr == '':
        toaddr = determineProvider(num)
    else:
        toaddr = str(num)+getSuffix(prvdr)

    msg['Subject'] = subj
    msg['From'] = emailaddr
    msg['To'] = toaddr

    # Send the message
    s = smtplib.SMTP(smtp+":"+port)
    s.starttls()
    s.login(emailaddr, pwd)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This routine will send somone a text message.')
    parser.add_argument(
        'num',
        help='The 10 digit telephone number (e.g., 2025551212).')
    parser.add_argument(
        'msg',
        help='The message you want to send.')
    parser.add_argument(
        'emailaddr',
        help='The email address the message will be sent from.')
    parser.add_argument(
        'pwd',
        help='The password of the emailaddr the message will be sent from.')
    parser.add_argument(
        'prvdr',
        help='(optional) The provider/carrier of the person ' +
             'you want to send the message to. Options are ' +
             '"att", "verizon", "tmobile", "sprint", "uscellular", "vmobile"',
             nargs='?')
    parser.add_argument(
        'subj',
        help='(optional) the subject of the message. ',
             nargs='?')
    parser.add_argument(
        'smtp',
        help='(optional) the from email smtp. ' +
             'if not set, this assumes gmail.',
             nargs='?')
    parser.add_argument(
        'port',
        help='[optional] the smtp port. ' +
             'if not set, this assumes gmail (587).',
             nargs='?')
    parser.add_argument(
        'uname',
        help='The username of the emailaddr the message will be sent from.',
        nargs='?')
    if len(sys.argv) > 10:
        print('use the command')
        cmd = ('python sendSms.py num msg '
               'emailaddr uname pwd [smtp] [port] [prvdr] [subj]')
        print(cmd)
        sys.exit(2)

    parser.set_defaults(prvdr='', smtp='smtp.gmail.com', port='587', subj='')
    args = parser.parse_args()
    parser.set_defaults(uname=args.emailaddr)

    sendSms(int(args.num), args.msg, args.emailaddr, args.pwd,
            args.prvdr, args.subj, args.smtp, args.port, args.uname)
