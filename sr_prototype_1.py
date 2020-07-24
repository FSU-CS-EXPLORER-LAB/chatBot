import speech_recognition as sr
import socket
import time
import re
import pyttsx3
try:
    from urllib import quote, urlopen, urlencode  # Python 2.X
except ImportError:
    from urllib.parse import quote, urlencode  # Python 3+
    from urllib.request import urlopen  # Python 3+


def submitInformation(url,parameters):
    print(3)
  #  encodedParams =  urlencode(parameters);  # encode the parameters
 #   encodedParams = encodedParams.encode('utf-8')
    encodedParams  = dictionary2URI(parameters);    # encode the parameters
    encodedParams = encodedParams.encode('utf-8')
    print(4)
    net = urlopen(url,encodedParams);        # Post the data.
    print(5)
    return(net.read());                             # return the result.


def dictionary2URI(theDictionary) :

    encoded = '';           # Initialize the string to return
    for key, value in theDictionary.items():

        # Encode each item in the dictionary.
        encoded += quote(key)+"="+quote(value)+"&";

    remove = re.compile('&$')             # Remove the trailing ampersand.
    encoded = remove.sub('',encoded);

    return(encoded);

def listen_small():
    pass

def listen_large():
    pass

def listen_medium():
     recognizer = sr.Recognizer()
     mic = sr.Microphone(sample_rate = 8000, chunk_size = 1024)
     with mic as source:
          recognizer.adjust_for_ambient_noise(source)
          captured_audio = recognizer.record(source=mic, duration=3)
          try:
               rec = recognizer.recognize_google(captured_audio)
          except sr.UnknownValueError:
               rec = 'Unknown'
          print(rec)
     return rec

def speak(engine, text, person=None):
        if person == 'Mark':
             engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Fred')
        elif person == 'Tony':
             engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')
        elif person == 'Ryan':
             engine.setProperty('voice', 'com.apple.speech.synthesis.voice.veena')
        else:
             engine.setProperty('voice', 'com.apple.speech.synthesis.voice.Alex')
        engine.say(text)
        engine.runAndWait()

def parseRecvMsg(info):
        persons = []
        messages = []
        allMsg = []
        allMsg = info.split('~')
        for i in allMsg:
             persons.append(i.split(':')[0])
             messages.append(i.split(':')[1])
        return (persons,messages)

npcDict = {}
npcNames = []
command1 = ['raise', 'Raise', 'hand', 'Hand']
command2 = ['Nod', 'nod', 'Head', 'head', 'not', 'Not']
command3 = ['Draw', 'draw', 'Map', 'map']
command4 = ['Understand', 'understand', 'Everyone', 'everyone']
command5 = ['Need', 'need', 'Example', 'example','Examples','examples']
host_name = socket.gethostname()
hostId = '{}'.format(host_name)
engine = pyttsx3.init()
more = 'Y'
url = ''
name = ''
welcomeMessage = 'Hi everyone, welcome. To begin, kindly please enter the N.P.C. Name with their U.R.L.'
speak(engine=engine,text=welcomeMessage)
op_msg1 = 'Please enter the U.R.L. and name for the N.P.C. To enter more press Y. When you are done please press N'
speak(engine=engine,text=op_msg1)
while more == 'Y' or more == 'y' or more == 'Yes' or more == 'yes':
        print("Please enter the url and name for the npc")
        url = input('Enter the URL : ')
        name = input('Enter the name of the NPC : ')
        name = name.strip().upper()
        npcDict[name] = url
        npcNames.append(name)
        more = input('Do you want to enter more NPC :')

while(1):
    name = input('Please enter the person you want to send the message to : ')
    name = name.strip().upper()
    url = npcDict.get(name,'')
    if url != '':
        print('Please say your message')
        while True:
                 fullMsg = listen_medium() 
                 if fullMsg == 'Unknown':
                         speak(engine=engine,text='Sorry could not get you')
                 else:
                         break
        print('Processing')   
        command_status = '0'
        command = ''
        person = ''
        msg = ''
        count = 0
        count_1 = 0
        count_2 = 0
        count_3 = 0
        count_4 = 0
        if (fullMsg == 'exit' or fullMsg == 'EXIT'):
                break
        for i in command1:
                 if fullMsg.find(i) != -1:
                         count += 1
        for i in command2:
                 if fullMsg.find(i) != -1:
                         count_1 += 1
        for i in command3:
                 if fullMsg.find(i) != -1:
                         count_2 += 1
        for i in command4:
                 if fullMsg.find(i) != -1:
                         count_3 += 1
        for i in command5:
                 if fullMsg.find(i) != -1:
                         count_4 += 1
        if count == 2:
                 command = '00001'
                 command_status = '1'
                 print("The command is : ",command)
        elif count_1 == 2:
                 command = '00002'
                 command_status = '1'
                 print("The command is : ",command)
        elif count_2 == 2:
                 command = '00003'
                 command_status = '1'
                 print("The command is : ",command)
        elif count_3 == 2:
                 command = '00004'
                 command_status = '1'
                 print("The command is : ",command)
        elif count_4 == 2:
                 command = '00005'
                 command_status = '1'
                 print("The command is : ",command)
        else:
                 print("The message is : ", fullMsg)
        parameters = {'id':hostId,
                  'message':fullMsg,
                  'command_status':command_status,
                  'command_message':command}
        info = submitInformation(url,parameters)
        if info:
            info = info.decode("utf-8").strip()
            person, msg = parseRecvMsg(info)
            print(person,msg)
        for p, m in zip(person, msg):
            speak(engine=engine,text=m,person=p)
    else:
        continue 

