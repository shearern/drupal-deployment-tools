from textwrap import dedent

def secrets_tpl():
    return dedent("""\
        SSH_USER=username
        SSH_KEYFILE=/home/username/.ssh/id_rsa
        DB_PASS=db-password
        DB_USER=db-username
        """)
