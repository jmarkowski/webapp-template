import re


class InvalidEmail(Exception):
    pass


email_regex = r'([^@\s]{1,64})@([a-zA-Z0-9\-]+)\.([a-zA-Z0-9\.]+)$'


def parse_email(email):
    if email:
        m = re.match(email_regex, email.lower())

        if m:
            local = m.group(1)
            domain = m.group(2)
            tld = m.group(3)

            if len(domain) + len(tld) < 255:
                return (local, domain, tld)

    raise InvalidEmail
