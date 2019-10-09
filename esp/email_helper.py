import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import VOLPE_GMAIL_PASSWORD

sender_email = "volpe.notifications@gmail.com"
recipients = [("Tyler", "tyler.gillson@gmail.com"),]


# Connect to Google's SMTP server, then send a series of personalized emails:
def notify_recipients(alert_text):
    # Create a secure SSL context:
    context = ssl.create_default_context()

    # Connect to Gmail's SMTP server (465 is Gmail's SSL port):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, VOLPE_GMAIL_PASSWORD)

        for name, address in recipients:
            message = create_email(name, address, alert_text)
            server.sendmail(sender_email, address, message.as_string())


# Generate a personalised email:
def create_email(name, email_address, alert_text):
    # Initialize MIME message:
    message = MIMEMultipart("alternative")
    message["Subject"] = "VOLPE Safety Alert"
    message["From"] = sender_email
    message["To"] = email_address

    # Create the plain-text and HTML version of your message
    text = f"""\
    Hello {name},
    
    The following Tweet was just posted in your area:
    
    "{alert_text}"
    
    Please see: www.volpe.dot.gov to learn more about how the US DOT Volpe Center is working to keep you safe."""

    html = f"""\
    <html>
      <body>
        <p>Hello {name},<br><br>
           The following Tweet was just posted in your area: "<strong>{alert_text}</strong>"<br><br>
           Learn more about how the <a href="https://www.volpe.dot.gov/">US DOT Volpe Center</a> 
           is working to keep you safe.
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
