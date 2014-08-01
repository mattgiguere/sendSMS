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


__author__ = "Matt Giguere (github: @mattgiguere)"
__maintainer__ = "Matt Giguere"
__email__ = "matthew.giguere@yale.edu"
__status__ = " Development NOT(Prototype or Production)"
__version__ = '0.0.1'


def sendSms(num, msg, emailaddr, prvdr='', smtp='smtp.gmail.com', subj=''):
    """PURPOSE: To send someone a text message"""
    # Create a text/plain message
    msg = MIMEText(msg)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = subj
    msg['From'] = emailaddr
    msg['To'] = you

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP(smtp)
    s.sendmail(me, [you], msg.as_string())
    s.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='This routine will send somone a text message.')
    parser.add_argument(
        'num',
        help='The 10 digit telephone number (e.g., 2025551212).')
    parser.add_argument(
        'msg',
        help='The message you want to send.',
             nargs='?')
    parser.add_argument(
        'emailaddr',
        help='The email address the message will be sent from.',
             nargs='?')
    parser.add_argument(
        'smtp',
        help='(optional) the from email smtp. ' +
             'if not set, this assumes gmail.',
             nargs='?')
    parser.add_argument(
        'prvdr',
        help='(optional) The provider/carrier of the person ' +
             'you want to send the message to. Options are ' +
             '"att", "verizon", "tmobile", "sprint"',
             nargs='?')
    if len(sys.argv) > 4:
        print('use the command')
        print('python sendSms.py num msg [prvdr]')
        sys.exit(2)

    args = parser.parse_args()

    sendSms(int(args.num), args.msg, args.emailaddr, prvdr=args.prvdr)
