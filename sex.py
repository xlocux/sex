import os
import sys
import requests,re,argparse,random,json
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor, as_completed


colors = ["red","green","yellow","blue","magenta","cyan","white"]
patterns = json.load(open("patterns.json", "r"))
patterns = list(zip(patterns.keys(), patterns.values()))
alreadyfound = []

ap = argparse.ArgumentParser()
ap.add_argument("--dir", required=True,help="Set directory")
ap.add_argument("--threads",required=True,help="Threads")
ap.add_argument("--colorless",required=False,help="Colorless", action='store_true')
args = vars(ap.parse_args())
threadPool = ThreadPoolExecutor(max_workers=int(args["threads"]))
path = args["dir"]

def printResult(name,key,url):
	if not key in alreadyfound:
		if args["colorless"] == True:
			print("Name: {}, Key: {}, URL: {}".format(name,key,url))
			pass
		else:
			print(colored("Name: {}, Key: {}, URL: {}".format(name,key,url),random.choice(colors)))
			pass
		alreadyfound.append(key)
		pass
	pass

def extractSecrets(url):
	f=open(url, "r")
	if f.mode == 'r':
		contents =f.read()
					
		for p in patterns:
			thePattern = r"[:|=|\'|\"|\s*|`|´| |,|?=|\]|\|//|/\*}]("+p[1]+r")[:|=|\'|\"|\s*|`|´| |,|?=|\]|\}|&|//|\*/]"
			findPattern = re.findall(re.compile(thePattern),contents)
			findPattern and [printResult(str(p[0]),str(result),url) for result in findPattern]
			pass
		pass


try:
	
	files = []
	# r=root, d=directories, f = files
	for r, d, f in os.walk(path):
		for file in f:
			files.append(os.path.join(r, file))
        
            
	for f in files:
		threadPool.submit(extractSecrets,f)
		pass
	pass
except KeyboardInterrupt as e:
	threadPool.shutdown(wait=False)
	pass
	







