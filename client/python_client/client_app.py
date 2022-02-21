#!/usr/bin/env python
import gnureadline
import socket

from algorithms import MainApi
from base_api import in_ports

##################################################################################

if __name__ == "__main__":

    ######################################
    #           Initialisation           #
    ######################################

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    M = MainApi()

    try:
        sock.connect(('localhost', 10000))
        print("- Client session succesfully started")

    except Exception as e:
        print("- Error, server is not available")
        print(f"REASON: {e}")
        exit(1)
        
    M = MainApi(sock)
    
    print("(Do something to fill data structure)")
    while not in_ports:
        M.wait(0.001)
    
    # ----------------------------------------------------------------------------
    
    ######################################
    #            Application             #
    ######################################

    print("1. Main commands: run, stop, exit\n"+
          "2. Checking commands: color, shares\n"+
          "3. Database commands: add (.), show (.), fill, clear, add (.)\n"+
          "4. Service commands: act0 (.), act1 (.), act2 (.), act3 (.), set (.)")
    print("- Command pattern: \'COMMAND\' or \'COMMAND ARGUMENTS\'")

    command = None
    methods = {'color': 'M.get_color',
               'shares': 'M.check_shares',
               
               'run': 'M.run_factory',
               'stop': 'M.stop_factory',
               
               'add': 'M.add_blocks',
               'show': 'M.show_warehouse',
               'fill': 'M.fill_warehouse',
               'clear': 'M.clear_warehouse',
               
               'act1': 'M.act1', 'act1': 'M.act1', 'act1': 'M.act1', 'act1': 'M.act1', 'set': 'M.set'}

    while command != "exit" or sock.fileno() == -1:
        command = input("Command: ").split(maxsplit=1)
        command, args = (command[0], '') if len(command) == 1 else command

        try:
            if command == 'exit':
                sock.close()
            elif sock.fileno() == -1:
                print('- Error, server is not available')
            elif command in ('run', 'stop',
                             'color', 'shares',
                             'show', 'fill', 'clear', 'add',
                             'act0', 'act1', 'act2', 'act3', 'set'):
                exec(f'{methods[command]}({args})')
            else:
                print('- This command is not available!')
                # exec(command)

        except Exception as e:
            M.error('- Error while executing the command')
            M.error(f"REASON: {e}")
    M.wait(1) # time for closing threads
    print("- Client session is shutting down")
        
    # ----------------------------------------------------------------------------
