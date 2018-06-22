from routeros_api import api, api_socket, base_api, api_communicator
from routeros_api import api_communicator
from routeros_api import communication_exception_parsers
from routeros_api import api_socket
from routeros_api import api_structure
from routeros_api import base_api
from routeros_api import exceptions
from routeros_api import resource
import binascii

def new_connect(host, username='admin', password='xd', port=8729):
    return CustomRouterOsApiPool(host, username, password, port).get_api()


class CustomRouterOsApiPool(api.RouterOsApiPool):
    def get_api(self):
        if not self.connected:
            self.socket = api_socket.get_socket(self.host, self.port,
                                                timeout=self.socket_timeout)
            base = base_api.Connection(self.socket)
            communicator = api_communicator.ApiCommunicator(base)
            self.api = CustomRouterApi(communicator,version="1.43")
            for handler in self._get_exception_handlers():
                communicator.add_exception_handler(handler)
            self.api.login(self.username, self.password)
            self.connected = True
        return self.api



class CustomRouterApi(api.RouterOsApi):
    def __init__(self, communicator, version="1.43"):
        self.communicator = communicator
        self.version = version

    def _new_login(self, login, password):
        response = self.get_binary_resource('/').call('login')
        token = binascii.unhexlify(response.done_message['ret'])        
        hasher=b'\x00'        
        hasher+=password.encode()
        hasher+=token
        hashed = b'00' + hasher     
        self.get_binary_resource('/').call(            
        'login', {'name': login.encode(), 'password': hashed})

    def login(self, login, password):
        if self.version=="1.43":
        	self._new_login(login,password)
        else:
            super(CustomRouterApi, self).login(login,password)

def main():
    host = "rb2011.wisphub.net"
    api = new_connect(host)

if __name__ == "__main__":
    main()
