#coding:utf-8 
'''
@file upload_url_make.py
@brief make.
       It can be used to generate upload url.
@author renzelong
<pre><b>copyright: Youku</b></pre>
<pre><b>email: </b>renzelong@youku.com</pre>
<pre><b>company: </b>http://www.youku.com</pre>
<pre><b>All rights reserved.</b></pre>
@date 2015/09/23
@see  ./unit_tests/upload_url_make_test.py \n
'''
import const
import ujson
import time
from token_helper import TokenHelper
import lctrl_conf
from data_const_defs import *

const.PC_PLUGIN_UPLOAD = 0 #PC Plug-in Upload 
const.FLASH_CLIENT_UPLOAD = 1 #Flash Client 
const.RTMP_UPLOAD = 2 #RTMP Client 
const.RTP_UPLOAD = 3 #RTP SDK Upload 
const.NET_STREAM_UPLOAD = 4 #net stream Upload 

def make_up_sche_token(stream_id, user_id_str, secret_word):
    curr_time = (int(time.time()) & 0xFFFFFFFF)
    ret = TokenHelper.make_token(curr_time, stream_id, user_id_str, '', secret_word)
    return ret

def get_up_sche_format(request):
    rtmp_app_name   = lctrl_conf.rtmp_app_name      # 'trm'
    client_type = str(request.upload_client_type).strip().lower()
    format = const.PC_PLUGIN_UPLOAD

    if 'fc' == client_type:  # flash client
        format = const.FLASH_CLIENT_UPLOAD

    elif 'rtmp' == client_type:  # rtmp
        format = const.RTMP_UPLOAD

    elif 'rtp' == client_type: #rtp
        format = const.RTP_UPLOAD

    elif 'ns' == client_type: #net_stream
        format = const.NET_STREAM_UPLOAD

    else:
        rtmp_app_name = ''
    return (format, rtmp_app_name)

def make_up_sche_url(request):

    token = make_up_sche_token(request.stream_id, request.user_id_str,
                               lctrl_conf.up_sche_secret)

    user_id         = request.user_id_str
    room_id         = request.room_id_str
    stream_id       = request.stream_id
    (format, rtmp_app_name) = get_up_sche_format(request)

    up_sche_server_addr = lctrl_conf.up_sche_server_addr
    if request.upload_ip_str != '':
        up_sche_server_addr = request.upload_ip_str

    up_sche_server_http_port = lctrl_conf.up_sche_server_http_port
    if request.upload_port_str != '':
        up_sche_server_http_port = request.upload_port_str

    #                     
    if format == const.FLASH_CLIENT_UPLOAD:
         upload_url = '%s://%s:%d/v2/us?uid=%s&rid=%s&a=%s&b=%d&c=%s'
         upload_url %= ('http', up_sche_server_addr,
            up_sche_server_http_port,
            request.user_id_str,
            request.room_id_str,
            token,
            request.stream_id,
            lctrl_conf.rtmp_app_name)
         return (upload_url, token)

     #                     
    elif const.NET_STREAM_UPLOAD == format:
         upload_url = 'http://%s/v1/nus?u=%s&rid=%s&a=%s&b=%d&s=%s&st=%s&r=%s&nt=%s'
         upload_url %= (request.net_stream_upsche_addr,
                       request.user_id_str,
                       request.room_id_str,
                       token,
                       request.stream_id,
                       request.net_stream_media_src,
                       request.net_stream_media_src_type,
                       request.res,
                       request.need_transcoding
                       )
         return (upload_url, token)

    #            rtp               
    if request.need_transcoding == 0:
        upload_url = '%s://%s:%d/v3/us?uid=%s&rid=%s&a=%s&b=%d&f=%s&c=%s'
        upload_url %= ('http', up_sche_server_addr,
            up_sche_server_http_port,
            request.user_id_str,
            request.room_id_str,
            token,
            request.stream_id,
            format,
            rtmp_app_name)
    else:
        upload_url = '%s://%s:%d/v3/us?uid=%s&rid=%s&a=%s&b=%d&f=%s&c=%s&r=%s'
        upload_url %= ('http', up_sche_server_addr,
            up_sche_server_http_port,
            request.user_id_str,
            request.room_id_str,
            token,
            request.stream_id,
            format,
            rtmp_app_name,
            request.res)
    return (upload_url, token)

#return (old, current)
def make_get_upload_url(create_req, ext_para_dict = DEFAULT_EXT_PARAM_DICT):
    try:
        return make_get_upload_url_none_safe(create_req, ext_para_dict)
    except Exception as e:
        logging.error('make_get_upload_url exception:%s', str(e))
    return (None, None)

def make_get_upload_url_none_safe(create_req, ext_para_dict = DEFAULT_EXT_PARAM_DICT):
    (upload_url, upload_token) = make_up_sche_url(create_req)

    upload_url += ext_para_dict['append_content']

    get_upload_dict_old = {"upload_token": str(upload_token),
                           "upload_stream_id": int(create_req.stream_id),
                           "upload_url": upload_url}

    get_upload_dict = {"upload_url": str(upload_url),
                       "error_code": "0",
                       "stream_id": int(create_req.stream_id)}

    return (get_upload_dict_old, ujson.encode(get_upload_dict))


