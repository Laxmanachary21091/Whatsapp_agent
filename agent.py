from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import pyttsx3
import os
from dotenv import load_dotenv

from db import init_db, add_reminder
from agent import call_crewai_parse

# Load environment variables
load_dotenv()

app = Flask(__name__)
scheduler = BackgroundScheduler()
scheduler.start()

init_db()

# ✅ Twilio credentials (add these to your .env file)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")  # e.g., "whatsapp:+14155238886"

# Initialize Twilio client
twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# ---- Reminder Job with Voice AND WhatsApp ----
def send_reminder(msg, phone_number=None):
    """Send reminder via voice AND WhatsApp"""
    print(f"🔔 Reminder triggered: {msg}")
    
    # 1. Voice reminder (local computer)
    try:
        engine = pyttsx3.init()
        engine.say(f"Reminder: {msg}")
        engine.runAndWait()
        print("✅ Voice reminder played")
    except Exception as e:
        print(f"❌ Voice error: {e}")
    
    # 2. WhatsApp message back to user
    if twilio_client and phone_number and TWILIO_WHATSAPP_NUMBER:
        try:
            message = twilio_client.messages.create(
                body=f"🔔 Reminder: {msg}",
                from_=TWILIO_WHATSAPP_NUMBER,
                to=phone_number
            )
            print(f"✅ WhatsApp reminder sent: {message.sid}")
        except Exception as e:
            print(f"❌ WhatsApp send error: {e}")
    else:
        print("⚠️ Twilio not configured - skipping WhatsApp message")

@app.route("/whatsapp", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body")
    from_number = request.form.get("From")  # Get sender's WhatsApp number
    
    print(f"📥 Received message from {from_number}: {incoming_msg}")

    # Call LLM (CrewAI + GPT-4o)
    parsed = call_crewai_parse(incoming_msg)

    if not parsed:
        resp = MessagingResponse()
        resp.message("⚠️ Could not parse reminder. Please include a time/date.")
        return str(resp)

    task = parsed.get("task")
    dt_iso = parsed.get("datetime")
    important = parsed.get("is_important", False)

    # Store in DB
    add_reminder(task, dt_iso, important)

    # Schedule with proper timezone handling
    if dt_iso:
        try:
            # Parse the datetime
            run_time = datetime.datetime.fromisoformat(dt_iso)
            
            # Check if it's in the future
            now = datetime.datetime.now()
            if run_time < now:
                # If time is in the past, assume it's for today/tomorrow
                if run_time.time() > now.time():
                    # Later today
                    run_time = run_time.replace(year=now.year, month=now.month, day=now.day)
                else:
                    # Tomorrow
                    tomorrow = now + datetime.timedelta(days=1)
                    run_time = run_time.replace(year=tomorrow.year, month=tomorrow.month, day=tomorrow.day)
            
            print(f"📅 Scheduling reminder for: {run_time}")
            
            # Schedule the job with phone number
            scheduler.add_job(
                send_reminder, 
                'date', 
                run_date=run_time, 
                args=[task, from_number],
                id=f"reminder_{dt_iso}_{task[:10]}"  # Unique ID
            )
            
            time_until = run_time - now
            hours = int(time_until.total_seconds() / 3600)
            minutes = int((time_until.total_seconds() % 3600) / 60)
            
            resp = MessagingResponse()
            resp.message(f"✅ Reminder set for {run_time.strftime('%Y-%m-%d %I:%M %p')}\n"
                        f"⏰ In {hours}h {minutes}m\n"
                        f"📝 Task: {task}")
            
        except Exception as e:
            print(f"❌ Scheduling error: {e}")
            resp = MessagingResponse()
            resp.message(f"⚠️ Error scheduling reminder: {str(e)}")
    else:
        resp = MessagingResponse()
        resp.message("⚠️ Could not parse date/time")
    
    return str(resp)

if __name__ == "__main__":
    print("🚀 WhatsApp Reminder Agent starting...")
    print(f"📱 Twilio configured: {twilio_client is not None}")
    app.run(port=5000, debug=True)
