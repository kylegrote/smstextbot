import smtplib
import os



def sendEmail(to, subject, body):
    myEmail = "kennyakakyle@gmail.com"
    appKey = os.getenv('kennyakakyleEmailKey')
    connection = smtplib.SMTP("smtp.gmail.com", 587)
    connection.starttls()
    try:
        connection.login(user=myEmail, password=appKey)
    except Exception as e:
        print(e)
        return


    # <--------------------------------test connection---------------------------------------->

    # <--------------------------------send email(s)---------------------------------------->

    signature = "Otto Matic \nRobotic Office Assistant to Kyle Grote \nFor more Information about Otto: https://www.youtube.com/watch?v=uc6f_2nPSX8 "
    msg = {
        "subject": subject,
        "body": f"{body}\n\n{signature}",
        "to": to,
        "from": myEmail,
    }

    connection.sendmail(from_addr=msg["from"], to_addrs=msg["to"], msg=f"subject:{msg["subject"]}\n\n{msg["body"]}")
    connection.close()




