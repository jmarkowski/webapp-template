# Do NOT add this file to version control

# A secret key is used for securely signing the session in a cookie and can be
# used for other security related needs. It should be a long random string of
# bytes.
# For example, the output of the following command:
# $ python -c 'import os; print(os.urandom(16))'
#
# It should go without saying: NEVER REVEAL THE SECRET KEY.
SECRET_KEY = 'my-super-secret-key'

DB_URI = 'postgresql://postgres:mypassword@sql_database:5432/webapp_db'
