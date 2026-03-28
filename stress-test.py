import traceback
import requests
import time
import logging
import threading
import random
import sys
import subprocess
import glob
import os
import hashlib
import re
import xml.dom.minidom
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from requests.auth import HTTPDigestAuth
from requests.auth import HTTPBasicAuth

"""
    !!!!!!!!!!!!! INIZIO CONFIGURAZIONE !!!!!!!!!!!!!!!
"""
#ADMIN_USER="epson"
#ADMIN_PASS="epson"

num_tills = 5               # 15
receipts_per_day = 1       # 800
num_server_zreports = 1     # 3000

PROTOCOL = "https"
SERVER_RT = "192.168.1.136"

THREAD_START_DELAY = 1

MAX_TX_RETRIES = 10
TX_TIMEOUT = 200     # in secondi
TIME_BETWEEN_TOKEN_RECEIPT = 0.500

TIME_BETWEEN_TOKEN_RETRIES = 2
TIME_BETWEEN_RECEIPT_RETRIES = 2

RANDOM_RANGE_MIN = 1
RANDOM_RANGE_MAX = 2

DEBUG_PRINT_REQUESTS = 0
DEBUG_PRINT_REPLIES = 0
DEBUG_REQUESTS_LOGGING = 0

"""
    !!!!!!!!!!!!! FINE CONFIGURAZIONE !!!!!!!!!!!!!!!
"""



"""TOKEN
                         rand   data    z-rep  doc  daily amount
              1           2          3              4
    01234567890 12345678 90123 45678901 2345   6789 012345678
    99SEC000004 AAAA0001 13536 20180515 0051   0001 000006400

    <printerFiscalReceipt>
    <beginFiscalReceipt/>
    <printRecItem description="ID IVA 0" quantity="1" unitPrice="1,00" vatID="0"/>
    <printRecTotal description="PAGAMENTO CONTANTE" index="0" payment="1,00" paymentType="0"/>
    <fiscalInformation cashAmount="1,00" changeAmount="0,00" checkAmount="0,00" dailyAmount="67,00" dateTime="20180517T145145" ePayAmount="0,00" noPayAmount="0,00" paidAmount="1,00" recAmount="1,00" recNumber="0021" recVAT="0,00" serviceAmount="0,00" tillId="AAAA0001" zRepNumber="0051"/>
    <endFiscalReceipt/>
    </printerFiscalReceipt>


Output atteso da inviare a fpserver:

<createReceipt><receipt><hash fingerPrint="99SEC000004AAAA0001142752018052200510048000009300"/><printerFiscalReceipt>
<beginFiscalReceipt/>
<printRecItem description="ID IVA 0" quantity="1" unitPrice="1,0" vatID="0"/>
<printRecTotal description="PAGAMENTO CONTANTE" index="0" payment="1,0" paymentType="0"/>
<fiscalInformation cashAmount="1,0" changeAmount="0,00" checkAmount="0,00" dailyAmount="94,0" dateTime="20180522T110254" docType="0" ePayAmount="0,00" noPayAmount="0,00" paidAmount="1,0" recAmount="1,0" recNumber="0048" recVAT="0,00" tillId="AAAA0001" zRepNumber="0051"/>
<endFiscalReceipt/>
</printerFiscalReceipt></receipt><receiptSecurity><hash fingerPrint="fb5696d00cfe8c3fbf45555cb79781a23545f73191f567621a67e9e3912d1711"/></receiptSecurity></createReceipt>

"""


#print(str(random.uniform(RANDOM_RANGE_MIN, RANDOM_RANGE_MAX)))


class statistic:
    def __init__(self):
        self.transact_num = 0
        self.transact_token_failure = 0
        self.transact_token_timeout_failure = 0
        self.transact_token_exception_failure = 0
        self.transact_receipt_failure = 0
        self.transact_receipt_timeout_failure = 0
        self.transact_receipt_exception_failure = 0
        self.req_time_sum = 0
        self.transact_lt_150ms = 0
        self.transact_gt_300ms = 0
        self.transact_betw_150_300ms = 0

class thrd_info:
    def __init__(self, index):
        till = index + 1
        self.index = till
        self.token_ok = 0
        self.token_required = 1
        self.last_token = ""
        self.daily_amount = 0
        self.rec_per_day = 0
        self.num_till_zrep = 0
        self.fiscalInfo_dailyAmount = 0
        self.fiscalInfo_tillId = "AAAA" + '{:04d}'.format(till)
        self.fiscalInfo_zRepNumber = 0
        self.fiscalInfo_recNumber = 0
        

prefix = """<?xml version="1.0" encoding="UTF-8" standalone="no"?><SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"><SOAP-ENV:Header/><SOAP-ENV:Body>"""
suffix = """</SOAP-ENV:Body></SOAP-ENV:Envelope>"""

xml_token_pre = """<createToken><till tillId="AAAA"""
xml_token_post = """" /></createToken>"""

xml_ctills_pre = """<createTills><user userId = "spagnolo" password = "killalo"/><tills>"""
xml_ctills_post = """</tills></createTills>"""

xml_dclosure_pre = """<createDailyClosure><till tillId="AAAA"""
xml_dclosure_post = """" /></createDailyClosure>"""


def send_token(tillNum, session, statistics):
    
    thrd_index = tillNum - 1

    thread_name = "Thread-" + '{:02d}'.format(tillNum)

    xml_token = xml_token_pre +  '{:04d}'.format(tillNum) + xml_token_post

    tosend = prefix + xml_token + suffix
    print ("\n**** TOKEN REQUEST ****\n")
    if DEBUG_PRINT_REQUESTS:
        print(tosend)

    logfile = open(thread_name + ".log", "a")
    logfile.write("\n**** TOKEN REQUEST ****\n")
    logfile.write(tosend)
    logfile.close()

    threads_info[thrd_index].token_ok = 0

    try:
        ####
        # Con l'autenticazione Digest la connessione viene resettata ogni volta (provato in http)
        #r = session.post("http://" + SERVER_RT + "/cgi-bin/fpserver.cgi", stream=False, verify=False, auth=HTTPDigestAuth('epson', 'epson'), data=tosend)
        ####
        start = time.time()
        r = session.post(PROTOCOL + "://" + SERVER_RT + "/cgi-bin/fpserver.cgi", stream=False, verify=False, auth=HTTPBasicAuth('epson', 'epson'), data=tosend, timeout=TX_TIMEOUT)
        end = time.time()
        #time.sleep(1)
        time.sleep(TIME_BETWEEN_TOKEN_RETRIES)

        transact_time = end - start
        statistics.req_time_sum = statistics.req_time_sum + transact_time
        if transact_time < 0.150:
            statistics.transact_lt_150ms += 1
        elif transact_time > 0.300:
            statistics.transact_gt_300ms += 1
        else:
            statistics.transact_betw_150_300ms += 1

        print("tempo transazione attuale          " + str(transact_time))

        response = r.text
        print ("\n**** TOKEN RESPONSE ****\n")
        #print(response)
        if DEBUG_PRINT_REPLIES:
            print(response)

        logfile = open(thread_name + ".log", "a")
        logfile.write("\n**** TOKEN RESPONSE ****\n")
        logfile.write(response)

        if response.find("success=\"true\"") != -1:
            logfile.write("\nTOKEN OK\n")
            print ("\nTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
            logfile.write("tempo transazione token OK:   " + str(transact_time) + "\n")
            logfile.close()

            root = xml.etree.ElementTree.fromstring(response)
            token = root[0][0][0][1].text
            #print(token)
            threads_info[thrd_index].last_token = token

            threads_info[thrd_index].token_ok = 1
        else:
            logfile.write("\nTOKEN ERROR\n")
            logfile.write("tempo transazione token ERR:   " + str(transact_time) + "\n")
            logfile.close()
            print ("\nTTTTTTTTEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            statistics.transact_token_failure += 1

    except requests.exceptions.Timeout:
        statistics.transact_token_timeout_failure += 1
        logfile = open(thread_name + ".log", "a")
        logfile.write("\n**** TOKEN ERROR Timed Out ****\n")
        logfile.close()
        print("Timed Out")
    except requests.exceptions.RequestException as e:
        statistics.transact_token_exception_failure += 1
        logfile = open(thread_name + ".log", "a")
        logfile.write("\n**** TOKEN ERROR Exception " + str(e) + "\n")
        logfile.close()
        print(str(e))

    statistics.transact_num += 1

    if threads_info[thrd_index].token_ok == 0:
        threads_info[thrd_index].last_token = ""

    return threads_info[thrd_index].token_ok


def send_receipt(tillNum, session, statistics):

    thrd_index = tillNum - 1

    thread_name = "Thread-" + '{:02d}'.format(tillNum)

    token = threads_info[thrd_index].last_token

    token_serial =  token[:11]
    token_till =    token[11:19]
    token_random =  token[19:24]
    token_date =    token[24:32]
    token_zrep =    token[32:36]
    token_ndoc =    token[36:40]
    token_damount = token[40:]
    #print(token_serial)
    #print(token_till)
    #print(token_random)
    #print(token_date)
    #print(token_zrep)
    #print(token_ndoc)
    #print(token_damount)

    #fiscal_info_dataora = token_date + time.strftime('T%H%M%S')
    fiscal_info_dataora = time.strftime('%Y%m%dT%H%M%S')

    unit_cost = 1.00
    str_unit_cost = str(unit_cost).replace(".", ",")

    saved_dailyAmount = threads_info[thrd_index].fiscalInfo_dailyAmount
    saved_recNumber = threads_info[thrd_index].fiscalInfo_recNumber
    
    if threads_info[thrd_index].token_required == 1:
        updated_damount = (int (int(token_damount)/100 + unit_cost) * 100) / 100
        threads_info[thrd_index].fiscalInfo_dailyAmount = updated_damount
        threads_info[thrd_index].fiscalInfo_zRepNumber = int(token_zrep)
        threads_info[thrd_index].fiscalInfo_recNumber = int(token_ndoc)
    else:
        updated_damount = (int (threads_info[thrd_index].fiscalInfo_dailyAmount + unit_cost) * 100) / 100
        threads_info[thrd_index].fiscalInfo_dailyAmount = updated_damount
        threads_info[thrd_index].fiscalInfo_recNumber = threads_info[thrd_index].fiscalInfo_recNumber + 1

    str_updated_damount = str(updated_damount).replace(".", ",")
        

    top = Element('top')
    prFiscRec = SubElement(top, 'printerFiscalReceipt')
    #prFiscRec = Element('printerFiscalReceipt')
    begFiscRec = SubElement(prFiscRec, 'beginFiscalReceipt')
    prRecItem = SubElement(prFiscRec, 'printRecItem')
    prRecItem.set('quantity', '1')
    prRecItem.set('description', 'ID IVA 0')
    prRecItem.set('vatID', '0')
    prRecItem.set('unitPrice', str_unit_cost)
    prRecTot = SubElement(prFiscRec, 'printRecTotal')
    prRecTot.set('payment', str_unit_cost)
    prRecTot.set('index', '0')
    prRecTot.set('description', 'PAGAMENTO CONTANTE')
    prRecTot.set('paymentType', '0')
    fiscalInfo = SubElement(prFiscRec, 'fiscalInformation')
    fiscalInfo.set('dailyAmount', str_updated_damount)
    fiscalInfo.set('tillId', threads_info[thrd_index].fiscalInfo_tillId)
    fiscalInfo.set('zRepNumber', str(threads_info[thrd_index].fiscalInfo_zRepNumber))
    fiscalInfo.set('recNumber', str(threads_info[thrd_index].fiscalInfo_recNumber))
    fiscalInfo.set('dateTime', fiscal_info_dataora)
    fiscalInfo.set('recAmount', str_unit_cost)
    fiscalInfo.set('recVAT', '0,00')
    fiscalInfo.set('cashAmount', str_unit_cost)
    fiscalInfo.set('ePayAmount', '0,00')
    fiscalInfo.set('noPayAmount', '0,00')
    fiscalInfo.set('changeAmount', '0,00')
    fiscalInfo.set('paidAmount', str_unit_cost)
    fiscalInfo.set('checkAmount', '0,00')
    fiscalInfo.set('docType', '0')
    endFiscRec = SubElement(prFiscRec, 'endFiscalReceipt')

    #print (tostring(prFiscRec))
    rough_string = tostring(prFiscRec, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    #print (reparsed.toprettyxml(indent="\t"))
    xml_before_token_and_hash = reparsed.toprettyxml(indent="")
    #print ("xml prima del token")
    #print (xml_before_token_and_hash)

    receipt = Element('receipt')
    rechash = SubElement(receipt, 'hash')
    #rechash.set('fingerPrint', token)
    rechash.set('fingerPrint', threads_info[thrd_index].last_token)
    receipt.extend(top)

    #rec_string = tostring(receipt, 'utf-8')
    rec_string = tostring(receipt, 'utf-8')
    rec_reparsed = xml.dom.minidom.parseString(rec_string)
    xml_before_hash = rec_reparsed.toprettyxml(indent="")
    #print (xml_before_hash)
    to_secure = xml_before_hash.split("\n",1)[1];
    #print ("To be SECURED")
    #print (to_secure)
    to_secure_1 = to_secure.split("\n");
    result_to_secure = ""
    for i in range(3):
        result_to_secure += to_secure_1[i]

    result_to_secure += "\n"
    for i in range(3, len(to_secure_1) - 3):
        result_to_secure += to_secure_1[i]
        result_to_secure += "\n"

    result_to_secure += to_secure_1[len(to_secure_1) - 3]
    result_to_secure += to_secure_1[len(to_secure_1) - 2]

    #print ("To be SECURED elab")
    #print(result_to_secure)

    hash_object = hashlib.sha256(result_to_secure.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    #print(hex_dig)

    result_to_secure_ext = "<tmp>" + result_to_secure + "</tmp>"
    to_embed = xml.etree.ElementTree.fromstring(result_to_secure_ext)

    newdoc_root = Element('createReceipt')
    #hashed_rec = SubElement(newdoc_root, result_to_secure)
    newdoc_root.extend(to_embed)
    security_node = SubElement(newdoc_root, 'receiptSecurity')
    hash_node = SubElement(security_node, 'hash')
    hash_node.set('fingerPrint', hex_dig)

    final_string = tostring(newdoc_root, 'utf-8')
    final_reparsed = xml.dom.minidom.parseString(final_string)
    xml_final = final_reparsed.toprettyxml(indent="")

    filtered = '\n'.join([x for x in xml_final.split("\n") if x.strip()!=''])

    to_output = filtered.split("\n",1)[1];
    output_list = to_output.split("\n");
    output = ""
    for i in range(4):
        output += output_list[i]

    output += "\n"
    for i in range(4, len(output_list) - 6):
        output += output_list[i]
        output += "\n"

    output += output_list[len(output_list) - 6]
    output += output_list[len(output_list) - 5]
    output += output_list[len(output_list) - 4]
    output += output_list[len(output_list) - 3]
    output += output_list[len(output_list) - 2]
    output += output_list[len(output_list) - 1]

    print ("\n**** RECEIPT REQUEST ****\n")
    if DEBUG_PRINT_REQUESTS:
        print(output)

    tosend = prefix + output + suffix

    logfile = open(thread_name + ".log", "a")
    logfile.write("\n**** RECEIPT REQUEST ****\n")
    logfile.write(tosend)
    logfile.write("\n")
    logfile.close()

    completed = 0

    try:
        ####
        # Con l'autenticazione Digest la connessione viene resettata ogni volta (provato in http)
        #r = session.post("http://" + SERVER_RT + "/cgi-bin/fpserver.cgi", stream=False, verify=False, auth=HTTPDigestAuth('epson', 'epson'), data=tosend)
        ####
        start = time.time()
        r = session.post(PROTOCOL + "://" + SERVER_RT + "/cgi-bin/fpserver.cgi", stream=False, verify=False, auth=HTTPBasicAuth('epson', 'epson'), data=tosend, timeout=TX_TIMEOUT)
        end = time.time()
        #time.sleep(1)
        time.sleep(TIME_BETWEEN_RECEIPT_RETRIES)
        transact_time = end - start
        statistics.req_time_sum = statistics.req_time_sum + transact_time
        if transact_time < 0.150:
            statistics.transact_lt_150ms += 1
        elif transact_time > 0.300:
            statistics.transact_gt_300ms += 1
        else:
            statistics.transact_betw_150_300ms += 1

        print("tempo transazione attuale          " + str(transact_time))

        response = r.text
        print ("\n**** RECEIPT RESPONSE ****\n")
        #print(response)
        if DEBUG_PRINT_REPLIES:
            print(response)

        logfile = open(thread_name + ".log", "a")
        logfile.write("\n**** RECEIPT RESPONSE ****\n")
        logfile.write(response)
        print(response)

        if response.find("success=\"true\"") != -1:
            print ("\nRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
            logfile.write("\nRECEIPT OK\n")
            logfile.write("tempo transazione receipt OK:   " + str(transact_time) + "\n")
            logfile.close()
            
            tree = xml.etree.ElementTree.fromstring(response)
            
            """
            print(tree.tag)
            for item in tree.getchildren():
                print(item.tag)
                for subitem in item.getchildren():
                    print(subitem.tag)
                    for subitem1 in subitem.getchildren():
                        print(subitem1.tag)
            #print(root.tag)
            
#            for elem in root.iterfind('soapenv:Envelope/soapenv:Body/response/addInfo/fingerPrint'):
            for elem in tree.iterfind('Envelope/Body/response/addInfo/fingerPrint'):
                print (elem.tag)
                print (elem.text)
            """

            token = tree[0][0][0][4].text
            print(token)

            threads_info[thrd_index].last_token = token
            completed = 1

        else:
            logfile.write("\nRECEIPT ERROR\n")
            logfile.write("tempo transazione ERR:   " + str(transact_time) + "\n\n")
            logfile.close()
            print ("\nRRRRRRRRRRREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            statistics.transact_receipt_failure += 1
            completed = 2

    except requests.exceptions.Timeout:
        statistics.transact_receipt_timeout_failure += 1
        completed = 3
        logfile = open(thread_name + ".log", "a")
        logfile.write("\n**** RECEIPT ERROR Timed Out ****\n")
        logfile.close()
        print("Timed Out")
    except requests.exceptions.RequestException as e:
        statistics.transact_receipt_exception_failure += 1
        completed = 4
        threads_info[thrd_index].fiscalInfo_dailyAmount = saved_dailyAmount
        threads_info[thrd_index].fiscalInfo_recNumber = saved_recNumber
        logfile = open(thread_name + ".log", "a")
        logfile.write("\n**** RECEIPT ERROR Exception " + str(e) + "\n")
        logfile.close()
        print(str(e))

    statistics.transact_num += 1

    return completed


def send_till_closure(tillNum, session, statistics):

    thread_name = "Thread-" + '{:02d}'.format(tillNum)

    xml_dclosure = xml_dclosure_pre + '{:04d}'.format(tillNum) + xml_dclosure_post

    tosend = prefix + xml_dclosure + suffix
    print ("\n**** TILL DAILY CLOSURE REQUEST ****")
    if DEBUG_PRINT_REQUESTS:
        print(tosend)
    logfile = open(thread_name + ".log", "a")
    logfile.write("\n**** TILL DAILY CLOSURE REQUEST ****\n")
    logfile.write(tosend)
    logfile.close()

    completed = 0

    try:
        r = session.post(PROTOCOL + "://" + SERVER_RT + "/cgi-bin/fpserver.cgi", stream=False, verify=False, auth=HTTPBasicAuth('epson', 'epson'), data=tosend)
        response = r.text
        print ("\n**** TILL DAILY CLOSURE RESPONSE ****")
        if DEBUG_PRINT_REPLIES:
            print(response)
        logfile = open(thread_name + ".log", "a")
        logfile.write("\n**** TILL DAILY CLOSURE RESPONSE ****\n")
        logfile.write(response)

        if response.find("success=\"true\"") != -1:
            logfile.write("\nTILL CLOSURE OK\n")
            print ("\nCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")
            logfile.close()
            completed = 1
        else:
            logfile.write("\nTILL CLOSURE ERROR\n")
            logfile.close()
            print ("\nCCCCCCCCCCEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            statistics.transact_token_failure += 1

    except requests.exceptions.Timeout:
        statistics.transact_token_timeout_failure += 1
        logfile = open(thread_name + ".log", "a")
        logfile.write("\n**** TILL CLOSURE ERROR Timed Out ****\n")
        logfile.close()
        print("Timed Out")
    except requests.exceptions.RequestException as e:
        statistics.transact_token_exception_failure += 1
        logfile = open(thread_name + ".log", "a")
        logfile.write("\n**** TILL CLOSURE ERROR Exception " + str(e) + "\n")
        logfile.close()
        print(str(e))

    return completed


def send_token_receipt(tillNum, session, statistics):

    thread_name = "Thread-" + '{:02d}'.format(tillNum)

    xml_token = xml_token_pre +  '{:04d}'.format(tillNum) + xml_token_post

    tosend = prefix + xml_token + suffix
    print ("\n**** TOKEN REQUEST ****\n")
    if DEBUG_PRINT_REQUESTS:
        print(tosend)

    logfile = open(thread_name + ".log", "a")
    logfile.write("\n**** TOKEN REQUEST ****\n")
    logfile.write(tosend)
    logfile.close()

    cnt_retry = 0
    completed = 0
    while cnt_retry < MAX_TX_RETRIES:
        try:
            ####
            # Con l'autenticazione Digest la connessione viene resettata ogni volta (provato in http)
            #r = session.post("http://" + SERVER_RT + "/cgi-bin/fpserver.cgi", stream=False, verify=False, auth=HTTPDigestAuth('epson', 'epson'), data=tosend)
            ####
            start = time.time()
            r = session.post(PROTOCOL + "://" + SERVER_RT + "/cgi-bin/fpserver.cgi", stream=False, verify=False, auth=HTTPBasicAuth('epson', 'epson'), data=tosend, timeout=TX_TIMEOUT)
            end = time.time()
            #time.sleep(1)
            time.sleep(TIME_BETWEEN_TOKEN_RETRIES)

            transact_time = end - start
            statistics.req_time_sum = statistics.req_time_sum + transact_time
            if transact_time < 0.150:
                statistics.transact_lt_150ms += 1
            elif transact_time > 0.300:
                statistics.transact_gt_300ms += 1
            else:
                statistics.transact_betw_150_300ms += 1

            print("tempo transazione attuale          " + str(transact_time))

            response = r.text
            print ("\n**** TOKEN RESPONSE ****\n")
            #print(response)
            if DEBUG_PRINT_REPLIES:
                print(response)

            logfile = open(thread_name + ".log", "a")
            logfile.write("\n**** TOKEN RESPONSE ****\n")
            logfile.write(response)

            if response.find("success=\"true\"") != -1:
                logfile.write("\nTOKEN OK\n")
                print ("\nTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
                logfile.write("tempo transazione token:   " + str(transact_time) + "\n")
                logfile.close()
                completed = 1
                break
            else:
                logfile.write("\nTOKEN ERROR\n")
                logfile.write("tempo transazione token:   " + str(transact_time) + "\n")
                logfile.close()
                print ("\nEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

            statistics.transact_token_failure += 1
            cnt_retry += 1

        except requests.exceptions.Timeout:
            statistics.transact_token_timeout_failure += 1
            cnt_retry += 1
            print("Timed Out")
        except requests.exceptions.RequestException as e:
            statistics.transact_token_exception_failure += 1
            cnt_retry += 1
            print(e)

    statistics.transact_num += 1

    if completed == 0:
        logfile = open(thread_name + ".log", "a")
        logfile.write("\nTOKEN REQUEST FAILED AFTER " + str(cnt_retry) + " RETRIES\n")
        return

    time.sleep(TIME_BETWEEN_TOKEN_RECEIPT)

    root = xml.etree.ElementTree.fromstring(response)
    #print (root[0][0][0][1].text)
    token = root[0][0][0][1].text

    token_serial =  token[:11]
    token_till =    token[11:19]
    token_random =  token[19:24]
    token_date =    token[24:32]
    token_zrep =    token[32:36]
    token_ndoc =    token[36:40]
    token_damount = token[40:]
    #print(token_serial)
    #print(token_till)
    #print(token_random)
    #print(token_date)
    #print(token_zrep)
    #print(token_ndoc)
    #print(token_damount)

    #fiscal_info_dataora = time.strftime('%Y%m%dT%H%M%S')
    fiscal_info_dataora = token_date + time.strftime('T%H%M%S')

    unit_cost = 1.00
    str_unit_cost = str(unit_cost).replace(".", ",")

    updated_damount = (int (int(token_damount)/100 + unit_cost) * 100) / 100
    str_updated_damount = str(updated_damount).replace(".", ",")

    top = Element('top')
    prFiscRec = SubElement(top, 'printerFiscalReceipt')
    #prFiscRec = Element('printerFiscalReceipt')
    begFiscRec = SubElement(prFiscRec, 'beginFiscalReceipt')
    prRecItem = SubElement(prFiscRec, 'printRecItem')
    prRecItem.set('quantity', '1')
    prRecItem.set('description', 'ID IVA 0')
    prRecItem.set('vatID', '0')
    prRecItem.set('unitPrice', str_unit_cost)
    prRecTot = SubElement(prFiscRec, 'printRecTotal')
    prRecTot.set('payment', str_unit_cost)
    prRecTot.set('index', '0')
    prRecTot.set('description', 'PAGAMENTO CONTANTE')
    prRecTot.set('paymentType', '0')
    fiscalInfo = SubElement(prFiscRec, 'fiscalInformation')
    fiscalInfo.set('dailyAmount', str_updated_damount)
    fiscalInfo.set('tillId', token_till)
    fiscalInfo.set('zRepNumber', token_zrep)
    fiscalInfo.set('recNumber', token_ndoc)
    fiscalInfo.set('dateTime', fiscal_info_dataora)
    fiscalInfo.set('recAmount', str_unit_cost)
    fiscalInfo.set('recVAT', '0,00')
    fiscalInfo.set('cashAmount', str_unit_cost)
    fiscalInfo.set('ePayAmount', '0,00')
    fiscalInfo.set('noPayAmount', '0,00')
    fiscalInfo.set('changeAmount', '0,00')
    fiscalInfo.set('paidAmount', str_unit_cost)
    fiscalInfo.set('checkAmount', '0,00')
    fiscalInfo.set('docType', '0')
    endFiscRec = SubElement(prFiscRec, 'endFiscalReceipt')

    #print (tostring(prFiscRec))
    rough_string = tostring(prFiscRec, 'utf-8')
    reparsed = xml.dom.minidom.parseString(rough_string)
    #print (reparsed.toprettyxml(indent="\t"))
    xml_before_token_and_hash = reparsed.toprettyxml(indent="")
    #print ("xml prima del token")
    #print (xml_before_token_and_hash)

    receipt = Element('receipt')
    rechash = SubElement(receipt, 'hash')
    rechash.set('fingerPrint', token)
    receipt.extend(top)

    #rec_string = tostring(receipt, 'utf-8')
    rec_string = tostring(receipt, 'utf-8')
    rec_reparsed = xml.dom.minidom.parseString(rec_string)
    xml_before_hash = rec_reparsed.toprettyxml(indent="")
    #print (xml_before_hash)
    to_secure = xml_before_hash.split("\n",1)[1];
    #print ("To be SECURED")
    #print (to_secure)
    to_secure_1 = to_secure.split("\n");
    result_to_secure = ""
    for i in range(3):
        result_to_secure += to_secure_1[i]

    result_to_secure += "\n"
    for i in range(3, len(to_secure_1) - 3):
        result_to_secure += to_secure_1[i]
        result_to_secure += "\n"

    result_to_secure += to_secure_1[len(to_secure_1) - 3]
    result_to_secure += to_secure_1[len(to_secure_1) - 2]

    #print ("To be SECURED elab")
    #print(result_to_secure)

    hash_object = hashlib.sha256(result_to_secure.encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    #print(hex_dig)

    result_to_secure_ext = "<tmp>" + result_to_secure + "</tmp>"
    to_embed = xml.etree.ElementTree.fromstring(result_to_secure_ext)

    newdoc_root = Element('createReceipt')
    #hashed_rec = SubElement(newdoc_root, result_to_secure)
    newdoc_root.extend(to_embed)
    security_node = SubElement(newdoc_root, 'receiptSecurity')
    hash_node = SubElement(security_node, 'hash')
    hash_node.set('fingerPrint', hex_dig)

    final_string = tostring(newdoc_root, 'utf-8')
    final_reparsed = xml.dom.minidom.parseString(final_string)
    xml_final = final_reparsed.toprettyxml(indent="")

    filtered = '\n'.join([x for x in xml_final.split("\n") if x.strip()!=''])

    to_output = filtered.split("\n",1)[1];
    output_list = to_output.split("\n");
    output = ""
    for i in range(4):
        output += output_list[i]

    output += "\n"
    for i in range(4, len(output_list) - 6):
        output += output_list[i]
        output += "\n"

    output += output_list[len(output_list) - 6]
    output += output_list[len(output_list) - 5]
    output += output_list[len(output_list) - 4]
    output += output_list[len(output_list) - 3]
    output += output_list[len(output_list) - 2]
    output += output_list[len(output_list) - 1]

    print ("\n**** RECEIPT REQUEST ****\n")
    if DEBUG_PRINT_REQUESTS:
        print(output)

    tosend = prefix + output + suffix

    logfile = open(thread_name + ".log", "a")
    logfile.write("\n**** RECEIPT REQUEST ****\n")
    logfile.write(tosend)
    logfile.close()

    cnt_retry = 0
    completed = 0
    while cnt_retry < MAX_TX_RETRIES:
        try:
            ####
            # Con l'autenticazione Digest la connessione viene resettata ogni volta (provato in http)
            #r = session.post("http://" + SERVER_RT + "/cgi-bin/fpserver.cgi", stream=False, verify=False, auth=HTTPDigestAuth('epson', 'epson'), data=tosend)
            ####
            start = time.time()
            r = session.post(PROTOCOL + "://" + SERVER_RT + "/cgi-bin/fpserver.cgi", stream=False, verify=False, auth=HTTPBasicAuth('epson', 'epson'), data=tosend, timeout=TX_TIMEOUT)
            end = time.time()
            #time.sleep(1)
            time.sleep(TIME_BETWEEN_RECEIPT_RETRIES)
            transact_time = end - start
            statistics.req_time_sum = statistics.req_time_sum + transact_time
            if transact_time < 0.150:
                statistics.transact_lt_150ms += 1
            elif transact_time > 0.300:
                statistics.transact_gt_300ms += 1
            else:
                statistics.transact_betw_150_300ms += 1

            print("tempo transazione attuale          " + str(transact_time))

            response = r.text
            print ("\n**** RECEIPT RESPONSE ****\n")
            #print(response)
            if DEBUG_PRINT_REPLIES:
                print(response)

            logfile = open(thread_name + ".log", "a")
            logfile.write("\n**** RECEIPT RESPONSE ****\n")
            logfile.write(response)

            if response.find("success=\"true\"") != -1:
                print ("\nRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
                logfile.write("\nRECEIPT OK\n")
                logfile.write("tempo transazione receipt:   " + str(transact_time) + "\n")
                logfile.close()
                completed = 1
                break
            else:
                logfile.write("\nRECEIPT ERROR\n")
                logfile.write("tempo transazione receipt:   " + str(transact_time) + "\n\n")
                logfile.close()
                print ("\nEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")

            statistics.transact_receipt_failure += 1
            cnt_retry += 1

        except requests.exceptions.Timeout:
            statistics.transact_receipt_timeout_failure += 1
            cnt_retry += 1
            print("Timed Out")
        except requests.exceptions.RequestException as e:
            statistics.transact_receipt_exception_failure += 1
            cnt_retry += 1
            print(e)

    if completed == 0:
        logfile = open(thread_name + ".log", "a")
        logfile.write("\nRECEIPT REQUEST FAILED AFTER " + str(cnt_retry) + " RETRIES\n")

    statistics.transact_num += 1



# Define a function for the thread
def http_req_thrd(thread_num, cnt_server_zreports, num_cycles):
    """ thread_num corrisponde al till """

    thrd_index = thread_num - 1

    if DEBUG_REQUESTS_LOGGING == 1:
        logging.basicConfig(level=logging.DEBUG)

    statistics = statistic()

    thread_name = "Thread-" + '{:02d}'.format(thread_num)
    outfile = open(thread_name, "a") 

    #session = requests.Session()
    cycle = 1
    with requests.Session() as session:

        session.headers['Content-Type'] = 'application/soap+xml; charset=utf-8'

        #while True:
        while cycle <= num_cycles:
            logfile = open(thread_name + ".log", "a")

            logline =  "\n\n"
            logline += "###  " + time.strftime('%Y%m%dT%H%M%S') + "  #######################################################\n"
            logline += "###  SERVER-ZREP: " + str(cnt_server_zreports) + "    TILL: AAAA" + '{:04d}'.format(thread_num) + "    CICLO  " + str(cycle) + "\n"

            print(logline)
            logfile.write(logline)
            logfile.close()

            cnt_retry = 0
            if threads_info[thrd_index].token_required == 1:
                while cnt_retry < MAX_TX_RETRIES:
                    tok_res = send_token(thread_num, session, statistics)
                    if tok_res == 1:
                        break

                if threads_info[thrd_index].token_ok == 0:
                    logfile = open(thread_name + ".log", "a")
                    logline =  "###  " + time.strftime('%Y%m%dT%H%M%S') + "  #######################################################\n"
                    logline += "###  TOKEN FAIL --- SERVER-ZREP: " + str(cnt_server_zreports) + "    TILL: AAAA" + '{:04d}'.format(thread_num) + "    CICLO  " + str(cycle) + "\n"
                    logline += "############################################################\n"
                    print(logline)
                    logfile.write(logline)
                    logfile.close()
                    time_to_sleep = random.uniform(RANDOM_RANGE_MIN, RANDOM_RANGE_MAX)
                    print("SLEEPING  " + str(time_to_sleep))
                    time.sleep(time_to_sleep)
                    cycle += 1
                    continue

            time.sleep(TIME_BETWEEN_TOKEN_RECEIPT)

            cnt_retry = 0
            receipt_ok = 0
            while cnt_retry < MAX_TX_RETRIES:
                rec_res = send_receipt(thread_num, session, statistics)
                if rec_res == 1:
                    threads_info[thrd_index].token_required = 0
                    receipt_ok = 1
                    break
                if rec_res == 2: # se non errore timeout
                    break

            if receipt_ok == 0:
                threads_info[thrd_index].token_required = 1

                logfile = open(thread_name + ".log", "a")
                logline =  "###  " + time.strftime('%Y%m%dT%H%M%S') + "  #######################################################\n"
                logline += "###  RECEIPT FAIL --- SERVER-ZREP: " + str(cnt_server_zreports) + "    TILL: AAAA" + '{:04d}'.format(thread_num) + "    CICLO  " + str(cycle) + "\n"
                logline += "############################################################\n"
                print(logline)
                logfile.write(logline)
                logfile.close()
                
                time_to_sleep = random.uniform(RANDOM_RANGE_MIN, RANDOM_RANGE_MAX)
                print("SLEEPING  " + str(time_to_sleep))
                time.sleep(time_to_sleep)
                #cycle += 1
                continue
                
            #send_token_receipt(thread_num, session, statistics)

            logfile = open(thread_name + ".log", "a")
            logline =  "###  " + time.strftime('%Y%m%dT%H%M%S') + "  #######################################################\n"
            logline += "###  CYCLE OK --- SERVER-ZREP: " + str(cnt_server_zreports) + "    TILL: AAAA" + '{:04d}'.format(thread_num) + "    CICLO  " + str(cycle) + "\n"
            logline += "############################################################\n"
            print(logline)
            logfile.write(logline)
            logfile.close()

            time_to_sleep = random.uniform(RANDOM_RANGE_MIN, RANDOM_RANGE_MAX)
            print("SLEEPING  " + str(time_to_sleep))
            time.sleep(time_to_sleep)
            cycle += 1

        statistics.mean_req_time = statistics.req_time_sum / statistics.transact_num

        outfile.write("\n")
        outfile.write(time.strftime('%Y%m%dT%H%M%S') + "\n")
        outfile.write("n. transazioni totali:                                   " + str(statistics.transact_num) + "\n")
        outfile.write("n. transazioni token fallite per success=\"false\":      " + str(statistics.transact_token_failure) + "\n")
        outfile.write("n. transazioni token fallite per timeout):               " + str(statistics.transact_token_timeout_failure) + "\n")
        outfile.write("n. transazioni token fallite per exception):             " + str(statistics.transact_token_exception_failure) + "\n")
        outfile.write("n. transazioni receipt fallite per success=\"false\":    " + str(statistics.transact_receipt_failure) + "\n")
        outfile.write("n. transazioni receipt fallite per timeout):             " + str(statistics.transact_receipt_timeout_failure) + "\n")
        outfile.write("n. transazioni receipt fallite per exception):           " + str(statistics.transact_receipt_exception_failure) + "\n")
        outfile.write("tempo medio delle transazioni                            " + str(statistics.mean_req_time) + "\n")
        outfile.write("n. transazioni sotto 150ms:                              " + str(statistics.transact_lt_150ms) + "\n")
        outfile.write("n. transazioni tra 150ms e 300ms:                        " + str(statistics.transact_betw_150_300ms) + "\n")
        outfile.write("n. transazioni sopra 300ms:                              " + str(statistics.transact_gt_300ms) + "\n")
        outfile.write("\n")
 
        print("n. transazioni totali:             " + str(statistics.transact_num))
        print("n. transazioni token fallite:      " + str(statistics.transact_token_failure))
        print("n. transazioni receipt fallite:    " + str(statistics.transact_receipt_failure))
        print("tempo medio delle transazioni      " + str(statistics.mean_req_time))
        print("n. transazioni sotto 150ms:        " + str(statistics.transact_lt_150ms))
        print("n. transazioni tra 150ms e 300ms:  " + str(statistics.transact_betw_150_300ms))
        print("n. transazioni sopra 300ms:        " + str(statistics.transact_gt_300ms))
        print("\n")
 
        outfile.close()

        """
        xml_dclosure = xml_dclosure_pre + '{:04d}'.format(thread_num) + xml_dclosure_post

        tosend = prefix + xml_dclosure + suffix
        print ("\n**** TILL DAILY CLOSURE REQUEST ****")
        if DEBUG_PRINT_REQUESTS:
            print(tosend)
        logfile = open(thread_name + ".log", "a")
        logfile.write("\n**** TILL DAILY CLOSURE REQUEST ****\n")
        logfile.write(tosend)
        logfile.close()

        r = session.post(PROTOCOL + "://" + SERVER_RT + "/cgi-bin/fpserver.cgi", stream=False, verify=False, auth=HTTPBasicAuth('epson', 'epson'), data=tosend)
        response = r.text
        print ("\n**** TILL DAILY CLOSURE RESPONSE ****")
        if DEBUG_PRINT_REPLIES:
            print(response)
        logfile = open(thread_name + ".log", "a")
        logfile.write("\n**** TILL DAILY CLOSURE RESPONSE ****\n")
        logfile.write(response)
        logfile.close()
        """

        cnt_retry = 0
        till_closure_ok = 0
        while cnt_retry < MAX_TX_RETRIES:
            till_res = send_till_closure(thread_num, session, statistics)
            if till_res == 1:
                till_closure_ok = 1
                break
 
        print(thread_name + "finished")



def send_server_zrep():
    with requests.Session() as session:

        session.headers['Content-Type'] = 'application/soap+xml; charset=utf-8'

        outfile = open("rt-server.log", "a")
        outfile.write(time.strftime('%Y%m%dT%H%M%S') + "\n")

        xml_report = """<printerFiscalReport>
                        <printZReport operator="1" timeout="600000" />
                        </printerFiscalReport>"""
        tosend = prefix + xml_report + suffix
        print ("\n**** SERVER DAILY CLOSURE REQUEST ****\n")
        print(tosend)

        outfile.write("\n**** SERVER DAILY CLOSURE REQUEST ****\n")
        outfile.write(tosend)

        r = session.post(PROTOCOL + "://" + SERVER_RT + "/cgi-bin/fpmate.cgi", stream=False, verify=False, auth=HTTPBasicAuth('epson', 'epson'), data=tosend)

        response = r.text
        print ("\n**** SERVER DAILY CLOSURE RESPONSE ****\n")
        print(response)
        outfile.write("\n**** SERVER DAILY CLOSURE RESPONSE ****\n")
        outfile.write(response)

        outfile.close()


def create_tills(n_tills):
    """
    <createTills>
        <user userId = "pippo1" password = "AAABBBB" />
	<change add = "AAAA0001" />
	<change remove = "AAAA0004" />
   	<tills>
            <till tillId = "AAAA0001" />
	    <till tillId = "AAAA0002" />
	    <till tillId = "AAAA0003" />
	</tills>
    </createTills>
    """
    with requests.Session() as session:

        session.headers['Content-Type'] = 'application/soap+xml; charset=utf-8'

        tillstr = ""
        for till in range(1, n_tills+1):
            tillstr += "<till tillId = \"AAAA" + '{:04d}'.format(till) + "\" />"

        xml_token = xml_ctills_pre + tillstr + xml_ctills_post

        tosend = prefix + xml_token + suffix

        print ("\n**** CREATE TILLS REQUEST ****")
        print(tosend)

        outfile = open("rt-server.log", "a")
        outfile.write(time.strftime('%Y%m%dT%H%M%S') + "\n")
        outfile.write("\n**** CREATE TILLS REQUEST ****\n")
        outfile.write(tosend)

        r = session.post(PROTOCOL + "://" + SERVER_RT + "/cgi-bin/fpserver.cgi", stream=False, verify=False, auth=HTTPBasicAuth('epson', 'epson'), data=tosend)
        response = r.text
        print ("\n**** CREATE TILLS RESPONSE ****")
        print(response)

        outfile.write("\n**** CREATE TILLS RESPONSE ****\n")
        outfile.write(response)
        outfile.close()


cycles = receipts_per_day

cnt_server_zreports = 0     # 3000

threads_info = []

# Create two threads as follows
try:
    create_tills(num_tills)
    time.sleep(3)
    #sys.exit(1)

    outfile = open("rt-server.log", "w")
    outfile.write("START " + time.strftime('%Y%m%dT%H%M%S') + "\n")
    outfile.close()

    for n_thrd in range(1, num_tills+1):
        thread_name = "Thread-" + '{:02d}'.format(n_thrd)
        outfile = open(thread_name, "w")
        outfile.write("START " + time.strftime('%Y%m%dT%H%M%S') + "\n")
        outfile.close()
        logfile = open(thread_name + ".log", "w") 
        logfile.write("START " + time.strftime('%Y%m%dT%H%M%S') + "\n")
        logfile.close()

    while cnt_server_zreports < num_server_zreports:
        threads = []
        threads_info = []
        for n_thrd in range(1, num_tills+1):
            thread = threading.Thread(target=http_req_thrd, args=(n_thrd, cnt_server_zreports, cycles))
            threads.append(thread)
            threads_info.append(thrd_info(n_thrd - 1))

        # Start them all
        for thread in threads:
            thread.start()
            time.sleep(THREAD_START_DELAY)

        # Wait for all to complete
        for thread in threads:
            thread.join()

        send_server_zrep()

        cnt_server_zreports += 1

    sys.exit(0)

except Exception:
    print ("Error: unable to start thread")
    try:
        exc_info = sys.exc_info()

        # do you usefull stuff here
        # (potentially raising an exception)
        try:
            raise TypeError("Again !?!")
        except:
            pass
        # end of useful stuff


    finally:
        # Display the *original* exception
        traceback.print_exception(*exc_info)
        del exc_info

sys.exit(0)


