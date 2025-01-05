# Author: Vikash kumar
# Date: jan 2025
# Description: Service developed for sending cold emails for job hunting.

import telebot
from flask import Flask, request
import smtplib
from email.mime.text import MIMEText

API_TOKEN = "7300246385:AAGIJ0MslmK6Ipz8AWEWk3vqc4DBVrL01cM"
bot = telebot.TeleBot(API_TOKEN)

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Email sending function
def send_email(sender_email,password,receiver_email,name,subject,body):
    try:
        msg = MIMEText(body, "html")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# Telegram Command Handlers
@bot.message_handler(commands=["start"])
def welcome_message(message):
    bot.reply_to(message, "Hello! Send '/sendemail ##sender_email##password##receiver_email##name##subject##body' to trigger an email.")

@bot.message_handler(commands=["sendemail"])
def send_email_command(message):
    try:
        args = message.text.split('##')
        if len(args) < 6:
            bot.reply_to(message, "Usage: /sendemail ##sender email##password##receiver email##name##subject##body")
            return
        sender_email,password,receiver_email,name,subject,body = args[1], args[2], args[3], args[4], args[5], args[6]
        
        # Format email body
        body = body.format(name=name)
        # Send the email
        if send_email(sender_email,password,receiver_email,name,subject,body):
            bot.reply_to(message, f"Email sent successfully to {receiver_email}.")
        else:
            bot.reply_to(message, "Failed to send email. Please try again.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")

# Run Flask App for Telegram Webhook (Optional for Deployment)
app = Flask(__name__)

@app.route("/" + API_TOKEN, methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "OK", 200

if __name__ == "__main__":
    # Use this for local development
    bot.polling()
