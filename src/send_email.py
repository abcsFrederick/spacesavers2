#!/usr/bin/env python

""" Email the html report

Usage:
    python src/send_email.py <report_html> <recipient_emails>

Example:
    python src/send_email.py docs/report.html kelly.sovacool@nih.gov
    python src/send_email.py docs/2024/report_2024-01-17.html kelly.sovacool@nih.gov,vishal.koparde@nih.gov

"""

import datetime
from email.message import EmailMessage
import os
import smtplib
import sys


def send_email(
    subject="test email from python",
    plain_text=None,
    html_attach = None,
    sender="kelly.sovacool@nih.gov",
    recipient="kelly.sovacool@nih.gov"
):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    if plain_text:
        msg.set_content(plain_text)
    if html_attach:
        with open(html_attach, 'rb') as file:
            html_data = file.read()
        msg.add_attachment(html_data, 
                           filename = os.path.basename(html_attach),
                           maintype = 'text', subtype = 'html')

    with smtplib.SMTP("localhost") as server:
        server.send_message(msg)


if __name__ == "__main__":
    html_filename = sys.argv[1] if len(sys.argv) > 1 else ''
    recipient_addr = sys.argv[2] if len(sys.argv) > 2 else 'kelly.sovacool@nih.gov'
    send_email(
        subject=f"🚀 spacesavers2 report",
        recipient=recipient_addr,
        plain_text = f"Download the attached report or view it at https://ccbr.github.io/spacesavers2/{html_filename.strip('docs/')}\n\nThis is an automated email.",
        html_attach = html_filename
    )
