import datetime

currentLine = ""
comma = 0
specialWord = ""
specialKey = 0
def start():
    f = open("interpretedLog.txt", "a")
    f.truncate(0)
    f.close()
    splitter()

def reader():
    f = open("log.txt", "r")
    file = f.read()
    f.close()
    return file;

def output(line):
    f = open("interpretedLog.txt", "a")
    f.write(line)
    f.close()

def addKey(key):
    global currentLine
    global comma
    comma = 0
    currentLine += key

def commaSequence():
    global comma
    comma = 1
    if(specialKey == 1):
        comma = 0
        specialKeySequence()
        return
     
def specialKeySequence():
    global currentLine
    global specialWord
    global specialKey
    if(len(currentLine) > 0):
        currentLine += "\n"
    currentLine += "--" + specialWord
    currentLine += "\n"
    output(currentLine)
    specialWord = ""
    currentLine = ""
    specialKey = 0
    
def splitter():
    log = reader()
    global specialKey
    global comma
    for x in range(len(log)):
        if(log[x] == ","):
            if(comma == 1):
                addKey(log[x])
            else:                   #comma keystroke
                commaSequence()
            continue
        if(log[x+1] == "," and specialKey == 0): #regular keystroke
            addKey(log[x])
            continue
        specialKey = 1
        comma = 0                   #special key sequence
        global specialWord
        specialWord += log[x]
            
def printer():
    print(reader())

start()

