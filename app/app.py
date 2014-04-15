from googlevoice import Voice
from googlevoice.util import input
import dictmodule
import parsesms
import sys
import BeautifulSoup
import time


def extractsms(htmlsms) :
    """
    extractsms  --  extract SMS messages from BeautifulSoup tree of Google Voice SMS HTML.

    Output is a list of dictionaries, one per message.
    """
    msgitems = []										# accum message items here
    #	Extract all conversations by searching for a DIV with an ID at top level.
    tree = BeautifulSoup.BeautifulSoup(htmlsms)			# parse HTML into tree
    conversations = tree.findAll("div",attrs={"id" : True},recursive=False)
    for conversation in conversations :
        #	For each conversation, extract each row, which is one SMS message.
        rows = conversation.findAll(attrs={"class" : "gc-message-sms-row"})
        for row in rows :								# for all rows
            #	For each row, which is one message, extract all the fields.
            msgitem = {"id" : conversation["id"]}		# tag this message with conversation ID
            spans = row.findAll("span",attrs={"class" : True}, recursive=False)
            for span in spans :							# for all spans in row
                cl = span["class"].replace('gc-message-sms-', '')
                msgitem[cl] = (" ".join(span.findAll(text=True))).strip()	# put text in dict
            msgitems.append(msgitem)					# add msg dictionary to list
    return msgitems
    
voice = Voice()
voice.login()

voice.sms()

sendTo = []
wordDef = []

def getDefinitions():
  sendTo = []
  wordDef = []
  for msg in extractsms(voice.sms.html):
    sendTo.append(str(msg['from']))
    wordDef.append(dict.returnDef(msg['text'].upper()))
  print sendTo
  print wordDef
  print len(wordDef)

def sendDefinitions():
  print len(wordDef)
  for i in range(len(wordDef)):
    print str(wordDef[i]) + "\n" + "Sending to: " + str(sendTo[i])[:-1]
    voice.send_sms(str(sendTo[i])[1:-1], str(wordDef[i]))

def deleteMessages():
  for message in voice.sms().messages:
    message.delete()

def messageHandler():
  sendTo = []
  wordDef = []
  for msg in extractsms(voice.sms.html):
    print str(msg['from'])
    if str(msg['from']) != "Me:":
      sendTo.append(str(msg['from']))
      wordDef.append(dictmodule.returnDef(msg['text'].upper()))
  if len(wordDef) == 0:
    print ("Sorry, no new messages!")
  for i in range(len(wordDef)):
    print str(wordDef[i]) + "\n" + "Sending to: " + str(sendTo[i])[:-1]
    voice.send_sms(str(sendTo[i])[1:-1], str(wordDef[i]))
  deleteMessages()

while True:
  messageHandler()
  time.sleep(5)
