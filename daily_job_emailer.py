# daily_job_emailer.py
import smtplib
import datetime
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from whatsapp_sender import send_whatsapp
import os

def scrape_yc_jobs():
    url = "https://www.workatastartup.com/jobs?role=software-engineer&level=entry"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("li", class_="job-preview")

    jobs = []
    for job in job_cards[:5]:
        title_tag = job.find("h4")
        company_tag = job.find("h3")
        link_tag = job.find("a", href=True)
        summary_tag = job.find("p")

        if title_tag and company_tag and link_tag:
            jobs.append({
                "title": title_tag.get_text(strip=True),
                "company": company_tag.get_text(strip=True),
                "location": "Remote or US (source: YC)",
                "link": "https://www.workatastartup.com" + link_tag["href"],
                "summary": summary_tag.get_text(strip=True) if summary_tag else "No summary."
            })
    return jobs

def scrape_angellist_jobs():
    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://wellfound.com/jobs#remote=true&entry_level=true"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []
    for job in soup.select(".styles_component__job___3Zbkm")[:5]:
        title_tag = job.select_one(".styles_title__job___wFZzo")
        company_tag = job.select_one(".styles_component__companyName___1KPZp")
        link_tag = job.find("a", href=True)
        location_tag = job.select_one(".styles_component__location___2OYLa")

        if title_tag and company_tag and link_tag:
            jobs.append({
                "title": title_tag.text.strip(),
                "company": company_tag.text.strip(),
                "location": location_tag.text.strip() if location_tag else "Remote",
                "link": "https://wellfound.com" + link_tag["href"],
                "summary": "From AngelList – entry level opportunity"
            })
    return jobs

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
    jobs = [j for j in jobs if 'remote' in j['location'].lower() or 'india' in j['location'].lower()]
    subject, html_body = create_email_content(jobs)
    send_email(subject, html_body)

    # WhatsApp plain message
    text_jobs = "\n\n".join([f"{j['title']} at {j['company']}\n{j['link']}" for j in jobs[:5]])
    send_whatsapp(f"\U0001F4BC Top Entry-Level Jobs Today:\n\n{text_jobs}")
