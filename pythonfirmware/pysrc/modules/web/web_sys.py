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


app = picoweb.WebApp(__name__)
# Default Logging
LOG = logging.getLogger(__name__)


async def _json_response(resp, data, code="200"):
    await picoweb.start_response(resp, content_type="application/json", status=code)
    await resp.awrite(ujson.dumps(data))


async def _json_error(resp, error, msg=None, status="401", payload={}):
    data = {'code': status,
            'error': error}
    if (msg):
        data['message'] = msg
    for k in payload.keys():
        data[k] = payload[k]

    await _json_response(resp, data, status)


async def delayed_reboot(delay):
    LOG.critical("Restarting in {}".format(delay))
    await asyncio.sleep(delay)
    machine.reset()


async def _json_msg(resp, subject, msg=None, status="200", payload={}):
    data = {'code': status,
            'msg': subject}
    if (msg):
        data['long_msg'] = msg
    for k in payload.keys():
        data[k] = payload[k]
    await _json_response(resp, data, status)


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
    await _json_response(resp, result)


BUFFERSIZE = 1024*16


@app.route("/ota/sha256")
async def ota_checksum(req, resp):
    r = req.reader
    active = True
    size = int(req.headers[b"Content-Length"])
    tsize = 0
    checksum = sha256()
    while active:
        buffer = await r.read(BUFFERSIZE)
        active = buffer != None and len(buffer) > 0
        if active:
            tsize += len(buffer)
            checksum.update(buffer)
            if tsize >= size:
                active = False
    await _json_response(resp, {'checksum': ubinascii.hexlify(checksum.digest()).decode()})


last_checksum = ""


@app.route("/ota/activate")
async def ota_upload(req, resp):
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
    await _json_response(resp, result)
    asyncio.get_event_loop().create_task(delayed_reboot(5))


@app.route("/ota/upload")
async def ota_upload(req, resp):
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
    while active:
        buffer = await r.read(blocksize)
        if active:
            blength = len(buffer)
            tsize += blength

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
    await _json_response(resp, result)


@app.route("/sys/reset")
async def sys_restart(req, resp):
    qs = parse_qs(req.qs)
    asyncio.get_event_loop().create_task(delayed_reboot(5))
    await _json_msg(resp, "Restart requested.")
