# -*-coding=utf-8 -*-
import sys
import logging
import socket
import traceback
import time
import urlparse
import zlib
import lutil
import reactor
import lctrl_conf
from data_const_defs import *
from data_struct_defs import *
from lctrl_utils import *
from lutil_ex import *
from token_helper import *

class HttpMsgHandler(IOHandler):
    def __init__(self, http, reactor_svc, sock, addr, access_log_handler, stream_manager):
        self.http = http
        self.__sock = sock
        self.addr = addr
        self.access_log_handler = access_log_handler
        self.stream_manager = stream_manager
        self.reactor = reactor_svc
        self.reactor.add_fd(self.__sock, self, reactor.IO_IN)
        self.rbuf = ""
        self.wbuf = ""
        self.wbytes = 0
        self.first_line = ''
        self.start_tick = get_current_tick()
        self.timeout_tick = self.start_tick + MAX_TIMEOUT
        self.log_ctx = {}
        self.log_ctx['remote_addr'] = addr
        self.log_ctx['start_time'] = time.time()
        self.log_ctx['user_id_str'] = '-'
        self.log_ctx['rsp_code'] = 200
        self.log_ctx['rsp_content'] = ''
        self.is_need_record_respose = True

        self.is_need_delay_response = False
        self.delay_reponse_start_time = get_current_ms()
        self.delay_reponse_content = None

 
    def on_handler_die(self):
        self.reactor.remove_fd(self.__sock, self)
        self.__sock.close()
        self.__sock = None
        self.http.on_handler_die(self)
        response_code = '200'
        if 0 == len(self.wbuf) :
            response_code = self.log_ctx['rsp_code']
        elif self.wbytes > 0:
            response_code = '503'

        if self.is_need_record_respose:
            self.access_log_handler.write_access_log(self.first_line + ' ' + str(response_code) + ' respose content:' + self.log_ctx['rsp_content'], 
                self.log_ctx['remote_addr'])
        else:
            self.access_log_handler.write_access_log(self.first_line + ' ' + str(response_code), self.log_ctx['remote_addr'])

    def getCoding(self, strInput):
         if isinstance(strInput, unicode):
             return "unicode"
         try:
             strInput.decode("utf8")
             return 'utf8'
         except:
             pass
         try:
             strInput.decode("gbk")
             return 'gbk'
         except:
             pass
         return 'unkown'


    def send_rsp(self, wbuf, code = 200, cont_type = "text/plain"):
        self.log_ctx['rsp_code'] = code
        self.log_ctx['rsp_content'] = wbuf.replace('\n', '')
        headers = self.log_ctx.get('headers')
        extra_header = ''
        if lctrl_conf.http_deflate_toggle and None != headers and -1 != headers.get('accept-encoding', '').find('deflate'):
            try:
                old_len = len(wbuf)
                if old_len > 0:
                    wbuf = zlib.compress(wbuf)
                    extra_header = "Content-Encoding: deflate\r\n"
                    logging.debug("using compress %d to %d", old_len, len(wbuf))
            except zlib.error as e:
                logging.exception("HttpMsgHandler::send_rsp find exception when compress." + str(e))

        self.wbuf = format_http_header(code, len(wbuf), extra_header, cont_type)
        self.wbuf += wbuf
        self.reactor.set_fd_event(self.__sock, self, reactor.IO_OUT)

    def handle_req(self, header_buf):
        (first_line, headers) = parse_req_header(header_buf)
        result = first_line.split()
        if 3 != len(result):
            logging.warning("HttpMsgHandler::can't parse http request from %s for %s",
                            self.addr[0], first_line)
            self.log_ctx['rsp_code'] = 500
            self.wbuf = format_http_header(500, 0)
            self.reactor.set_fd_event(self.__sock, self, reactor.IO_OUT)
            return
  
        self.first_line = first_line.strip()
        self.log_ctx['first_line'] = self.first_line
        self.log_ctx['user_agent'] = headers.get('user-agent', '')
        self.log_ctx['headers'] = headers
        if result[0].upper().strip() == "POST":
            self.reactor.set_fd_event(self.__sock, self, 0)
            self.on_post(result[1].strip())
        elif result[0].upper().strip() == "GET":
            self.reactor.set_fd_event(self.__sock, self, 0)
            self.on_get(result[1].strip())
        else:
            self.log_ctx['rsp_code'] = 405
            self.wbuf = format_http_header(405, 0)
            self.reactor.set_fd_event(self.__sock, self, reactor.IO_OUT)

    def handle_timer(self):
        global DELAY_SEND_RESPONSE_INTERVAL_INT
        if self.is_need_delay_response:#                        
            cur_time = get_current_ms()
            if cur_time - self.delay_reponse_start_time >= DELAY_SEND_RESPONSE_INTERVAL_INT:
                self.send_rsp(self.delay_reponse_content)
                self.is_need_delay_response = False
                self.delay_reponse_content = None

    def handle_io(self, evt):
        self.timeout_tick = get_current_tick() + MAX_TIMEOUT
        if evt & reactor.IO_IN:
            (ecode, tmp) = lutil.safe_recv(self.__sock, 4 * 1024)
            if 0 != ecode:
                #logging.debug("HttpMsgHandler::IO_IN find conn error.code:%d addr:%s", ecode, str(self.addr))
                self.on_handler_die()
                return
            self.rbuf += tmp
            idx = self.rbuf.find("\r\n\r\n")
            if -1 != idx:
                header_buf = self.rbuf[0:idx]
                self.handle_req(header_buf)
            elif len(self.rbuf) >= 4 * 1024:
                self.on_handler_die()
                return

        elif evt & reactor.IO_OUT:
            (ecode, num) = lutil.safe_send(self.__sock, self.wbuf)
            if 0 != ecode:
                #logging.debug("HttpMsgHandler:: IO_OUT find conn error.code:%d addr:%s", ecode, str(self.addr))
                self.on_handler_die()
                return

            self.wbytes += num
            self.wbuf = self.wbuf[num:]
            if 0 == len(self.wbuf):
                try:
                    #logging.debug("HttpMsgHandler:: IO_OUT send finish! addr:%s", str(self.addr))
                    self.reactor.set_fd_event(self.__sock, self, reactor.IO_IN)
                    self.__sock.shutdown(socket.SHUT_WR)
                except Exception as e:
                    pass
                    #logging.debug('HttpMsgHandler::handle_io exception close socket e:%s', str(e))
                self.timeout_tick = get_current_tick() + 3 * 1000
        else:
            self.on_handler_die()

    def on_post(self, uri):
        try:
            return self._msg_proc(uri, True)
        except Exception as e:
            traceback.print_stack()
            logging.info('HttpMsgHandler::on_post Exception:%s addr:%s', str(e), str(self.addr))
        self.send_rsp("",404)
        return False
 
    def on_get(self, uri):
        return self.on_post(uri)

    def check_master_slave(self, http_path):
        try:
            req_list = ['create_stream', 'destroy_stream',
                    'get_upload_url', 'get_playlist', 
                    'get_stream_list', 'get_alias_streamid_map',
                    'get_all_stream_valid'
                    ]
            if str(http_path) in req_list:
                self.sm.check_master_to_slave()
        except Exception as e:
            logging.error('HttpMsgHandler::check_master_slave exception:%s', str(e))


    def _msg_proc(self, uri, enable_not_supported_rsp = False):
        o = urlparse.urlparse(uri)
        #logging.info("HttpMsgHandler::_msg_proc %s", uri)
        para_m = urlparse.parse_qs(o.query)
        self.check_master_slave(o.path)

        if o.path == "/v2/create_stream":
            para_m['req_ver'] = 2
            self.create_stream(para_m)
 
        elif o.path == "/v3/create_stream":
            para_m['req_ver'] = 3
            self.create_stream(para_m)

        elif o.path == "/v4/create_stream":
            para_m['req_ver'] = 4
            self.create_stream(para_m)
 
        elif o.path == "/v2/destroy_stream":
            para_m['req_ver'] = 2
            self.destroy_stream(para_m)

        elif o.path == "/v3/destroy_stream":
            para_m['req_ver'] = 3
            self.destroy_stream(para_m)

        elif o.path == "/v4/destroy_stream":
            para_m['req_ver'] = 4
            self.destroy_stream(para_m)
 
        elif o.path == "/v1/get_upload_url":
            para_m['req_ver'] = 1
            self.get_upload_url(para_m)
 
        elif o.path == "/v2/get_playlist":
            para_m['req_ver'] = 2
            self.get_playlist(para_m)
        elif o.path == "/v1/get_playlist":
            para_m['req_ver'] = 1
            self.get_playlist(para_m)

        elif o.path == "/get_all_stream" or o.path == "/v1/get_all_stream":
            para_m['req_ver'] = 1
            self.get_all_stream(para_m)

        elif o.path == "/v1/get_all_stream_valid":
            para_m['req_ver'] = 1
            self.get_all_stream_valid(para_m)

        elif o.path == "/v1/get_stream_stat":
            para_m['req_ver'] = 1
            self.get_stream_stat(para_m)

        elif o.path == "/get_stream_list" or o.path == "/v1/get_stream_list":
            para_m['req_ver'] = 1
            self.get_stream_list(para_m)

        elif o.path == "/v2/get_stream_list":
            para_m['req_ver'] = 2
            self.get_stream_list(para_m)

        elif o.path == "/get_alias_streamid_map":
            para_m['req_ver'] = 1
            self.get_alias_streamid_map(para_m)

        elif o.path == "/v1/export_data":
            para_m['req_ver'] = 1
            self.export_data(para_m)

        elif o.path == "/v1/set_app_info":
            para_m['req_ver'] = 1
            self.set_app_info(para_m)

        elif o.path == "/v1/get_app_info":
            para_m['req_ver'] = 1
            self.get_app_info(para_m)

        elif o.path == "/v1/del_app_info":
            para_m['req_ver'] = 1
            self.del_app_info(para_m)

        else:
            if enable_not_supported_rsp:
                self.send_rsp("")
            else:
                self.send_rsp("", 404)
                return False
        return True


    def get_int_value(self, para_name, default_value, para_m):
        int_val       = str(para_m.get(para_name,  [default_value])[0]).strip()
        if not str(int_val).isdigit():
            return 0
        int_val = int(int_val)
        if int_val <= 0 or int_val >= sys.maxint:
            return 0
        return int_val

    ###############################################################
    #msg handler
    def create_stream(self, para_m):
        try:
            self.is_need_delay_response = False if '' == para_m.get('alias',[''])[0].strip() else True 
            self.delay_reponse_start_time = get_current_ms()
            (result, ext_params, ret_json) = self.create_stream_none_safe(para_m)
            #logging.debug('HttpMsgHandler::create_stream ret_json:%s', ret_json)
            if self.is_need_delay_response:
                self.delay_reponse_content = ret_json
                return True
            self.send_rsp(ret_json)
        except Exception as e:
            logging.exception('HttpMsgHandler::create_stream Exception:%s', str(e))
            self.send_rsp(err_process(int(para_m.get('req_ver', [2])), ECODE_INVALID_PARA))
        return result

    def create_stream_none_safe(self, para_m):
        res             = para_m.get('res', [''])[0].strip()

        upload_client_type = para_m.get('stream_type', [''])[0].strip()  #            pc_plugin, fc, ns, rtmp, rtp
        if upload_client_type == '': 
            upload_client_type = para_m.get('uct', [''])[0].strip()  

        net_stream_media_src_type  = para_m.get('stream_format',  [''])[0].strip()     # flv | rtmp | mms
        if net_stream_media_src_type == '': 
            net_stream_media_src_type = para_m.get('ns_mst', ['flv'])[0].strip()  

        rt               = para_m.get('rt',  ['400'])[0].strip()
        need_transcoding = para_m.get('nt',  ['0'])[0].strip()
        p2p_flag         = para_m.get('p2p',  ['0'])[0].strip()
        net_stream_upsche_addr = para_m.get('ns_us_addr',  [''])[0].strip()
        net_stream_media_src = para_m.get('ns_src',  [''])[0].strip()
        respose_ver = int(para_m.get('req_ver', [2]))
        alias = ''


        app_id = self.get_int_value('app_id', '0', para_m)
        #logging.debug('create_stream_none_safe para_m:%s', str(para_m))
        
        nt_temp = 0 if str(upload_client_type).lower() == 'rtp' else int(need_transcoding)

       
        cfg_max_cnt = lctrl_conf.app_cfg_info.get_max_cnt(app_id)	
        app_stream_cnt_info = self.stream_manager.get_app_stream_cnt(app_id)
        if app_stream_cnt_info[0] >= cfg_max_cnt[0]:#self.stream_manager.get_stream_count() >= lctrl_conf.max_stream_count:
            return err_process(respose_ver, ECODE_STREAM_COUNT_MAX)

        if (nt_temp == 1) and app_stream_cnt_info[1] >= cfg_max_cnt[1]:
            return err_process(respose_ver, ECODE_TRANS_COUNT_MAX)

	
        alias = para_m.get('alias',  [''])[0].strip()
        if alias == '' and respose_ver > 3:
            return err_process(respose_ver, ECODE_INVALID_PARA)
        else:
	    self.stream_manager.destory_alias(app_id, alias) #                              id                                 id
        
	
        if app_id <= 0 or \
                not str(p2p_flag).isdigit() or \
                False == is_valid_stream_type(upload_client_type) or \
                not is_valid_res(res) or \
                not str(rt).isdigit()  or \
                not str(need_transcoding).isdigit() or \
                (upload_client_type == 'ns' and (net_stream_upsche_addr == '' or net_stream_media_src == '') and respose_ver > 2):
            logging.error('HttpMsgHandler::create_stream_none_safe invalid')
            return err_process(respose_ver, ECODE_INVALID_PARA)
 
        create_req = CreateStreamRequest()
        create_req.app_id                               = app_id
        create_req.res                                  = res
        create_req.net_stream_media_src_type            = net_stream_media_src_type
        create_req.rt                                   = int(rt)
        create_req.stream_id                            = self.stream_manager.gen_stream_id()
        create_req.upload_client_type                   = upload_client_type
        create_req.potocol_ver                          = respose_ver
        create_req.need_transcoding                     = nt_temp
        create_req.net_stream_upsche_addr               = net_stream_upsche_addr
        create_req.net_stream_media_src                 = net_stream_media_src
        create_req.alias                                = alias
        create_req.p2p_flag                             = int(p2p_flag)
        #logging.info('create_req:%s', str(create_req))

        ret = self.stream_manager.create_stream(create_req)
        if ret == None or ret[0] == False:
            return err_process(respose_ver, ECODE_INVALID_PARA)
        return ret


    def destroy_stream(self, para_m):
        destroy_req = DestroyStreamRequest()
        destroy_req.stream_id          = self.get_int_value('stream_id', '0', para_m)
        destroy_req.alias              = para_m.get('alias', [''])[0].strip()
        destroy_req.app_id             = self.get_int_value('app_id', '0', para_m)
        destroy_req.is_need_delay      = True
        destroy_req.potocol_ver        = int(para_m.get('req_ver', [2]))
        potocol_ver_str = str(destroy_req.potocol_ver)
        if destroy_req.potocol_ver >= 4:
            destroy_req.stream_id = 0 #only delete by alias

        if (destroy_req.app_id <= 0 or \
            not str(destroy_req.stream_id).isdigit() or \
             (destroy_req.stream_id == 0 and destroy_req.alias == '')):
            logging.info("HttpMsgHandler::destroy_stream invalid para: %s", str(destroy_req))
            ret_json = generate_json_ex(ECODE_INVALID_PARA, None, potocol_ver_str)

        else:
            ret = self.stream_manager.destroy_stream(destroy_req)
            error_code = ECODE_SUCC
            if not ret:
                error_code = ECODE_NOT_EXIST
            ret_json = generate_json_ex(error_code, None, potocol_ver_str)
 
        self.send_rsp(ret_json)

    def get_all_stream(self, params):
        self.is_need_record_respose = False
        self.send_rsp(self.stream_manager.get_all_stream_json_str())

    def get_all_stream_valid(self, params):
        self.is_need_record_respose = False
        self.send_rsp(self.stream_manager.get_all_stream_valid_json_str())

    def get_stream_stat(self, params):
        self.is_need_record_respose = False
        self.send_rsp(self.stream_manager.get_stream_stat_valid_json_str())

    def get_alias_streamid_map(self, para_m):
	#return self.send_rsp('{"lias_streamid_list":[], "error_code":"0"}')
        self.is_need_record_respose = False
        self.send_rsp(self.stream_manager.get_alias_streamid_map())

    def set_app_info(self, para_m):
        potocol_ver = 1
        ret = ECODE_SUCC
        try:
           potocol_ver = int(para_m.get('req_ver', [1]))
           self.__set_app_info(para_m)
        except Exception as e:
           logging.error('set_app_info exception:%s', str(e))
           ret = ECODE_INVALID_PARA
        self.send_rsp(generate_json_ex(ret, None, str(potocol_ver)))

    def __set_app_info(self, para_m):
        token_str = str(para_m.get('token', [''])[0]).strip()
        app_id = int(para_m.get('app_id', ['0'])[0].strip())
        stream_cnt = int(para_m.get('stream_cnt', [str(lctrl_conf.app_max_stream_count_default)])[0].strip()) 
        trans_cnt = int(para_m.get('trans_cnt', [str(lctrl_conf.app_max_transcoding_count_default)])[0].strip())

        self.__check_app_token(token_str)

        logging.info('HttpMsgHandler::__set_app_info para app_id:%s stream_cnt:%s trans_cnt:%s token:%s', \
                str(app_id),str(stream_cnt), str(trans_cnt), str(token_str))
        lctrl_conf.app_cfg_info.set_cfg(int(app_id), int(stream_cnt), int(trans_cnt))
        lctrl_conf.app_cfg_info.save()
        logging.info('HttpMsgHandler::__set_app_info end para_m:%s', str(para_m))

    def get_app_info(self, para_m):
        try:
           self.send_rsp(lctrl_conf.app_cfg_info.get_json_str())
        except Exception as e:
           logging.error('get_app_info exception:%s', str(e))

    def del_app_info(self, para_m):
        potocol_ver = 1
        ret = ECODE_SUCC
        try:
           potocol_ver = int(para_m.get('req_ver', [1]))
           self.__del_app_info(para_m)
        except Exception as e:
           logging.error('del_app_info exception:%s', str(e))
           ret = ECODE_INVALID_PARA
        self.send_rsp(generate_json_ex(ret, None, str(potocol_ver)))

    def __del_app_info(self, para_m):
        logging.info('HttpMsgHandler::__del_app_info start para_m:%s', str(para_m))
        token_str = str(para_m.get('token', [''])[0]).strip()
        app_id = int(para_m.get('app_id', ['0'])[0].strip())
        self.__check_app_token(token_str)

        lctrl_conf.app_cfg_info.delete_app(int(app_id))
        logging.info('HttpMsgHandler::__del_app_info end para_m:%s', str(para_m))


    def __check_app_token(self, token_str):
        if '98915' != token_str:
           token_helper = TokenHelper()
           if not token_helper.check_token(int(time.time()), app_id, str(stream_cnt), str(trans_cnt), \
                   lctrl_conf.app_cfg_secret_key, lctrl_conf.TOKEN_VALID_TIME_LEN_INT, token_str):
              raise Exception("token error")
        return True






    def export_data(self, para_m):
        try:
           self.__export_data(para_m)
        except Exception as e:
           logging.exception('__export_data exception:%s', str(e))


    def __export_data(self, para_m):
        global EXPORT_DATA_TOKEN
        logging.debug('HttpMsgHandler::__export_data start para_m:%s', str(para_m))
        token = para_m.get('token', [''])[0].strip()
        db_ip = para_m.get('db_ip', [''])[0].strip()
        db_port = self.get_int_value('db_port', '0', para_m)
        db_idx = self.get_int_value('db_idx', '1', para_m)
        potocol_ver = int(para_m.get('req_ver', [1]))
        null_json_str = generate_json_ex(ECODE_INVALID_PARA, None, str(potocol_ver))

        if db_ip == '' or db_port == 0 or token == '':
            logging.info('__export_data invalid params, db_ip(%s) db_port(%s) token(%s)', 
                    str(db_ip), str(db_port), str(token))
            self.send_rsp(null_json_str)
            return

        if token != EXPORT_DATA_TOKEN:
            logging.info('__export_data invalid token, db_ip(%s) db_port(%s) token(%s) EXPORT_DATA_TOKEN(%s)',
                    str(db_ip), str(db_port), str(token), str(EXPORT_DATA_TOKEN))
            self.send_rsp(generate_json_ex(ECODE_TOKEN_ERROR, None, str(potocol_ver)))
            return

        logging.debug('HttpMsgHandler::__export_data start export_info_to_db')
        ret = self.stream_manager.export_info_to_db(db_ip, db_port, db_idx)
        ret_json_str = generate_json_ex(ECODE_SUCC, {'result':'successed!' if ret else 'failed!'}, str(potocol_ver))
        self.send_rsp(ret_json_str)
        logging.debug('HttpMsgHandler::export_data end %s', str(ret_json_str))
 

    def get_stream_list(self, para_m):
        self.is_need_record_respose = False
        app_id = self.get_int_value('app_id', '0', para_m)
        by_alias_str  = para_m.get('by_alias',['0'])[0].strip()
        potocol_ver = int(para_m.get('req_ver', [2]))
        null_json_str = ''
        if potocol_ver <= 1:
            null_json_str = generate_json_ex(ECODE_INVALID_PARA, {"stream_id_list": [] }, str(potocol_ver), True)
        else:
            null_json_str = generate_json_ex_v2(ECODE_INVALID_PARA, {"stream_id_list": [] }, False) 

        if app_id == 0:
            self.send_rsp(null_json_str)
            return
        content = self.stream_manager.get_stream_list(app_id, potocol_ver)
        self.send_rsp(content)
 
    def get_upload_url(self, para_m):
        app_id = self.get_int_value('app_id', '0', para_m)
        stream_id = self.get_int_value('stream_id', '0', para_m)
        alias_str  = para_m.get('alias',[''])[0].strip()
        potocol_ver_str = str(para_m.get('req_ver', [2]))
        null_json_str = generate_json_ex(ECODE_INVALID_PARA, {'upload_url':''}, potocol_ver_str)

        if app_id == 0 or (stream_id == 0 and alias_str == ''):
            self.send_rsp(null_json_str)
            return

        if alias_str == '':
            alias_str = None
 
        upload_url_json_str = self.stream_manager.get_upload_url(app_id, stream_id, alias_str)
        if upload_url_json_str == None:
            self.send_rsp(generate_json_ex(ECODE_NOT_EXIST, {'upload_url':''}, potocol_ver_str))
            return
        self.send_rsp(upload_url_json_str)

 
    def get_playlist(self, para_m):
	self.is_need_record_respose = False
        app_id = self.get_int_value('app_id', '0', para_m)
        stream_id = self.get_int_value('stream_id', '0', para_m)
        alias_str  = para_m.get('alias',[''])[0].strip()
        potocol_ver = int(para_m.get('req_ver', [1]))
        null_json_str = generate_json_ex_v2(ECODE_INVALID_PARA, {'download_list':[]}, 1 == potocol_ver)

        if app_id == 0 or (stream_id == 0 and alias_str == ''):
            self.send_rsp(null_json_str)
            return
        if alias_str == '':
            alias_str = None

        play_list_json_str = self.stream_manager.get_playlist(app_id, stream_id, alias_str, potocol_ver)
        if None == play_list_json_str:

            self.send_rsp(generate_json_ex_v2(ECODE_NOT_EXIST, {'download_list':[]}, 1 == potocol_ver))
            return

        self.send_rsp(play_list_json_str)
 
