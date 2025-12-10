from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import json
import re
load_dotenv()

from google import genai

client = genai.Client()

day = 2

prompt = """
You are my personal AI tutor specializing in Large Language Models (LLMs).

Your task:
Generate a short, structured LLM lesson for Day %d.

You MUST return the output as valid JSON ONLY.

CRITICAL RULES (do NOT break these):
- Output MUST be a single JSON object.
- NO text before or after the JSON.
- NO Markdown code fences (no ```).
- NO comments.
- NO extra keys.
- The "body" field MUST contain valid HTML (Gmail-compatible).
- All hyperlinks MUST use <a href="...">...</a>.
- Do NOT escape HTML tags.
- Do NOT return Markdown.

Your JSON MUST match this structure exactly:

{
  "subject": "<email subject line>",
  "body": "<valid HTML email body>"
}

Content rules for the HTML inside "body":
- Include:
  - Topic Title
  - Concept Explanation
  - Real-World Example or Analogy
  - Optional Deep Dive (short)
  - Mini Quiz (2–3 questions)
  - Further Learning (with HTML hyperlinks)
- Keep total content under 400 words.
- Use simple, beginner-friendly language.
- Lesson must build on previous days.

REMEMBER:
Return ONLY the JSON object.
If you include anything else, the system will break.
""" % day

response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
)

try:
    data = json.loads(response.text)
except Exception as e:
    print("Error parsing model response as JSON:", str(e))
    print("--- raw model response ---")
    print(response.text)
    raise
subject = data.get("subject", f"Lesson {day}")
body = data.get("body", "No body content returned.")

# --- 2. Send via SendGrid ---

raw_emails = os.getenv("to_email") #receivers emails
email_list = [email.strip() for email in raw_emails.split(",")]
for email in email_list:
    message = Mail(
        from_email=os.getenv("from_email"),
        to_emails=email,
        subject=subject,
        html_content=body 
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print("email sent successfully")
    except Exception as e:
        print(str(e))