import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


class EmailService:
    def __init__(self):
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')  # App password!
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')

    def send_email(self, subject: str, html_content: str, text_content: str = None):
        """
        Send HTML email

        Args:
            subject: Email subject
            html_content: HTML body
            text_content: Plain text fallback (optional)
        """
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['From'] = self.sender_email
            message['To'] = self.recipient_email
            message['Subject'] = subject

            # Add plain text version (fallback)
            if text_content:
                part1 = MIMEText(text_content, 'plain')
                message.attach(part1)

            # Add HTML version
            part2 = MIMEText(html_content, 'html')
            message.attach(part2)

            # Send via Gmail SMTP
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            print(f"Email sent to {self.recipient_email}")
            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            return False


# Example
if __name__ == "__main__":
    email_service = EmailService()

    html = """
    <html>
        <body>
            <h1 style="color: #0066cc;">Daily Digest</h1>
            <p>Here's your daily update!</p>

            <h2>Weather</h2>
            <p>Temperature: 25°C</p>

            <h2>News</h2>
            <ul>
                <li>Breaking story 1</li>
                <li>Breaking story 2</li>
            </ul>
        </body>
    </html>
    """

    email_service.send_email(
        subject="Your Daily Digest - Jan 16, 2025",
        html_content=html,
        text_content="Daily Digest - Check email in HTML view"
    )