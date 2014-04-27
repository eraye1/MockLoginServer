import socketserver
import hashlib
import json

class MockLoginServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()

        hashHex = hashlib.sha224(self.data).hexdigest()

        responseString = json.dumps({'success': 'true', 'sessionToken': hashHex}, sort_keys=True, indent=4, separators=(',', ': '))

        print(responseString);

        bytesHash = bytes(responseString, 'utf-8')


        self.request.sendall(bytesHash)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    server = socketserver.TCPServer((HOST, PORT), MockLoginServer)
    server.serve_forever()