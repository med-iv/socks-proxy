import socket
import struct
import select
from socketserver import ThreadingMixIn, TCPServer, StreamRequestHandler

PORT = 1080


class SocksProxy(StreamRequestHandler):
    def get_user_id(self) -> str:
        resulted_id = []
        c = self.connection.recv(1)
        while ord(c):
            resulted_id.append(c.decode("utf-8"))

        return ''.join(resulted_id)

    @staticmethod
    def begin_exchange(client, remote):
        while True:
            r, w, e = select.select([client, remote], [], [])
            print("loop step")
            print(r)
            if client in r:
                data = client.recv(4096)
                if remote.send(data) <= 0:
                    break

            if remote in r:
                data = remote.recv(4096)
                if client.send(data) <= 0:
                    break

    def handle(self) -> None:
        print('Accepting connection from %s:%s' % self.client_address)

        try:
            # initiate connection
            version = struct.unpack("!B", self.connection.recv(1))[0]
            cmd = struct.unpack("!B", self.connection.recv(1))[0]
            remote_port = struct.unpack('!H', self.connection.recv(2))[0]
            remote_address = socket.inet_ntoa(self.connection.recv(4))
            print(remote_address, remote_port, cmd)
            user_id = self.get_user_id()
            print(user_id)

            # send acknowledge
            self.connection.sendall(b'\x00')
            self.connection.sendall(b'\x5a')
            for i in range(6):
                self.connection.sendall(b'\x00')

            if cmd == 1:
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.connect((remote_address, remote_port))
                print('Connected to %s %s' % (remote_address, remote_port))
                self.begin_exchange(client=self.connection, remote=remote)

            self.server.close_request(self.request)
        except Exception as err:
            print(err)


class AsyncTCPServer(ThreadingMixIn, TCPServer):
    pass


if __name__ == '__main__':
    with AsyncTCPServer(('', PORT), SocksProxy) as server:
        server.serve_forever()
