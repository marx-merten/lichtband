import ulogging as logging
import picoweb
import ujson
from uhashlib import sha256
import ubinascii
import re
import uos as os
from picoweb.utils import parse_qs
from web.utils import _json_error,_json_msg,_json_response,_txt_response
from picoweb import http_error


import utime as time

app = picoweb.WebApp(__name__)
# Default Logging
LOG = logging.getLogger(__name__)


S_IFDIR  = 0o040000  # directory
S_IFREG  = 0o100000  # regular file

BUFFERSIZE = 1024*16


corsHeader={'Access-Control-Allow-Origin':'*'}



def convert_to_ISOTime(time_val):
    (year,month,day,hour,minute,second,_,_) = time.gmtime(time_val)
    return "{}-{}-{}T{}:{}:{}Z".format(year,month,day,hour,minute,second)


def _recurse_path(path,level=0 ,recurse=True):
    try:
        dirs=[]
        for f in os.listdir(path):
            fileinfo ={}
            fileinfo['name']=path+f
            stats = os.stat(fileinfo['name'])
            fileinfo['depth']=level


            fileinfo['timestamp']=int(stats[8])
            fileinfo['time']=convert_to_ISOTime(fileinfo['timestamp'])
            if stats[0] == S_IFREG:
                fileinfo['type']='f'
                fileinfo['size']=int(stats[6])
                dirs.append(fileinfo)
            elif stats[0] == S_IFDIR:
                fileinfo['type']='d'
                fileinfo['size']=0
                dirs.append(fileinfo)
                if recurse:
                    dirs+=_recurse_path(fileinfo['name']+'/',level+1)
        return dirs
    except OSError:
        return []



async def fs_dir_list(req,resp,path):
    result = []
    try:
        result = _recurse_path(path,recurse=False)
        await _json_response(resp,result,headers=corsHeader)
    except OSError:
        LOG.error("Error while retrieving directory")
        await http_error(resp, "404")


async def fs_dir_delete(req,resp,path):
    # if recurse is whished something like this
    # [d['name'] for d in list(filter(lambda info:info['type'] == 'f',dat))]
    # followed by sorted(dat, key= lambda info:info['depth'],reverse=True)
    # with rmdir on all dirs
    # Depth first

    try:
        os.rmdir(path)
        await _json_response(resp,{'deletedPath':path},headers=corsHeader)
    except OSError:
        LOG.error("Error while retrieving directory")
        await http_error(resp, "404")

@app.route(re.compile("/dir(/.*)"))
async def fs_dir(req, resp):
    path = req.url_match.group(1)
    if req.method == "GET":
        await fs_dir_list(req,resp,path)
    elif req.method == "DELETE":
        await fs_dir_delete(req,resp,path)
    else :
        await _json_error(resp,"Method not Supported",payload={'method':req.method},headers=corsHeader)

async def fs_file_delete(req,resp,path):
    try:
        os.remove(path)
        await _json_response(resp,{'deletedPath':path})
    except OSError:
        LOG.error("Error while retrieving directory")
        await http_error(resp, "404")

async def fs_file_get(req,resp,path):
    try:
        LOG.info("Retrieve File {}".format(path))
        await app.sendfile(resp, path,headers=corsHeader)
    except OSError:
        LOG.error("Error while retrieving directory")
        await http_error(resp, "404")


def _file_type(path):
    try:
        stats = os.stat(path)
        return "f" if stats[0] == S_IFREG else "d"
    except OSError:
        return None



@app.route(re.compile("/tree(/.*)"))
async def fs_tree(req, resp):
    path = req.url_match.group(1)
    result =_recurse_path(path)
    await _json_response(resp,result,headers=corsHeader)

def _check_dir(path):
    p = ""
    for segment in path.split('/')[:-1] :
        p=p+'/'+segment
        filetype= _file_type(p)
        if filetype is None:
            os.mkdir(p)

async def fs_file_post(req,resp,path):
    r = req.reader
    active = True
    size = int(req.headers[b"Content-Length"])
    tsize = 0
    checksum = sha256()
    _check_dir(path)
    try:
        with open(path,"w") as outfile:
            while active:
                buffer = await r.read(BUFFERSIZE)
                active = buffer is not None and len(buffer) > 0
                if active:
                    tsize += len(buffer)
                    checksum.update(buffer)
                    outfile.write(buffer)
                    if tsize >= size:
                        active = False
        await _json_response(resp, {'checksum': ubinascii.hexlify(checksum.digest()).decode()})
    except OSError:
        await http_error(resp, "404")


@app.route(re.compile("/file(/.*)"))
async def fs_file(req, resp):
    path = req.url_match.group(1)
    if req.method == "GET":
        await fs_file_get(req,resp,path)
    elif req.method == "DELETE":
        await fs_file_delete(req,resp,path)
    elif req.method == "POST" or req.method == "PUT":
        await fs_file_post(req,resp,path)
    else :
        await _json_error(resp,"Method not Supported",payload={'method':req.method})