import os
import requests
import sys


def walk_dir(path,prefix=""):
    results=[]
    for f in os.listdir(path):
        if os.path.isfile(path+f):
            results.append(prefix+f)
        if os.path.isdir(path+f):
            results+=walk_dir(path+f+"/",prefix+f+"/")
    return results

def uploadDir(host,basedir):
    requests.delete(url="http://{}/api/fs/dir/html?recurse=true".format(host))
    for f in walk_dir(basedir):
        print(f)
        url = "http://{}/api/fs/file/html/{}".format(host,f)
        file = "{}{}".format(basedir,f)
        print("uploaded {} to {}".format(file,url))
        requests.put(url=url,data=open(file,"rb"))

if __name__ == "__main__":
    if len(sys.argv)<3 :
        print ("Usage: {} <hostname> <local-web-app>".format(sys.argv[0]))
    else :
        uploadDir(sys.argv[1],sys.argv[2])
