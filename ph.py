import string
import pylibftdi
from pylibftdi.device import Device
from pylibftdi.driver import FtdiError
from pylibftdi import Driver
import os
import time
import socket
import datetime

server_ip = '174.164.61.190'  # for website server, 174.164.61.190. For Local device, localhost
server_port = 49152  

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server (receiver)
client_socket.connect((server_ip, server_port))


class AtlasDevice(Device):

	def __init__(self, sn):
		Device.__init__(self, mode='t', device_id=sn)


	def read_line(self, size=0):
		"""
		taken from the ftdi library and modified to 
		use the ezo line separator "\r"
		"""
		lsl = len('\r')
		line_buffer = []
		while True:
			next_char = self.read(1)
			if next_char == '' or (size > 0 and len(line_buffer) > size):
				break
			line_buffer.append(next_char)
			if (len(line_buffer) >= lsl and
					line_buffer[-lsl:] == list('\r')):
				break
		return ''.join(line_buffer)
	
	def read_lines(self):
		"""
		also taken from ftdi lib to work with modified readline function
		"""
		lines = []
		try:
			while True:
				line = self.read_line()
				if not line:
					break
					self.flush_input()
				lines.append(line)
			return lines
		
		except FtdiError:
			print("Failed to read from the sensor.")
			return ''		

	def send_cmd(self, cmd):
		"""
		Send command to the Atlas Sensor.
		Before sending, add Carriage Return at the end of the command.
		:param cmd:
		:return:
		"""
		buf = cmd + "\r"     	# add carriage return
		try:
			self.write(buf)
			return True
		except FtdiError:
			print ("Failed to send command to the sensor.")
			return False
			
			
			
def get_ftdi_device_list():
	"""
	return a list of lines, each a colon-separated
	vendor:product:serial summary of detected devices
	"""
	dev_list = []
	
	for device in Driver().list_devices():
		# list_devices returns bytes rather than strings
		dev_info = map(lambda x: x, device)
		# device must always be this triple
		vendor, product, serial = dev_info
		dev_list.append(serial)
	return dev_list


if __name__ == '__main__':
	devices = get_ftdi_device_list()
	cnt_all = len(devices)
	index = 0
	dev = AtlasDevice(devices[int(index)])
	dev.send_cmd("C,0") # turn off continuous mode
	time.sleep(1)
	dev.flush()
	while 1:
		dev.send_cmd("R")
		lines = dev.read_lines()
		for i in range(len(lines)):
			if lines[i] != u'*OK\r':
				print("pH: ", lines[i])
				current_datetime = datetime.datetime.now()
				formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
				message = ("pH;" + lines[i] + "/EC;2/Date;" + formatted_datetime)
				client_socket.sendall(message.encode())
		time.sleep(1)
		
client_socket.close()
				 
