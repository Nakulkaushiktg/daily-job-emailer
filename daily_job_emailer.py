
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sample job data – replace this with real scraping/API logic
jobs = [
    {
        "title": "Software Engineer Intern",
        "company": "Zeta",
        "location": "Remote",
        "link": "https://careers.zeta.tech/software-engineer-intern",
        "summary": "Work on core backend systems with senior engineers. Learn Go and distributed architecture."
    },
    {
        "title": "Junior Backend Developer",
        "company": "Groww",
        "location": "Bangalore, India",
        "link": "https://groww.in/careers/backend-developer",
        "summary": "Entry-level backend role for fast-scaling fintech startup. Work with Node.js and MongoDB."
    }
]

def generate_linkedin_message(company, role):
    return (
        f"Hi [Hiring Manager Name],\n"
        f"I came across the {role} role at {company} and was impressed with your work. "
        "As a recent intern with MERN backend experience, I’d love to bring my skills to your team. "
        "Would love to connect and learn more!"
    )

def create_email_content(jobs):
    today = datetime.date.today().strftime('%B %d')
    subject = f"🔎 Daily Entry‑Level Software Dev Roles — {today}"
    body = f"<h2>{subject}</h2><br>"
    for job in jobs:
        msg = generate_linkedin_message(job['company'], job['title'])
        body += (
            f"<h3>{job['title']} – {job['company']}</h3>"
            f"<b>Location:</b> {job['location']}<br>"
            f"<b>Apply here:</b> <a href='{job['link']}'>{job['link']}</a><br>"
            f"<b>Summary:</b> {job['summary']}<br><br>"
            f"<b>💬 LinkedIn Message:</b><br><pre>{msg}</pre><hr><br>"
        )
    return subject, body

def send_email(subject, html_body):
    sender_email = "nakulkaushik777@gmail.com"
    receiver_email = "nakulkaushik777@gmail.com"
    app_password = os.getenv("GMAIL_APP_PASSWORD")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("✅ Email sent.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

if __name__ == "__main__":
    import os
    subject, body = create_email_content(jobs)
    send_email(subject, body)
