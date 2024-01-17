#!/usr/bin/env python

""" Email the html report

Usage:
    python src/send_email.py <report_html> <receiver_email>

Example:
    python src/send_email.py docs/report.html kelly.sovacool@nih.gov

"""

import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import sys


def send_email(
    subject="test email from python",
    html_text=None,
    sender="kelly.sovacool@nih.gov",
    receiver="kelly.sovacool@nih.gov",
):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    msg.attach(MIMEText(html_text, "html"))

    server = smtplib.SMTP("localhost")
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()


if __name__ == "__main__":
    html_filename = sys.argv[1]
    receiver_addr = sys.argv[2]

    with open(html_filename, "r") as infile:
        report_html = infile.read()
    send_email(
        subject=f"🚀 spacesavers2 report",
        html_text=report_html,
        receiver=receiver_addr
    )
