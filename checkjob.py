import requests
from requests.auth import HTTPBasicAuth
import jinja2

# Replace with your AWX details
AWX_HOST = "https://your-awx-server.com"
AWX_USERNAME = "your_username"
AWX_PASSWORD = "your_password"

# Email configuration
FROM_EMAIL = "noreply@awx.com"
TO_EMAIL = "recipient@example.com"
JOB_ID = 12345  # Replace with your specific job ID

# Optional: Path to custom Jinja2 template
TEMPLATE_FILE = "email_template.html"


def get_job_details(job_id):
    url = f"{AWX_HOST}/api/v2/jobs/{job_id}"
    auth = HTTPBasicAuth(AWX_USERNAME, AWX_PASSWORD)
    response = requests.get(url, auth=auth)
    response.raise_for_status()

    return response.json()


def format_email_content(job_data, template_file=None):
    if template_file:
        with open(template_file, "r") as f:
            template = jinja2.Template(f.read())
            return template.render(job_data)
    else:
        # Basic email content formatting
        content = f"Job Name: {job_data['name']}\n" \
                  f"Job ID: {job_data['id']}\n" \
                  f"Failed Hosts:\n"
        for host, tasks in job_data['failures'].items():
            content += f"- {host}:\n"
            for task, reason in tasks.items():
                content += f"    - Task: {task}\n" \
                           f"      Reason: {reason}\n"
        return content


def send_email(content):
    # Use your preferred email sending library (e.g., smtplib)
    # Configure SMTP server details and send the email with content
    pass  # Replace with your email sending logic


def main():
    job_data = get_job_details(JOB_ID)
    email_content = format_email_content(job_data, TEMPLATE_FILE)
    send_email(email_content)


if __name__ == "__main__":
    main()
