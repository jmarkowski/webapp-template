import re


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
