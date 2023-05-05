import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
import argparse

# Define the argument parser
parser = argparse.ArgumentParser(description="Zip a folder and send it via email.")
parser.add_argument("folder_to_zip", help="The directory to zip")

# Parse the arguments
args = parser.parse_args()

# Define the zip file name
zip_file_name = "my_folder.zip"

# Create a zipfile object to store the zipped data
zip_file = zipfile.ZipFile(zip_file_name, "w", zipfile.ZIP_DEFLATED)

# Write the contents of the directory to the zip file
for root, dirs, files in os.walk(args.folder_to_zip):
    for file in files:
        zip_file.write(os.path.join(root, file))

# Close the zip file
zip_file.close()

# Define the email parameters
email_from = "sender@gmail.com"
email_to = ["recepient@gmail.com"]
email_subject = "Zipped folder"
email_body = "Please find attached the zipped folder."

# Define the SMTP server details
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "sender@gmail.com"
smtp_password = "sender_password"

# Create a message object
msg = MIMEMultipart()
msg['From'] = email_from
msg['To'] = COMMASPACE.join(email_to)
msg['Subject'] = email_subject
msg.attach(MIMEText(email_body))

# Add the zipped file as an attachment
with open(zip_file_name, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename= {zip_file_name}")
    msg.attach(part)

# Connect to the SMTP server and send the message
smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
smtp_connection.starttls()
smtp_connection.login(smtp_username, smtp_password)
smtp_connection.sendmail(email_from, email_to, msg.as_string())
smtp_connection.quit()

# Remove the zip file
os.remove(zip_file_name)
