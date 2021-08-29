import os
import requests
def walk_dir(path,prefix=""):
    results=[]
    for f in os.listdir(path):
        if os.path.isfile(path+f):
            results.append(prefix+f)
        if os.path.isdir(path+f):
            results+=walk_dir(path+f+"/",prefix+f+"/")
    return results


requests.delete(url="http://172.17.100.43/fs/dir/html?recurse=true")

basedir="../adminweb/build/"
for f in walk_dir(basedir):
    url = "http://172.17.100.43/fs/file/html/{}".format(f)
    file = "{}{}".format(basedir,f)
    print("uploaded {} to {}".format(file,url))
    requests.put(url=url,data=open(file,"rb"))
