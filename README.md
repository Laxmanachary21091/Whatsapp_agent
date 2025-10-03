# 🤖 WhatsApp Reminder Agent

An intelligent WhatsApp bot that uses AI to parse natural language messages and set reminders with voice notifications. Built with CrewAI, OpenAI GPT-4, Flask, and Twilio.

## ✨ Features

- 📱 **WhatsApp Integration** - Send reminders via WhatsApp messages
- 🧠 **AI-Powered Parsing** - Understands natural language using GPT-4 and CrewAI
- 🔊 **Voice Notifications** - Text-to-speech reminders on your local machine
- ⏰ **Smart Scheduling** - Automatically handles date/time parsing
- 💾 **Database Storage** - Stores reminders in SQLite
- 🎯 **Importance Detection** - Identifies urgent reminders automatically

## 📋 Prerequisites

- Python 3.12+
- Twilio Account (for WhatsApp)
- OpenAI API Key
- ngrok (for local development)

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/whatsapp-reminder-agent.git
cd whatsapp-reminder-agent
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

## 📦 Required Dependencies

Create a `requirements.txt` file with:
```
flask==3.0.0
twilio==8.10.0
python-dotenv==1.0.0
apscheduler==3.10.4
pyttsx3==2.90
crewai==0.28.0
langchain-openai==0.1.0
```

## 🔧 Configuration

### 1. Twilio WhatsApp Setup

1. Sign up at [Twilio](https://www.twilio.com)
2. Navigate to WhatsApp Sandbox
3. Send join message to activate your sandbox
4. Copy your Account SID, Auth Token, and WhatsApp number

### 2. OpenAI Setup

1. Get API key from [OpenAI Platform](https://platform.openai.com)
2. Add to `.env` file

### 3. ngrok Setup (for local testing)

```bash
ngrok http 5000
```

Copy the HTTPS URL and set it as your Twilio webhook URL:
`https://your-ngrok-url.ngrok.io/whatsapp`

## 💻 Usage

### Start the server

```bash
python app.py
```

### Send WhatsApp Messages

Send natural language messages to your Twilio WhatsApp number:

**Examples:**
- "Remind me to call mom tomorrow at 3pm"
- "Set reminder for meeting on 02/10/2025 at 2:30pm, it's important"
- "Remind me to submit assignment 04/10/2025 at 12:42pm"

### Response Format

The bot will reply with:
```
✅ Reminder set for 2025-10-04 12:42 PM
⏰ In 2h 30m
📝 Task: submit assignment
```

## 📁 Project Structure

```
whatsapp-reminder-agent/
├── app.py              # Main Flask application
├── agent.py            # CrewAI agent for parsing
├── db.py              # Database operations
├── .env               # Environment variables (not in repo)
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🛠️ How It Works

1. **User sends message** → Twilio webhook receives it
2. **AI parsing** → CrewAI + GPT-4 extracts task, datetime, importance
3. **Storage** → Reminder saved to SQLite database
4. **Scheduling** → APScheduler sets up the reminder
5. **Notification** → At scheduled time:
   - Voice notification plays locally
   - WhatsApp message sent back to user

## 🔐 Security Notes

- Never commit `.env` file to GitHub
- Add `.env` to your `.gitignore`
- Keep API keys secure
- Use environment variables for all sensitive data

## 📝 .gitignore

Create a `.gitignore` file:
```
# Environment
.env
venv/
__pycache__/

# Database
*.db
*.sqlite

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

## 🐛 Troubleshooting

### Voice not playing?
- Check volume settings
- Ensure pyttsx3 is installed correctly
- Try `pip install pypiwin32` on Windows

### WhatsApp not responding?
- Verify Twilio credentials
- Check ngrok is running
- Confirm webhook URL is correct

### Parsing errors?
- Ensure OpenAI API key is valid
- Check message format includes date/time
- Review logs for detailed errors

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Your Name - [@yourhandle](https://twitter.com/yourhandle)

## 🙏 Acknowledgments

- [Twilio](https://www.twilio.com) for WhatsApp API
- [OpenAI](https://openai.com) for GPT-4
- [CrewAI](https://www.crewai.com) for agent framework
- [Flask](https://flask.palletsprojects.com) for web framework

## 📧 Support

For issues and questions, please open an issue on GitHub or contact [laxmanacharrymulkala@gmail.com]

---

⭐ If you found this project helpful, please give it a star!
