from pac import get_dirs
def getkey():
    with open(get_dirs.FILE_ENCRYPT_KEY,'rb+') as f:
        key=f.read()
        return key