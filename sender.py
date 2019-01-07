import RPi.GPIO as GPIO
import pigpio
import time
tick=0
button_pin = 20
number=1
pig = pigpio.pi()
PRESS_TIME=200
timestamp_dict=[]
def LED_signal(final_lst):
	time.sleep(1)
	word=final_lst.get('word')
	for char in word:
		print(char)
		for key, val in char.items():
			key=int(key)
			val = int(val)
			for n in range(0,key):
				pig.write(26,1)
				time.sleep(0.2)
				pig.write(26,0)
				time.sleep(0.2)
			time.sleep(0.5)
			for n in range(0,val):
				pig.write(26,1)
				time.sleep(0.2)
				pig.write(26,0)
				time.sleep(0.2)
		time.sleep(1)
def do_short():
	timestamp=time.time()
	timestamp_dict.append(timestamp)

def do_long():
	word_ls=[]
	word_ls[:]=[]
	index_lst=[]
	index_lst= timestamp_handling(timestamp_dict)
	final_lst = index_handling(index_lst, word_ls)
	print(final_lst)
	timestamp_dict[:]=[]
	LED_signal(final_lst)


def timestamp_handling(times):
	tmp_lst=[0]
	print('tmp_lst')
	print(tmp_lst)
	for n in range(0, len(times)):
		if n+1 == len(times):
			tmp_lst.append(n+1) # n+1 is final index
			break
		time_subtract= times[n+1]-times[n]
		if time_subtract > 0.5:
			time_index =  times.index(times[n+1])
			tmp_lst.append(time_index)
	return tmp_lst


def index_handling(index_lst, word_ls):
	for n in range(0, len(index_lst), 2):
		try:
			word_ls.append({str(index_lst[n + 1] - index_lst[n]): str(index_lst[n + 2] - index_lst[n + 1])})
		except Exception as e:
			print(e)
	word_to_send={'word': word_ls, 'received': []}
	return word_to_send
def settup():
	pig.set_mode(button_pin, pigpio.INPUT)#cai dat pin la input
	pig.set_mode(26, pigpio.OUTPUT)
	pig.set_pull_up_down(button_pin,pigpio.PUD_UP)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def loop():
	while True:
		state = pig.read(button_pin)
		global number
		if pig.read(button_pin) == False:
			global tick
			tick=tick+1
			print(tick)
		if pig.read(button_pin) == True:
			if tick < 10:
				tick=0
			if 10 < tick < PRESS_TIME:
				do_short()
				tick = 0
			if tick > PRESS_TIME:
				do_long()
				tick = 0
				number=number+1
settup()
loop()
