
import ujson

import ulogging as logging
LOG = logging.getLogger(__name__)

def i_read (stack,data):
    LOG.debug("{} search for {}".format(stack[0],stack[1:]))

    value = None
    if stack[0] in data.keys():
        value = data[stack[0]]
        if len(stack)>1 :
            value = i_read(stack[1:],value)
    return value

def i_write (stack,data,value):
    LOG.debug("{} search for {}".format(stack[0],stack[1:]))
    if not stack[0] in data.keys():
        ndata={}
        data[stack[0]]=ndata
    if len(stack) == 1 :
        data[stack[0]] = value
    else:
        i_write(stack[1:],data[stack[0]],value)

class Config:
    def __init__(self,filename="./cfg.json"):
        self.filename = filename
        try:
            with open(filename) as f :
                self.cfgjson = ujson.load(f)
                f.close()
                self.dirty=False
        except OSError:
            # Open failed, assuming new File
            self.dirty=True
            self.cfgjson={}


    def get(self,name):
        stack=name.split("/")
        return i_read(stack,self.cfgjson)

    def write(self,name,value):
        stack=name.split("/")
        oldValue = i_read(stack,self.cfgjson)
        if not oldValue == value :
            i_write(stack,self.cfgjson,value)
            self.dirty=True

    def save(self):
        with open(self.filename,"w") as f:
            ujson.dump(self.cfgjson,f)
            f.close()
            self.dirty=False
