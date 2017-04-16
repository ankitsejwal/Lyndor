def add_new_line(cookie, line):
    '''returns cookie file with NETSCAPE line'''
    with file(cookie, 'r') as original: data = original.read()
    with file(cookie, 'w') as modified: modified.write(line + data)
    return modified

def edit_hex_file(cookie):
    '''returns cookie file without carriage return'''
    with file(cookie, 'r') as f:
        newcontent = f.read().replace("\r\n", "\n")

    with file(cookie, 'w') as f:
        newfile = f.write(newcontent)
        return newfile

def edit_cookie(cookie, line):
    '''this function edits cookie'''
    add_new_line(cookie, line)
    edit_hex_file(cookie)
