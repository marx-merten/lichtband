import ulogging as logging
import picoweb
import uasyncio as asyncio
import gc
import ujson
from uhashlib import sha256
import ubinascii
import machine
import esp32
import uos
from picoweb.utils import parse_qs
from web.utils import _json_error,_json_msg,_json_response,_txt_response,_cors_header


import utime as time


app = picoweb.WebApp(__name__)
# Default Logging
LOG = logging.getLogger(__name__)

corsHeader={'Access-Control-Allow-Origin':'*'}



def convert_to_ISOTime(time_val):
    (year, month, day, hour, minute, second, _, _) = time.gmtime(time_val)
    return "{}-{}-{}T{}:{}:{}Z".format(year, month, day, hour, minute, second)


async def delayed_reboot(delay):
    LOG.critical("Restarting in {}".format(delay))
    await asyncio.sleep(delay)
    machine.reset()



@app.route("/dump")
async def dump(req, resp):
    LOG.info("{} {}<>{}".format(req.method, req.path, req.qs))
    LOG.info("{}".format(req))

    LOG.info("Headers {}".format(req.headers))
    if req.method == "POST":
        LOG.info("-------------------------------------")
        size = int(req.headers[b"Content-Length"])

        while size > 0:
            l = yield from req.reader.readline()
            size -= len(l)
            LOG.info("{}".format(l))

    LOG.info("-DONE-")
    await _txt_response(resp, "OK")


@app.route("/stats")
async def stats(req, resp):
    result = {}
    result['memory_free'] = gc.mem_free()
    result['memory_alloc'] = gc.mem_alloc()
    currentPartition = esp32.Partition(esp32.Partition.RUNNING)
    p = {}
    (p['type'], p['subtype'], p['addr'], p['size'], p['label'], p['encrypted']) = currentPartition.info()
    result['current_partition'] = p
    os = {}
    (os['sysname'], os['nodename'], os['release'], os['version'], os['machine']) = uos.uname()
    result['uname'] = os

    (bsize, _, size, _, free, _, _, _, _, _) = uos.statvfs("/")
    fs = {'size_kb': (size*bsize)/1024,
          'size_blocks': size,
          'avail_kb': (free*bsize)/1024,
          'avail': (free*bsize),
          'avail_blocks': free}
    result['fs'] = fs
    result['timestamp']= convert_to_ISOTime(time.time())

    await _json_response(resp, result,headers=corsHeader)


BUFFERSIZE = 1024*16


@app.route("/ota/sha256")
async def ota_checksum(req, resp):
    r = req.reader
    active = True
    size = int(req.headers[b"Content-Length"])
    tsize = 0
    checksum = sha256()
    lastProgress=0
    while active:
        buffer = await r.read(BUFFERSIZE)
        active = buffer != None and len(buffer) > 0
        if active:
            tsize += len(buffer)
            percent = (tsize*100//size)
            if percent-lastProgress>5:
                LOG.info("Progress {}".format(percent))
                lastProgress=percent
            checksum.update(buffer)
            if tsize >= size:
                active = False
    await _json_response(resp, {'checksum': ubinascii.hexlify(checksum.digest()).decode()},headers=corsHeader)


last_checksum = ""


@app.route("/ota/activate")
async def ota_activate(req, resp):
    if req.method == "OPTIONS":
        await _cors_header(resp)
        return
    result = {'status': 'restart'}
    LOG.debug(req.headers.keys())
    if not b'X-OTA-CHECKSUM' in req.headers.keys():
        await _json_error(resp, "No Checksum", "checksum header required.")
        return
    csum = req.headers[b'X-OTA-CHECKSUM'].decode()
    LOG.debug(csum)
    if csum != last_checksum:
        await _json_error(resp, "wrong Checksum", payload={"last_checksum": last_checksum})
        return
    partition = esp32.Partition(esp32.Partition.RUNNING).get_next_update()
    blocksize = partition.ioctl(5, 0)
    (_, _, result['addr'], _, result['part_label'], _) = partition.info()
    partition.set_boot()
    await _json_response(resp, result,headers=corsHeader)
    asyncio.get_event_loop().create_task(delayed_reboot(5))


#TODO Operate with bigger Buffer
@app.route("/ota/upload")
async def ota_upload(req, resp):
    if req.method == "OPTIONS":
        await _cors_header(resp)
    elif req.method == "POST" or req.method == "PUT":
        global last_checksum
        r = req.reader
        active = True
        size = int(req.headers[b"Content-Length"])
        tsize = 0
        block = 0
        partition = esp32.Partition(esp32.Partition.RUNNING).get_next_update()
        blocksize = partition.ioctl(5, 0)

        checksum = sha256()
        (_, _, addr, _, label, _) = partition.info()
        LOG.info("Write to partition {} ({})".format(label, addr))
        oldbuf = b''
        lastProgress=0
        while active:
            buffer = await r.read(blocksize)
            if active:
                blength = len(buffer)
                tsize += blength
                percent = (tsize*100//size)
                if percent-lastProgress>5:
                    LOG.info("Progress {}".format(percent))
                    lastProgress=percent

                # Process buffer in Blocksize
                if len(oldbuf) > 0:
                    buffer = oldbuf+buffer
                    oldbuf = b''
                while (len(buffer) >= blocksize):
                    write_buffer = buffer[:blocksize]
                    checksum.update(write_buffer)
                    buffer = buffer[blocksize:]
                    partition.writeblocks(block, write_buffer)
                    block += 1
                if len(buffer) > 0:
                    oldbuf = buffer

                if tsize >= size:
                    blength = len(buffer)
                    if (blength > 0):
                        LOG.debug(blength)
                        checksum.update(buffer)
                        filler = bytearray(blocksize-blength)
                        for i in range(len(filler)):
                            filler[i] = 0xff
                        write_buffer = buffer+filler
                        LOG.debug(len(write_buffer))

                        partition.writeblocks(block, write_buffer)
                        block += 1
                    active = False
        last_checksum = ubinascii.hexlify(checksum.digest()).decode()
        result = {
            'target_partition': label,
            'size': tsize,
            'blocks': block,
            'sha256': last_checksum
        }
        LOG.info("DONE.")
        await _json_response(resp, result,headers=corsHeader)


@app.route("/sys/reset")
async def sys_restart(req, resp):
    qs = parse_qs(req.qs)
    asyncio.get_event_loop().create_task(delayed_reboot(5))
    await _json_msg(resp, "Restart requested.",headers=corsHeader)
