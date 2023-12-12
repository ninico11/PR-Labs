import gradio as gr
from ftplib import FTP
import smtplib, ssl
import os
from private_data import email,passw

# Function to upload file to FTP server
def upload_to_ftp(filename):
    ftp = FTP("138.68.98.108")
    ftp.login(user="yourusername", passwd="yourusername")
    filename_only = os.path.basename(filename)
    with open(filename, 'rb') as f:
        ftp.storbinary(f"STOR {filename_only}", f)
    ftp.quit()
    return f"http://138.68.98.108/{filename_only}"  # Assuming file accessible via this URL


# Function to send email
def send_email(recipient, subject, body, file):
    port = 465  # For SSL
    password = passw # Input your email password here

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)

        file_url = upload_to_ftp(file)
        body_with_url = f"{body}\n\nFile URL: {file_url}"

        message = f"Subject: {subject}\n\n{body_with_url}"

        server.sendmail(email, recipient, message)


# Define Gradio interface
inputs = [
    gr.Textbox(label="Recipient Address", type="text"),
    gr.Textbox(label="Subject", type="text"),
    gr.Textbox(label="Body", type="text"),
    gr.File(label="File")
]


def mail_client(recipient, subject, body, file):
    send_email(recipient, subject, body, file)
    return "Email Sent Successfully!"


iface = gr.Interface(fn=mail_client, inputs=inputs, outputs="text", title="Mail Client")
iface.launch()
