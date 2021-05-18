# Password hacker simulator (JetBrains Academy's project)

### This scripts gets a list of logins and generate random passwords trying to get a correct one. It exploit known vulnerability: the remote host responds after delay if symbols we try for password match the beggining of the correct one.

## Used modules:

    datetime
    string
    urllib
    argparse
    json
    socket

### It should be started from terminal by: python password_hacker.py remote_host remote_port
