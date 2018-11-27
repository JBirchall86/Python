#import serial
import time
import random
import socket
import sys
from tkinter import *

class App():
    def __init__(self, master):
        self.master = master
        master.title("Toby L210 Modem Control")
        self.title_label = Label(master, text="Toby L210 Modem Control")
        
        # Updatable text labels and associated handles
        self.rat_str = "LTE"
        self.rat_str_text = IntVar()
        self.rat_str_text.set(self.rat_str)
        self.rat_str = Label(master, textvariable=self.rat_str_text)

        self.csq_str = "-85dBm"
        self.csq_str_text = IntVar()
        self.csq_str_text.set(self.csq_str)
        self.csq_str = Label(master, textvariable=self.csq_str_text)

        self.packet_str = "0"
        self.packet_str_text = IntVar()
        self.packet_str_text.set(self.packet_str)
        self.packet_str = Label(master, textvariable=self.packet_str_text)

        # Static labels
        self.rat_label = Label(master, text="RAT:")
        self.csq_label = Label(master, text="RSSI:")
        self.packet_label = Label(master, text="Last Tx Size:")
        # Lambda activates update callback to handle button press
        self.init_button = Button(master, text="Initialise Modem", command=lambda: self.update("init"))
        self.close_button = Button(master, text="Close Program", command=master.quit)

        
        v=IntVar()
        Radiobutton(master, text="O2", variable=v, value=1).grid(row=1, column=0, sticky=W)
        Radiobutton(master, text="Vodafone", variable=v, value=2).grid(row=1, column=1, sticky=W)
        Radiobutton(master, text="EE", variable=v, value=3).grid(row=1, column=2, sticky=W)
        v.set(1)
        
        #Position all elements
        #Top row, left
        self.title_label.grid(row=0, column=0, sticky=W, columnspan=3)
        #Middle row, left + right
        self.init_button.grid(row=2, column=0, sticky=W)
        self.close_button.grid(row=2, column=1, sticky=W)
        #Centred, bottom row
        self.rat_label.grid(row=3, column=0, sticky=W)
        self.rat_str.grid(row=3, column=1, sticky=W)
        self.csq_label.grid(row=4, column=0, sticky=W)
        self.csq_str.grid(row=4, column=1, sticky=W)
        self.packet_label.grid(row=5, column=0, sticky=W)
        self.packet_str.grid(row=5, column=1, sticky=W)

        

        # Create sub-grid for packet size numbers
        num_grid = Frame(root)
        # Subgrid spans 3 columns of master grid
        num_grid.grid(columnspan=2)
        numbers = [8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768]
        i = 0
        bttn = []
        for j in range(2):
            for k in range(6):
                bttn.append(Button(num_grid, text = numbers[i]))
                bttn[i].grid(row = j+6, column = k, pady = 5)
                bttn[i]["command"] = lambda x = numbers[i]: self.TX_UDP(x)
                i += 1
        # Init serial port
        #ser = serial.Serial('/dev/ttyACM0', baudrate = 115200)
        #ser.close()
        #ser.open()
        
    def send_AT(self, AT_command, AT_timeout):
        # Flush buffers
        ser.flushInput()
        ser.flushOutput()
        ser.timeout = AT_timeout
        transmission = str(AT_command + '\r\n')
        ser.write(bytes(transmission, 'UTF-8'))
        try:
            raw_data = ser.readline()
            raw_data = ser.readline()
 
            raw_data = str(raw_data.rstrip())
        except SerialTimeoutException:
            print("No response from modem")
            sys.exit
        finally:
            if raw_data.rstrip == 'OK':
                return 'OK'
            elif raw_data.rstrip() == 'ERROR':
                print ('Error with AT command: ' + AT_command)
                sys.exit
            else:
                ser.flushInput()
                return raw_data.rstrip()
        
    def get_ser_lev(self, raw):
        if raw == 0:
            self.rat_str = 'GSM'
            self.rat_str_text.set(self.rat_str)
        elif raw == 1:
            self.rat_str = 'GSM Compact'
            self.rat_str_text.set(self.rat_str)
        elif raw == 2:
            self.rat_str = 'UTRAN'
            self.rat_str_text.set(self.rat_str)
        elif raw == 3:
            self.rat_str = 'GSM with EDGE'
            self.rat_str_text.set(self.rat_str)
        elif raw == 4:
            self.rat_str = 'UTRAN with HSDPA'
            self.rat_str_text.set(self.rat_str)
        elif raw == 5:
            self.rat_str = 'UTRAN with HSUPA'
            self.rat_str_text.set(self.rat_str)
        elif raw == 6:
            self.rat_str = 'UTRAN with HSDPA and HSUPA'
            self.rat_str_text.set(self.rat_str)
        elif raw == 7:
            self.rat_str = 'LTE'
            self.rat_str_text.set(self.rat_str)
        else:
            self.rat_str = 'RAT Error'
            self.rat_str_text.set(self.rat_str)
        

    def get_sig_str(self, raw):
        if raw == 0:
            self.csq_str = '-113dBm or less'
            self.csq_str_text.set(self.csq_str)
        elif raw == 1:
            self.csq_str = '-111dBm'
            self.csq_str_text.set(self.csq_str)
        elif raw >= 2 & raw <=30:
            self.csq_str = (str(-113 + (2* raw)) + 'dBm')
            self.csq_str_text.set(self.csq_str)
        elif raw == 31:
            self.csq_str = '-51dBm or greater'
            self.csq_str_text.set(self.csq_str)
        else:
            self.csq_str = 'Signal strength error'
            self.csq_str_text.set(self.csq_str)
        
    def update(self, method):
        if method == "init":
            ser = serial.Serial('/dev/ttyACM0', baudrate = 115200)
            ser.timeout = 1
            ser.close()
            ser.open()
            # Turn echo off
            send_AT('ATE0', 1)
            # Check modem is working
            send_AT('AT', 1)
            send_AT('AT+CFUN=1', 1)
            time.sleep(2)
            #Select lte ONLY
            #send_AT('AT+URAT=3', 1)
            #send_AT('AT+CREG=1', 1)
            # Check for connection to network
            service = 0
            print("Searching for network connection")
  
            while service != 1:
                response = send_AT('AT+CEREG?', 1)
                data=response.rstrip("'").split(',')
                service=int(data[1])
                time.sleep(1)
                print(".", end='')

            # Get USB context stuff:
            response = send_AT('AT+UUSBCONF?', 1)
    
            # Get IP address of PDP context
            #send_AT('AT+CGDEL=1', 1)
            print('Please select network\n 1: O2\n 2: Vodafone/n 3: EE')
            Network = int(input('Selection:'))
    
            if Network == 1:
                send_AT('AT+CGDCONT=1,"IP","payandgo.o2.co.uk"',1)
                sent_AT('AT+UAUTHREQ=1,1,"payandgo","password"',1)
                sent_AT('AT+CGACT=1,1',1)
            elif Network == 2:
                send_AT('AT+CGDCONT=1,"IP","pp.vodafone.co.uk"',1)
                sent_AT('AT+UAUTHREQ=1,1,"wap","wap"',1)
                sent_AT('AT+CGACT=1,1',1)
            elif Network == 3:
                send_AT('AT+CGDCONT=1,"IP","everywhere"',1)
                sent_AT('AT+UAUTHREQ=1,1,"eesecure","secure"',1)
                sent_AT('AT+CGACT=1,1',1)
            else:
                print('Network selection error!')
                sys.exit
    
            response = send_AT('AT+CGDCONT?', 3)
            data = response.rstrip().split('"')
            print('IP address associated with PDP context:')
            PDP_IP=data[5]
            print(PDP_IP)
    
            # Get USB virtual IP address 
            response = send_AT('AT+UIPADDR=2', 3)
            data = response.rstrip().split('"')
            interface = data[1]
            USB_IP = data[3]
            print('Virtual IP:')
            print(USB_IP)
    
    
            # Build config strings
            Cntxt_str = 'sudo ifconfig usb0 192.168.1.149 netmask 255.255.255.0'
            Alias_str = ('sudo ifconfig ' + str(interface) +' '+str(PDP_IP)+ ' netmask 255.255.255.255 pointopoint ' + str(USB_IP) +' up')
            Gatew_str = ('sudo route add default gw ' + str(USB_IP))
            # Configure internal networking settings
            print(Cntxt_str)
            print(Alias_str)
            print(Gatew_str)
            os.system(Cntxt_str)
            os.system(Alias_str)
            os.system(Gatew_str)
            print("Modem Configured")
            # Close port
            ser.close()
            print("Modem Initialised")
            
        elif method == "quit":
            master.quit
        else:
            print("Balls")
        
    def TX_UDP(self, Datasize):
        UDP_IP = "78.145.243.132"
        UDP_PORT = 5004
        #try:
            #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #except socket.error:
            #print ('Failed to create socket')
        
        #Filename = 'output_file_' + str(Datasize)
        #f=open(Filename, 'rb')
        #data = f.read()
        #f.close()
        #try:
            #s.sendto(data, (UDP_IP, UDP_PORT))
        
            #response = send_AT('AT+COPS?', 1)
            #data = response.rstrip("'").split('"')
            #Serv_lev=data[2].split(",")
            #get_ser_lev(int(Serv_lev[1]))

            #response = send_AT('AT+CSQ', 1)
            #data = response.rstrip("'").split(' ')
            #Sig_qual=data[1].split(",")
            #get_sig_str(int(Sig_qual[0]))
        #except socket.error:
            #print ('Error Code: ')

        
        self.packet_str = Datasize
        self.packet_str_text.set(self.packet_str)

        
root = Tk()
sum1 = App(root)



        


    

root.mainloop()
