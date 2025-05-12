# 🤖 AI Study Assistant Bot

An advanced Telegram bot built with [Aiogram](https://docs.aiogram.dev) to help users learn and explore academic topics through natural language queries. This bot leverages AI-powered explanations, examples, formulas, and external resources to support interactive learning.

---

## 📁 Project Structure
```
├── app/
│ ├── db.py # Database operations (SQLite3)
│ ├── handlers.py # Message and command handlers
│ └── language.py # Multi-language support and translation
│
├── database/
│ └── users.db # SQLite database for storing user data
│
├── .env # Environment variables (Bot token, config)
├── config.py # Configuration management
├── requirements.txt # Python dependencies
├── run.py # Bot entry point (main runner)
├── tutor.py # Core AI tutor logic (explains topics)
```


---

## 🚀 Features

- 📚 **AI-Powered Topic Explanation**  
  Ask any question and receive a detailed explanation, complete with key formulas, examples, and learning resources.


- 🌐 **Multilingual Support**  
  The bot supports multiple languages (currently English and Russian) with smart fallback and automatic translation.


- 🧠 **Context-Aware Learning**  
  Each user has a profile that adapts over time based on their queries and topics.


- 📝 **User Management**  
  Users can register, edit their information, and track learning progress.


- ⚙️ **SQLite Database Integration**  
  Lightweight and fast storage for managing users.


- 🛡️ **Secure Config with .env**  
  Environment variables managed securely using `python-dotenv`.


---

## 🧠 Commands

| Command        | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `/start`       | Starts or restarts the registration process                                 |
| `/help`        | Displays bot usage instructions and feature list                            |
| `/edituser`    | Lets the user change their name and preferred language                      |
| *(any text)*   | Sends a topic to the bot and receives an AI-generated explanation           |

---

## 🧪 Example Conversation


👤 /start
🤖 Hello! Please choose your language.

👤 English 🇺🇸
🤖 Great! What is your name?

👤 Alice
🤖 Welcome Alice! You can now ask about any topic.

👤 What is Newton's second law?
🤖
📌 Newton's Second Law

📖 Explanation:
Newton's second law states that the force acting on an object is equal to the mass of that object times its acceleration...

📐 Key Formulas:

F = ma

🧪 Examples:

A 2 kg object accelerating at 3 m/s² experiences a force of 6 N.

📚 Resources:

https://en.wikipedia.org/wiki/Newton%27s_laws_of_motion


---

## ⚙️ Setup Instructions

1. **Clone the repo**:
   ```bash
   git clone https://github.com/ayubxontursunov/ai-study-assistant-bot.git
   cd ai-study-assistant-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Telegram bot token**  
   Create a `config.py` file:
   ```python
   TOKEN = "your_telegram_bot_token_here"
   ```

4. **Add your OpenAI API key**  
   Create a `.env` file:
   ```ini
   OPENAI_API_KEY=your_openai_api_key_here
   MODEL_CHOICE=gpt-4  # or gpt-3.5-turbo, etc.
   ```

5. **Run the bot**:
   ```bash
   python run.py
   ```


---

## 🧩 Dependencies

- `aiogram`
- `python-dotenv`
- `sqlite3` (Python built-in)
- `openai-agent or any LLM provider (configured in `tutor.py`)

---


Made with ❤️ using [Aiogram](https://docs.aiogram.dev/) & [OpenAI Agents](https://openai.github.io/openai-agents-python/)
