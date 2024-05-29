#!/usr/bin/python
import socket 
import time
import sys
import re
import datetime
import json
import csv
import fileinput

emailrule = "(?:[a-z0-9!#$%&'*+\=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
filename = sys.argv[1] 
file = open(filename, 'r') 
Lines = file.readlines() 
  
next = 0
name = ""
action = ""
condition = ""
# Strips the newline character 

for line in Lines: 
    if "name" in line:
    	name = line[6:len(line)-3]
    	next = 1
    if "actionValue" in line:
    	action = line[13:len(line)-3]
    	next +=1
    if "condition" in line:
    	condition = line[11:len(line)-3]
    	next +=1
    if next == 3: #\(sub.*,
    	if(re.search("\(sub.*", condition)):
    		c = re.findall("\[.*\]",condition)
    		folder  = action.replace("imap://spagnolo@imap.isti.cnr.it/","")
    		for e in c:
    			rule = "# rule:[Flagged %s]\n if header :contains \"subject\" \"%s\"  { fileinto \"%s\";}" % (e,e,folder)
    			print rule
    	if(re.search(emailrule, condition)):
    			c = re.findall(emailrule,condition)
    			folder  = action.replace("imap://spagnolo@imap.isti.cnr.it/","")
    			for e in c:
    				rule2 = "# rule:[%s]\n if allof (header :contains \"from\" \"%s\", header :contains \"to\" \"%s\"){ fileinto \"%s\";} " % (e,e,e,folder)
    				print rule2