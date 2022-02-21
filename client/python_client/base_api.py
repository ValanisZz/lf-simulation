from modbus.post_threading import Post

from contextlib import closing
from psycopg2 import connect
from time import sleep
from os import path

# ------------------------------------------------------------------------------------
shares, in_ports, out_ports = [], [], [0] * 106


######################################################################################

##########################################
#         Socket and FT methods          #
##########################################

class BaseApi:

    def __init__(self, sock):
        self.post = Post(self)
        self.sock = sock
        
        self.post.__send_data()
        self.post.__receive_data()
        self.post.__update_shares():

    ######################################
    #          Main FT methods           #
    ######################################

    @staticmethod
    def get(port: int):
        """Get input port value
    :param port: input port number
    :type port: int in range (0, 112)
        """
        return in_ports[port]

    def set(self, port, sensor=None, time=None, value=1):
        """Set output port value in a special way
    :param port: output port number
    :type port: int in range (0, 106)
    :param sensor: sensor port number, defaults to None
                   resetting port value after sensor value changed
    :type sensor: int in range (0, 112)
    :param time: seconds to reset port value, defaults to None
    :type time: float
    :param value: value to set, defaults to 1
    :type value: int in range (0, 2)
        """
        global out_ports
        out_ports[port] = value

        if value == 0:
            return
        elif sensor:
            value = self.get(sensor)
            while self.get(sensor) == value:
                self.wait(0.001)
            if time:
                self.wait(time)
        elif time:
            self.wait(time)
        else:
            return

        out_ports[port] = 0
        
    @staticmethod
    def wait(secs: float):
        """Wait for a special time
    :param secs: time for waiting
    :type secs: float
        """
        sleep(secs)

    ##################################################################################

    @staticmethod
    def execute(query: str, result=False):
        """Execute SQL-query
    :param query: query to execute
    :type query: str
    :param result: result return marker, defaults to False
    :type query: bool
    :return: SQL-query result
    :rtype: list of tuples
        """
        with closing(connect(user='postgres', password='...', host='localhost', database='postgres')) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()
                if result:
                    return cursor.fetchall()
    
    @staticmethod
    def check_shares():
        """Print wallet shares"""
        print(f'- Wallet shares: {shares}')

    def get_color(self):
        """Get current color from analog sensor"""
        print(f'- Current color: {self.get(0)}')

    ##################################################################################

    ######################################
    #          Data FT methods           #
    ######################################
    
    def __send_data():
        old_data = []
        while self.sock.fileno() != -1:
            if out_ports != old_data:
                old_data = out_ports.copy()
                self.sock.send(bytes(out_ports))
            self.wait(0.001)
    
    def __receive_data():
        try:
            global in_ports
            while True:
                new_data = list(self.sock.recv(2048))
                del in_ports[:]
                
                in_ports.extend(new_data)
        except:
            self.sock.close()
    
    def __update_shares():
        mtime = None
        global shares
        while self.sock.fileno() != -1:
            if mtime != path.getmtime('wallet_accounts.txt'):
                with closing(open('wallet_accounts.txt', 'r')) as file:
                    del shares[:]
                    newshares = list(map(int, file.readlines()))
                    shares.extend([ns / sum(newshares) for ns in newshares])
                    
                    mtime = os.path.getmtime('wallet_accounts.txt')
            self.wait(0.001)
    
# ------------------------------------------------------------------------------------
