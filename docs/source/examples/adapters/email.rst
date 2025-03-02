.. _examples_adapters_email:

Email Adapters
============

Sending emails with the email adapter.

Configuration
------------

First, configure your email settings:

.. code-block:: python

    from archipy.configs.base_config import BaseConfig

    class AppConfig(BaseConfig):
        EMAIL = {
            "SMTP_HOST": "smtp.gmail.com",
            "SMTP_PORT": 587,
            "SMTP_USERNAME": "your-email@gmail.com",
            "SMTP_PASSWORD": "your-app-password",
            "USE_TLS": True,
            "DEFAULT_SENDER": "Your App <your-email@gmail.com>"
        }

    # Set global configuration
    config = AppConfig()
    BaseConfig.set_global(config)

Basic Email Sending
----------------

Send a simple email:

.. code-block:: python

    from archipy.adapters.email.email_adapter import EmailAdapter

    # Create email adapter
    email_adapter = EmailAdapter()

    def send_welcome_email(user_email, user_name):
        # Send a simple text email
        email_adapter.send(
            to=user_email,
            subject="Welcome to Our App!",
            body=f"Hello {user_name},\n\nWelcome to our application!",
            body_type="plain"  # or "html" for HTML content
        )

    # Usage
    send_welcome_email("user@example.com", "John")

HTML Emails with Attachments
-------------------------

Send rich HTML emails with attachments:

.. code-block:: python

    from archipy.adapters.email.email_adapter import EmailAdapter

    email_adapter = EmailAdapter()

    def send_invoice_email(user_email, invoice_number, invoice_pdf_path):
        # HTML content
        html_content = f"""
        <html>
            <body>
                <h1>Invoice #{invoice_number}</h1>
                <p>Thank you for your purchase. Your invoice is attached.</p>
                <p>If you have any questions, please contact support.</p>
            </body>
        </html>
        """

        # Attachments
        attachments = [
            {
                "file_path": invoice_pdf_path,
                "filename": f"Invoice-{invoice_number}.pdf",
                "mime_type": "application/pdf"
            }
        ]

        # Send email with attachment
        email_adapter.send(
            to=user_email,
            subject=f"Your Invoice #{invoice_number}",
            body=html_content,
            body_type="html",
            attachments=attachments
        )

    # Usage
    send_invoice_email(
        "customer@example.com",
        "INV-12345",
        "/path/to/invoices/INV-12345.pdf"
    )

Multiple Recipients and CC/BCC
----------------------------

Send to multiple recipients with CC and BCC:

.. code-block:: python

    from archipy.adapters.email.email_adapter import EmailAdapter
    from pydantic import EmailStr

    email_adapter = EmailAdapter()

    def send_team_notification(subject, message, team_emails, cc_manager=True):
        # Convert recipient list to expected format
        recipients = [EmailStr(email) for email in team_emails]

        # Add CC recipients if needed
        cc = []
        if cc_manager:
            cc = [EmailStr("manager@example.com")]

        email_adapter.send(
            to=recipients,
            subject=subject,
            body=message,
            body_type="plain",
            cc=cc,
            bcc=[EmailStr("records@example.com")]  # BCC for record keeping
        )

    # Usage
    send_team_notification(
        "Project Update",
        "The project milestone has been completed.",
        ["team1@example.com", "team2@example.com"]
    )

Template-Based Emails
------------------

Send emails using templates:

.. code-block:: python

    from archipy.adapters.email.email_adapter import EmailAdapter
    import os

    email_adapter = EmailAdapter()

    def send_password_reset(user_email, reset_token, user_name):
        # Read template from file
        template_path = os.path.join("templates", "emails", "password_reset.html")
        with open(template_path, "r") as file:
            template = file.read()

        # Replace placeholders in template
        html_content = template.replace("{{user_name}}", user_name)
        html_content = html_content.replace("{{reset_token}}", reset_token)
        html_content = html_content.replace(
            "{{reset_link}}",
            f"https://example.com/reset-password?token={reset_token}"
        )

        # Send email using template
        email_adapter.send(
            to=user_email,
            subject="Password Reset Request",
            body=html_content,
            body_type="html"
        )

    # Usage
    send_password_reset(
        "user@example.com",
        "abc123xyz789",
        "John Doe"
    )
