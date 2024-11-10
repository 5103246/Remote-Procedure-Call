import socket
import os
import math
import json

class rpcFunction():
    @staticmethod
    def floor(x):
        return math.floor(x)
    
    @staticmethod
    def nroot(n, x):
        return x ** (1/n)
    
    @staticmethod
    def reverse(s):
        return s[::-1]
    
    @staticmethod
    def validAnagram(str1, str2):
        anagram = str2.lower()
        return str1.lower() == anagram[::-1]
    
    @staticmethod
    def sort(strArr):
        return sorted(strArr)
    
    functionMap = {
        'floor': floor.__func__,
        'nroot': nroot.__func__,
        'reverse': reverse.__func__,
        'validAnagram': validAnagram.__func__,
        'sort': sort.__func__
    }
    
class connection():
    @staticmethod
    def connect():
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_address = '/tmp/socket_file'
        try:
            os.unlink(server_address)
        except FileNotFoundError:
            pass
        
        print('Starting up on {}'.format(server_address))
        sock.bind(server_address)
        sock.listen(1)
        
        while True:
            connection, client_address = sock.accept()
            try:
                print('connection from {}'.format(client_address))
                
                while True:
                    data = connection.recv(4096)
                    
                    if data:
                        request = json.loads(data.decode('utf-8'))
                        
                        try:
                            result = jsonfile.getRequest(request)
                            response = jsonfile.createResponse(result, request['id'])
                            connection.sendall(response.encode())
                        except Exception as err:
                            response = jsonfile.createErrorResponse(err, request['id'])
                            connection.sendall(response.encode())
                        
                    else:
                        break
                    
            finally:
                print('closing socket')
                connection.close()

class jsonfile():
    @staticmethod
    def getRequest(request):
        try:
            result = rpcFunction.functionMap[request['method']](*request['params'])
            return result
        except Exception as err:
            raise err
    
    @staticmethod
    def createResponse(result, id):
        response = {
            'results': result,
            'result_type': type(result).__name__,
            'id': id
        }
        return json.dumps(response)
    
    @staticmethod
    def createErrorResponse(error, id):
        response = {
            'message': str(error),
            'id': id
        }
        return json.dumps(response)

def main():
    connection.connect()

if __name__ == '__main__':
    main()