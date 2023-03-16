import constants
import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (constants.SERVER, constants.PORT)
        self.p = self.connect()

    def get_p(self):
        """
        :return: p, the player id on the server
        """
        return self.p

    def connect(self):
        """
        Makes sure the client is connected to the server
        :return: ID of player
        """
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except Exception as e:
            print("Error connecting to server: ", e)

    def send(self, data):
        """
        Sends a command to the server and waits for a response
        :param data: String data being sent to the server
        :return: Object data returned by the server
        """
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
