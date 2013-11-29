from app.controller import Logic
from ast import literal_eval
import datetime, time

def get_price():
	logicObject = Logic.Logic()
	feedback = logicObject.execute("getprice",None)
	print feedback.getinfo()

def main():
	fname = "activepricefrequncy.txt"
	try:
		with open(fname):
			f = open(fname, "r")
			contentdata = f.read()
			list_content = contentdata.split(';')
			del list_content[0]
			for i in range(len(list_content)):
				eachitem = literal_eval(list_content[i])
				if i == 0:
					pricefreq = eachitem["activepricefreq"]
				elif i == 1:
					starttime = eachitem["starttime"]
				elif i == 2:
					endtime = eachitem["endtime"]
				
			print pricefreq, starttime, endtime
			#print list_content, type(list_content)

	except IOError:
		no_file = {'update':'No file'}


	#get_price()
	while True:
		currenttime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		if currenttime == endtime:
			get_price()
			print "reached"
			starttime = endtime
			endtimedelta = datetime.datetime.strptime(endtime,'%Y-%m-%d %H:%M:%S' )
			endtimedelta = endtimedelta + datetime.timedelta(minutes = int(pricefreq))
			endtime = endtimedelta.strftime('%Y-%m-%d %H:%M:%S')
			print endtime, starttime
if __name__ == '__main__':
	main()
