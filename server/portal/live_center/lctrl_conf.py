#coding:utf-8 
import ConfigParser
import io
import logging
import os
from app_cfg import *

SUPER_APP_ID = '999999'

log_level = 'DEBUG'
log_path = ''
log_mode = 'NET_FILE'

http_ip = '0.0.0.0'
http_port = 9090

bin_ip = '0.0.0.0'
bin_port = 9091

up_sche_secret = "wheretofindTheBestKey.Idonotknown."
up_sche_server_addr = 'lus.xiu.youku.com'
up_sche_server_port = 443
up_sche_server_http_port = 80

pl_sche_secret = "HowCanIFindTheBestKey.JustTry."
pl_sche_server_addr = 'lps.xiu.youku.com'
pl_sche_server_port = 80

http_deflate_toggle = 0

db_server_ip = '127.0.0.1'
db_server_port = 6379
db_server_idx = 1

reporter_ip = '10.10.69.195'
reporter_port = 2111
reporter_pipe = '/tmp/rpt.pip' #supported tcp send

rtmp_app_name = 'trm'

max_stream_count = 3000

app_max_stream_count_default = 300 #app                           300
app_max_transcoding_count_default = 5 #app                              5

app_cfg_secret_key = "IFindkeylcloud.Idonotknown.yklf"

app_cfg_info = None

def dump_conf():
    logging.warning('http_ip:%s', str(http_ip))
    logging.warning('http_port:%s', str(http_port))
    logging.warning('bin_ip:%s', str(bin_ip))
    logging.warning('bin_port:%s', str(bin_port))
    logging.warning('http_deflate_toggle:%s', str(http_deflate_toggle))
    logging.warning('up_sche_secret:%s', str(up_sche_secret))
    logging.warning('up_sche_server_addr:%s', str(up_sche_server_addr))
    logging.warning('up_sche_server_port:%s', str(up_sche_server_port))
    logging.warning('up_sche_server_http_port:%s', str(up_sche_server_http_port))

    logging.warning('pl_sche_secret:%s', str(pl_sche_secret))
    logging.warning('pl_sche_server_addr:%s', str(pl_sche_server_addr))
    logging.warning('pl_sche_server_port:%s', str(pl_sche_server_port))
    logging.warning('log_level_name:%s', str(log_level))
    logging.warning('log_path:%s', str(log_path))

    logging.warning('db_server_ip:%s', str(db_server_ip))
    logging.warning('db_server_port:%s', str(db_server_port))
    logging.warning('db_server_idx:%s', str(db_server_idx))

    logging.warning('reporter_ip:%s', str(reporter_ip))
    logging.warning('reporter_port:%s', str(reporter_port))
    logging.warning('reporter_pipe:%s', str(reporter_pipe))
    logging.warning('rtmp_app_name:%s', str(rtmp_app_name))
    logging.warning('max_stream_count:%d', int(max_stream_count))
    logging.warning('app_max_stream_count_default:%d', int(app_max_stream_count_default))
    logging.warning('app_max_transcoding_count_default:%d', int(app_max_transcoding_count_default))
    logging.warning('app_cfg_info:%s', str(app_cfg_info))

def get_app_max_stream_cnt(app_id):
    global app_cfg_info
    return app_cfg_info.get_max_stream_cnt(app_id)

def dump_conf_safe():
    try:
        dump_conf()
    except Exception as e:
       print('dump_conf_safe exception:' + str(e))


def load_conf(filename):
    try:
        content = open(filename, 'r').read()
        config = ConfigParser.RawConfigParser()
        config.readfp(io.BytesIO(content))

        global http_ip
        global http_port
        global bin_ip
        global bin_port
        global http_deflate_toggle
        global up_sche_secret
        global up_sche_server_addr
        global up_sche_server_port
        global up_sche_server_http_port
        global pl_sche_secret
        global pl_sche_server_addr
        global pl_sche_server_port
        global db_server_ip
        global db_server_port
        global db_server_idx
        global log_level
        global log_path
        global reporter_ip
        global reporter_port
        global reporter_pipe
        global rtmp_app_name
        global log_mode
        global app_cfg_info

        try:
            for item in config.items('app_cfg'):
                if 'max_stream_cfg' == item[0]:
                    if app_cfg_info == None:
                        app_cfg_info = AppCfg(filename, \
                                app_max_stream_count_default, \
                                app_max_transcoding_count_default)
                    app_cfg_info.load(item[1].strip())

        except IOError as e:
            print("parse app_cfg failed! IOError:%s", str(e))

        except Exception as e:
            print("parse app_cfg failed! Exception:%s", str(e))

        for item in config.items('lctrl'):
            if 'http_ip' == item[0]:
                http_ip = item[1].strip()
            elif 'http_port' == item[0]:
                http_port = int(item[1].strip())
            elif 'bin_ip' == item[0]:
                bin_ip = item[1].strip()
            elif 'bin_port' == item[0]:
                bin_port = int(item[1].strip())
            elif 'http_deflate_toggle' == item[0]:
                http_deflate_toggle = int(item[1].strip())
            elif 'up_sche_secret' == item[0]:
                up_sche_secret = item[1].strip()
            elif 'up_sche_server_addr' == item[0]:
                up_sche_server_addr = item[1].strip()
            elif 'up_sche_server_port' == item[0]:
                up_sche_server_port = int(item[1].strip())
            elif 'up_sche_server_http_port' == item[0]:
                up_sche_server_http_port = int(item[1].strip())
            elif 'pl_sche_secret' == item[0]:
                pl_sche_secret = item[1].strip()
            elif 'pl_sche_server_addr' == item[0]:
                pl_sche_server_addr = item[1].strip()
            elif 'pl_sche_server_port' == item[0]:
                pl_sche_server_port = int(item[1].strip())
            elif 'log_level_name' == item[0]:
                log_level = str(item[1].strip())
            elif 'log_mode' == item[0]:
                log_mode = item[1].strip()
            elif 'log_path' == item[0]:
                log_path = item[1].strip()
            elif 'db_server_ip' == item[0]:
                db_server_ip = item[1].strip()
            elif 'db_server_port' == item[0]:
                db_server_port = int(item[1].strip())
            elif 'db_server_idx' == item[0]:
                db_server_idx = int(item[1].strip())
            elif 'reporter_ip' == item[0]:
                reporter_ip = item[1].strip()
            elif 'reporter_port' == item[0]:
                reporter_port = int(item[1].strip())
            elif 'reporter_pipe' == item[0]:
                reporter_pipe = int(item[1].strip())
            elif 'rtmp_app_name' == item[0]:
                rtmp_app_name = item[1].strip()
            elif 'max_stream_count' == item[0]:
                max_stream_count = int(item[1].strip())
                if max_stream_count < 100:
                    max_stream_count = 2000
                elif max_stream_count > 5000:
                    max_stream_count = 5000
                else:
                    pass

    except IOError as e:
        print("can't parse conf:%s", str(e))
    except Exception as e:
        print("can't parse conf:%s", str(e))

    dump_conf_safe()

    if '' == log_path:
        log_path = os.path.dirname(filename)
        log_path = os.path.join(log_path, 'logs')



