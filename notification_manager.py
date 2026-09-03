import smtplib

MY_EMAIL = "sp25-bcs-122@cuilahore.edu.pk"
MY_PASSWORD = "tpaq oeof tmwb kpio"


class NotificationManager:

    def send_email(self, message):
        try:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=MY_EMAIL,
                    msg=f"Subject: Low Flight Price Alert!\n\n{message}".encode('utf-8')
                )
            print("✉️ Notification email sent successfully!")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")