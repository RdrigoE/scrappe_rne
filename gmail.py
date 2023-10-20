from dotenv import dotenv_values
import smtplib

config = dotenv_values(".env")


def send_email(message, lowest_prices):
    gmail_user = config["GMAIL_USER"]
    gmail_password = config["GMAIL_PASSWORD"]
    sent_from = gmail_user
    to = [config["GMAIL_RECIEVER"]]
    subject = lowest_prices[0].priheepece_tag
    body = message

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
        print("Something went wrong….", ex)
