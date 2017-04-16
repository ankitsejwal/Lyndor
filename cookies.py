def addNewLine(cookie,line):

    with file(cookie, 'r') as original: data = original.read()
    with file(cookie, 'w') as modified: modified.write(line + data)
    return modified

def editHexFile(cookie):
    with file(cookie,'r') as f:
        newcontent = f.read().replace("\r\n","\n")

    with file(cookie,'w') as f:
        newfile = f.write(newcontent)
        return newfile

def editCookie(cookie,line):
    addNewLine(cookie,line)
    editHexFile(cookie)
