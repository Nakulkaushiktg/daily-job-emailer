# daily_job_emailer.py
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from whatsapp_sender import send_whatsapp
import os

# Dummy fallback job list for testing
def scrape_yc_jobs():
    return [
        {
            "title": "Backend Developer",
            "company": "StartupX",
            "location": "Remote",
            "link": "https://startupx.com/job/backend-dev",
            "summary": "Work on scalable backend systems using Node.js."
        },
        {
            "title": "Junior Backend Engineer",
            "company": "TechNest",
            "location": "Remote",
            "link": "https://technest.com/careers/junior-backend",
            "summary": "Join a fast-growing team building API infrastructure."
        }
    ]

def scrape_angellist_jobs():
    return [
        {
            "title": "Entry-Level Backend Developer",
            "company": "CodeCraft",
            "location": "India (Remote)",
            "link": "https://wellfound.com/job/codecraft-backend",
            "summary": "Exciting backend opportunity in a product-focused startup."
        },
        {
            "title": "Software Engineer Intern",
            "company": "LaunchLabs",
            "location": "Remote",
            "link": "https://wellfound.com/job/launchlabs-se-intern",
            "summary": "Internship with a focus on backend services and cloud."
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
    subject = f"\U0001F50E Daily Entry‑Level Software Dev Roles — {today}"
    body = f"<h2>{subject}</h2><br>"
    for job in jobs:
        msg = generate_linkedin_message(job['company'], job['title'])
        body += (
            f"<h3>{job['title']} – {job['company']}</h3>"
            f"<b>Location:</b> {job['location']}<br>"
            f"<b>Apply here:</b> <a href='{job['link']}'>{job['link']}</a><br>"
            f"<b>Summary:</b> {job['summary']}<br><br>"
            f"<b>\U0001F4AC LinkedIn Message:</b><br><pre>{msg}</pre><hr><br>"
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
        print(f"❌ Email failed: {e}")

if __name__ == "__main__":
    jobs = scrape_yc_jobs() + scrape_angellist_jobs()
    subject, html_body = create_email_content(jobs)
    send_email(subject, html_body)

    # WhatsApp plain message
    text_jobs = "\n\n".join([f"{j['title']} at {j['company']}\n{j['link']}" for j in jobs[:5]])
    send_whatsapp(f"\U0001F4BC Top Entry-Level Jobs Today:\n\n{text_jobs}")
