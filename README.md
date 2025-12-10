# **LLM Daily Email Sender**

A small Python project that sends **daily educational lessons about Large Language Models (LLMs)** to a list of recipients.
Email delivery is powered by **SendGrid**, and recipients are managed through environment variables.

---

## **Features**

- Sends HTML-formatted LLM lessons via email
- Supports multiple recipients
- Uses environment variables for configuration
- Lightweight and easy to automate with cron or scheduled tasks

---

## **How It Works**

The script:

1. Reads the sender address and recipient list from environment variables
2. Constructs the email using SendGrid's `Mail` helper
3. Sends the email through the SendGrid API
4. Prints status codes for debugging

---

## **Project Structure**

```
project/
│
├── app.py
├── README.md
└── .env        # environment variables (not committed)
```

---

## **Environment Variables**

Create a `.env` file (or export manually) with:

```
SENDGRID_API_KEY=your_api_key
from_email=your_sender_email@example.com
to_email=example1@gmail.com,example2@gmail.com
```

**Note:**
`to_email` must be a comma-separated list—not a Python array. for example -> abc@gmail.com,dcf@gmail.com

---

## **Installation**

```bash
pip install sendgrid python-dotenv
```

---

## **Running the Script**

```bash
python app.py
```
