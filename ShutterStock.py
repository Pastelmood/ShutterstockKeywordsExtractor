import urllib.request
import urllib.parse
import os, sys


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


def callNotePad(text):
    filename = 'temp.txt'
    saveFile = open(filename, 'w')
    saveFile.write(text)
    saveFile.close()

    osCommandString = "notepad.exe " + filename
    os.system(osCommandString)


print()
print('+-----------------------------------+')
print('+  ShutterStock Keywords Extractor  +')
print('+-----------------------------------+')
print()
print('Press q for exit')
print()


try:
    while True:
        url = input('[ShutterStock] > ')

        if url == 'q':
            sys.exit()

        if url[:5] == 'https':
            sourceCode = getSource(url)
            if len(sourceCode) > 0:
                keyWords = getKeyword(sourceCode)
                if len(keyWords) > 0:
                    callNotePad(keyWords)

except Exception as e:
    sys.exit()
