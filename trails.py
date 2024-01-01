from email.message import EmailMessage
import smtplib, ssl
import logging
import connectionpool as cp

class mailtoFunctions:
    def __init__(self,pool):
        self.pool:cp.ConnectionPool = pool
    def fetchEmail(self,person):
        try:
            self.connection = self.pool.get_connection()
            if not isinstance(self.connection, str):
                with self.connection.cursor() as cursor:
                    cursor.execute("SELECT Email FROM Faculty WHERE Name = %s",(person,))
                    self.result = cursor.fetchone()
                    self.pool.return_connection(self.connection)
                    if self.result is not None:
                        return self.result[0],1
            else:
                return 'Check Internet Connection',0
        except Exception as e:
            return str(e),0
    def sendmail(self, visitor_name, visitor_phone, visitorEmail, person_to_meet, reason_of_visit):
        email_sender = '21311A0569@sreenidhi.edu.in'
        email_password = 'hbmmykgtaadqnjpp'
        email_recipient, flag = self.fetchEmail(person_to_meet)

        if flag == 1:
            subject = 'Visitor Management System'
            body = f"Mr./Ms. {visitor_name} is here to meet you.\n" \
                   f"He/She is at the gate and is expecting to meet you soon.\n" \
                   f"Contact: {visitor_phone}\nEmail: {visitorEmail}\nReason: {reason_of_visit}"

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_recipient  # Use the actual recipient here
            em['Subject'] = subject
            em.set_content(body)
            context = ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_recipient, em.as_string())
            except Exception as e:
                logging.error(f"Error sending email: {str(e)}")
        else:
            logging.error(f"Unable to fetch recipient email for {person_to_meet}")
