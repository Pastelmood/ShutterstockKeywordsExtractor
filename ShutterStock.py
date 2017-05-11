import urllib.request
import urllib.parse
import os, sys
import imp
import win32clipboard

def getSource(url):
    try:
        # now, with the below headers, we defined ourselves as a simpleton who is
        # still using internet explorer.
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        respData = resp.read()
        respData = respData.decode("utf-8")
        #print(respData)
        return respData

    except Exception as e:
        print(str(e))
        return ''

def getKeyword(sourceCode):
    sourceCode = sourceCode[sourceCode.find('<a href="/search/'):]
    sourceCode = sourceCode[:sourceCode.find('</div>')]

    sourceCode = sourceCode.replace(sourceCode[sourceCode.find('<'):sourceCode.find('>') + 1], '')
    sourceCode = sourceCode.replace(sourceCode[sourceCode.find('</a>') + 4:sourceCode.find('<a')], '')
    sourceCode = sourceCode.replace('</a>', ', ')

    while sourceCode.find('<') != -1:
        sourceCode = sourceCode.replace(sourceCode[sourceCode.find('<'):sourceCode.find('>') + 1], '')

    sourceCode = sourceCode[:-15]

    return sourceCode


def getDescription(sourceCode):
    description = sourceCode
    description = description.replace(description[:description.find('<meta name="description" content="') + 34], '')
    description = description[:description.find(' -')]

    return description


def getNumberOfKeywords(keyWords):
    sumKeywords = keyWords.count(',') + 1

    return sumKeywords


def callNotePad(description, keywords):

    sumKeywords = getNumberOfKeywords(keywords)

    content = '[Title]\n'
    content = content + 'Add title here.\n\n'
    content = content + '[Description]\n'
    content = content + description + '\n\n'
    content = content + '[Keywords]\n'
    content = content + keywords + '\n\n'
    content = content + 'Keywords total = ' + str(sumKeywords) + ' words.'
    
    filename = 'temp.txt'
    saveFile = open(filename, 'w')
    saveFile.write(content)
    saveFile.close()

    osCommandString = "notepad.exe " + filename
    os.system(osCommandString)

def countFromClipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()

    print('\nTotal Keywords = {0}\n'.format(data.count(',') + 1))


# Start Program

mLog = imp.load_compiled("mLog", "lib/Log.pyc")

print()
print('+-----------------------------------+')
print('+  ShutterStock Keywords Extractor  +')
print('+-----------------------------------+')
print()
print('Press q for exit')
print()


try:
    while True:
        url = input('[ShutterStock URL] > ')

        if url == 'q':
            sys.exit()

        if url == 'history':
            mLog.history()

        if url == 'count':
            countFromClipboard()

        if url[:5] == 'https':
            sourceCode = getSource(url)
            if len(sourceCode) > 0:
                keyWords = getKeyword(sourceCode)
                description = getDescription(sourceCode)
                if len(keyWords) > 0:
                    mLog.writeLog(url)
                    callNotePad(description, keyWords)
                    os.remove('temp.txt')

except Exception as e:
    print(str(e))
    sys.exit()
