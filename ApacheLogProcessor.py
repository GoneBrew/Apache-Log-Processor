#Luke Gleeson
#This program is used to process apache logs. it can do a range of different anaylsis on the data in a log file
#-n; displays the amount of ips which are present in the log file
#-tN; lists N most frequent ip addresses 
#-v ip; lists the amount of visits said ip has made to server
#-L ip; lists all the requests made by said ip
#-d date; lists the amount of times an ip visited the server on said date

#!/usr/bin/env python3
import sys
import re
from collections import Counter

#This function is used to compile a list of dictionaries in which the data will be held
def data_log_compiler():
	file = open(str(sys.argv[2]))
#regex has been coded to only accept defined ip addresses, rejects dummy ips
	reg = re.compile(r'(?P<ip>.{5,15}) \- \- \[(?P<date>.*?)\:(?P<time>.*?) (?P<timezone>.*?)\] \"(?P<request_method>.*?)(?P<path>.*?)(?P<request_version>.*?)\" (?P<status>.*?) (?P<length>.*?) \"(?P<referrer>.*?)\" \"(?P<user_agent>.*?)\"')

	data_log = []
	for line in file:
		if(reg.match(line)!=None):
			data_log.append(reg.match(line).groupdict())
	file.close()
	return data_log
#returns data_log to be used in other functions

#uses the counter from collections to count the unique ips in data_log
def allvisits(data_log):
	ip_counter = Counter(elem['ip'] for elem in data_log)
	print()
	print(len(ip_counter))


#uses the counter from collections to count the unique ips and then uses ".most_common" to order and diplay with amount of requests
def top(data_log):
	ip_counter = Counter(elem['ip'] for elem in data_log)
	for elem in ip_counter.most_common(int(sys.argv[4])):
		print ("\t%s Ip %d Requests" % elem)


#This function counts the amount of visits made by an ip address 
#Therefore must change all times given to seconds.
def indvisits(data_log):
	maxmin=60
	maxhr=3600
	maxday=86400
	ldate='blank'
	lsecs=0
	numip=0
	for elem in data_log:
		if(elem['ip']==sys.argv[4]):
			time=elem['time']
			hr=int(time[0])*10+int(time[1])
			mins=int(time[3])*10+int(time[4])
			secs=int(time[6])*10+int(time[7])
			secs= (hr*maxhr)+(mins*maxmin)+secs
			#must change format of 'time', converts to seconds to compare
			if(elem['date']!=ldate and ((maxday-lsecs)+secs)>maxhr):
				numip+=1
			else:
				if((secs-lsecs)>maxhr):
					numip+=1
			ldate=elem['date']
			lsecs=secs
	if(numip==0):
		numip=1
	print()
	print(numip)


#prints the requests made by an ip, cycles through data_log and if ip found prints out its respective request information
def indlog(data_log):
	for elem in data_log:
		if(elem['ip']==sys.argv[4]):
			print("Ip =", elem['ip'], elem['request_method'], elem['path'], elem['request_version'], elem['status'], elem['length'], elem['referrer'], elem['user_agent'])
			print()

#prints out the amount of visits by all ips on a set date. for date we must remove / which are present in log then compare to the entered date 
def date(data_log):
	ip=[]
	for elem in data_log:
		date=elem['date']
		date=(date[0],date[1],date[3],date[4],date[5],date[7],date[8],date[9],date[10])
		date=''.join(date)
		if(date==sys.argv[4]):
		#make a list of ips which have visited the site then sort the list 
			ip.append(elem['ip'])
	ip_counter = Counter(elem for elem in ip)
	numip=len(ip_counter)
	for elem in ip_counter.most_common(numip):
		print ("\t%s Ip %d Requests" % elem)


def processing():
	print('Processing request...')


def main():
	
	option = sys.argv[3]

	processing()
	
	data_log = data_log_compiler()
	
	if option=='-n':
		allvisits(data_log)

	if option=='-t':
		top(data_log)

	if option=='-v':
		indvisits(data_log)

	if option=='-L':
		indlog(data_log)

	if option=='-d':
		date(data_log)
	
main()						
