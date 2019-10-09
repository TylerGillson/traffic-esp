import smtplib
import ssl
import reverse_geocoder as rg
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import VOLPE_GMAIL_PASSWORD

sender_email = "volpe.notifications@gmail.com"
recipients = [
    # ("Jordan", "jordan.mowlai@sas.com"),
    # ("Will", "william.taylor@sas.com"),
    # ("Spain", "spain.niemer@sas.com"),
    ("Tyler", "tyler.gillson@sas.com"),

    # Presentation Emails:
    # ("Karl", "karl.quon@sas.com"),
    # ("Ulrike", "ulrike.scheuble@sas.com"),
    # ("Trevor", "trevor.aikin@sas.com"),
    # ("Patrick", "patrick.alcorn@sas.com"),
    # ("Steve", "steve.shirley@sas.com")
]


# Connect to Google's SMTP server, then send a series of personalized emails:
def notify_recipients(alert_text, coordinates, alert_category):
    # Create a secure SSL context:
    context = ssl.create_default_context()

    # Connect to Gmail's SMTP server (465 is Gmail's SSL port):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, VOLPE_GMAIL_PASSWORD)

        for name, address in recipients:
            message = create_email(name, address, alert_text, coordinates, alert_category)
            server.sendmail(sender_email, address, message.as_string())


# Generate a personalised email:
def create_email(name, email_address, alert_text, coordinates, alert_category):
    if coordinates:
        loc_dict = reverse_geocode(coordinates)
        loc = "".join([loc_dict["name"], ',', loc_dict["admin1"], ',', loc_dict["admin2"]])
    else:
        loc = "820 SAS Campus Dr, Cary, NC 27513"

    # Initialize MIME message:
    message = MIMEMultipart("alternative")
    message["Subject"] = f"VOLPE Safety Alert - {alert_category}"
    message["From"] = sender_email
    message["To"] = email_address

    # Create the plain-text and HTML version of your message
    text = f"""\
    Hello {name},
    
    The following Tweet was just posted in your area: "{alert_text}"
    
    Location: {loc}
    
    Please see: www.volpe.dot.gov to learn more about how the US DOT Volpe Center is working to keep you safe."""

    html = f"""\
    <html>
      <body>
        <p>Hello {name},<br><br>
           The following Tweet was just posted in your area: "<strong>{alert_text}</strong>"<br><br>
           Location: {loc}<br><br>
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


# Reverse geocode a (lat, long) tuple to return the country & city:
def reverse_geocode(coordinates):
    return rg.search(coordinates)
