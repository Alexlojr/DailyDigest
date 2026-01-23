import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class EmailService:
    def __init__(self):
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_PASSWORD')  # App password!
        self.recipient_email = os.getenv('RECIPIENT_EMAIL')

    def send_email(self, subject: str, html_content: str, text_content: str = None, image_paths: dict = None):
        """
        Send HTML email with optional embedded images

        Args:
            subject: Email subject
            html_content: HTML body (can reference images using cid:image_name)
            text_content: Plain text fallback (optional)
            image_paths: Dict of {image_name: file_path} for embedded images
                        Example: {'weather': 'src/imgs/morning_weather.png'}
        """
        try:
            # Create message container
            message = MIMEMultipart('related')
            message['From'] = self.sender_email
            message['To'] = self.recipient_email
            message['Subject'] = subject

            # Create alternative container for text/html
            msg_alternative = MIMEMultipart('alternative')
            message.attach(msg_alternative)

            # Add plain text version (fallback)
            if text_content:
                part_text = MIMEText(text_content, 'plain')
                msg_alternative.attach(part_text)
            else:
                # Default fallback text
                part_text = MIMEText('Please view this email in HTML mode.', 'plain')
                msg_alternative.attach(part_text)

            # Add HTML version
            part_html = MIMEText(html_content, 'html')
            msg_alternative.attach(part_html)

            # Attach images if provided
            if image_paths:
                for image_name, image_path in image_paths.items():
                    if Path(image_path).exists():
                        with open(image_path, 'rb') as img_file:
                            img_data = img_file.read()
                            image = MIMEImage(img_data)
                            image.add_header('Content-ID', f'<{image_name}>')
                            image.add_header('Content-Disposition', 'inline', filename=Path(image_path).name)
                            message.attach(image)
                            print(f"Attached image: {image_name} ({Path(image_path).name})")
                    else:
                        print(f"Image not found: {image_path}")

            # Send via Gmail SMTP
            # Note: Using port 465 (SSL). If execution fails, try port 587 with starttls.
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            print(f"Email sent to {self.recipient_email}")
            return True

        except Exception as e:
            print(f"Failed to send email: {e}")
            import traceback
            traceback.print_exc()
            return False


# Test example
if __name__ == "__main__":
    email_service = EmailService()

    # Example HTML with embedded image
    html = """
    <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h1 style="color: #0066cc;">Daily Digest</h1>
            <p>Here's your daily update!</p>

            <h2>Weather Radar</h2>
            <img src="cid:weather" alt="Weather Map" style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">

            <h2>News</h2>
            <ul>
                <li>Breaking story 1</li>
                <li>Breaking story 2</li>
            </ul>
        </body>
    </html>
    """

    # Specify images to embed
    images = {
        'weather': 'src/imgs/morning_weather.png'  # Reference in HTML as cid:weather
    }

    email_service.send_email(
        subject="Test Email with Image",
        html_content=html,
        text_content="Daily Digest - Check email in HTML view",
        image_paths=images
    )
