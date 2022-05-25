import re
import smtplib
from email.mime.text import MIMEText


class InvalidEmail(Exception):
    pass


# Source: https://www.rfc-editor.org/errata_search.php?rfc=3696&eid=1690
email_regex = r'([^@\s]{1,64})@([a-zA-Z0-9\-]+)\.([a-zA-Z0-9\.]+)$'
max_local_part_len = 64
max_email_len = 254
max_domain_len = max_email_len - max_local_part_len - 1 # 189, discard '@'


def parse_email(email):
    if email:
        m = re.match(email_regex, email.lower())

        if m:
            local = m.group(1)
            domain = m.group(2)
            tld = m.group(3)

            if len(domain) + len(tld) + 1 <= max_domain_len:
                return (local, domain, tld)

    raise InvalidEmail


def send_email(subject, body, config):
    to_email = config['EMAIL']['target']
    from_email = config['EMAIL']['mailer']
    from_name = config['EMAIL']['mailer_name']
    mail_username = config['MAIL_USERNAME']
    mail_password = config['MAIL_PASSWORD']
    mail_server = config['MAIL_SERVER']
    mail_port = config['MAIL_PORT']

    email_msg = \
            f'From: <{from_email}>\n' \
            f'To: <{to_email}>\n' \
            f'Subject: {subject}\n\n' \
            f'{body}\n'

    email = MIMEText(body, 'html')
    email['Subject'] = subject
    email['From'] = f'"{from_name}" <{from_email}>'
    email['To'] = f'<{to_email}>'

    print(f'Sending email to {to_email} via ' \
          f'{mail_server}:{mail_port}:\n')

    sender = from_email
    receiver = to_email

    if config['DEBUG'] or config['TESTING']:
        print('DEBUG: Successfully sent email (not actually)!')
        return True

    try:
        server = smtplib.SMTP(mail_server, mail_port)
        server.starttls()
        server.login(mail_username, mail_password)
        server.sendmail(sender, [receiver], email.as_string())
        server.close()
        print('Successfully sent email!')
    except Exception as e:
        print('Error: failed to send email: {}'.format(e))
        return False

    return True
