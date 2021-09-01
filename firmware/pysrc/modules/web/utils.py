import picoweb
import ujson


async def _txt_response(resp, data, code="200", content_type="text/plain",headers={}):
    await picoweb.start_response(resp, content_type=content_type, status=code,headers=headers)
    await resp.awrite(data)


async def _json_response(resp, data, code="200",headers={}):
    await picoweb.start_response(resp, content_type="application/json", status=code,headers=headers)
    await resp.awrite(ujson.dumps(data)+"\n")


async def _json_error(resp, error, msg=None, status="401", payload={},headers={}):
    data = {'code': status,
            'error': error}
    if (msg):
        data['message'] = msg
    for k in payload.keys():
        data[k] = payload[k]

    await _json_response(resp, data, status,headers=headers)


async def _cors_header(resp,methods=['GET','POST','PUT','DELETE'],age=86400,origin='*',headers={}):
    headers['Access-Control-Allow-Origin']=origin
    headers['Access-Control-Allow-Methods']=", ".join(methods)
    headers['Access-Control-Max-Age']=str(age)
    headers['Access-Control-Allow-Headers']="*"
    await picoweb.start_response(resp, status="204",headers=headers)

async def _json_msg(resp, subject, msg=None, status="200", payload={},headers={}):
    data = {'code': status,
            'msg': subject}
    if (msg):
        data['long_msg'] = msg
    for k in payload.keys():
        data[k] = payload[k]
    await _json_response(resp, data, status,headers=headers)
