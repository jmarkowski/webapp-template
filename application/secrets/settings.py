# Do NOT add this file to version control
from os import getenv


# A secret key is used for securely signing the session in a cookie and can be
# used for other security related needs. It should be a long random string of
# bytes.
# For example, the output of the following command:
# $ python -c 'import os; print(os.urandom(16))'
#
# It should go without saying: NEVER REVEAL THE SECRET KEY.
SECRET_KEY = 'my-super-secret-key'

DB_URI = 'postgresql://{user}:{password}@{server}:5432/{database}' \
         .format(user=getenv('POSTGRES_USER'),
                 password=getenv('POSTGRES_PASSWORD'),
                 database=getenv('POSTGRES_DB'),
                 server=getenv('SQL_DATABASE_SERVER_NAME'))
