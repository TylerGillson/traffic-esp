import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import VOLPE_GMAIL_PASSWORD

sender_email = "volpe-notifications@gmail.com"
recipients = [("Tyler", "tyler.gillson@gmail.com"),]


# Connect to Google's SMTP server, then send a series of personalized emails:
def connect_and_send():
    # Create a secure SSL context:
    context = ssl.create_default_context()

    # Connect to Gmail's SMTP server (465 is Gmail's SSL port):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("volpe-notifications@gmail.com", VOLPE_GMAIL_PASSWORD)

        for name, address in recipients:
            message = create_email(name, address)
            server.sendmail(sender_email, address, message.as_string())


# Generate a personalised email:
def create_email(name, email_address):
    # Initialize MIME message:
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = email_address

    # Create the plain-text and HTML version of your message
    text = f"""\
    Hi {name},
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""

    html = f"""\
    <html>
      <body>
        <p>Hi {name},<br>
           How are you?<br>
           <a href="http://www.realpython.com">Real Python</a> 
           has many great tutorials.
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects:
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message.
    # The email client will try to render the last part first.
    message.attach(part1)
    message.attach(part2)

    return message
