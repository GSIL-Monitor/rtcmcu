#coding:utf-8 
import time
import os
import sys
import logging

from data_struct_defs import *
from lctrl_utils import *
from stream_map import *
from upload_url_make import *
from download_list_make import *
from timeval_t import *
import lpersist
from streaminfo_pack import StreamInfoListPack, StreamInfoPack
from alias_stream_map import *
from alias_stream_manager import *
from export_to_db import *
import lctrl_conf



class StreamManagerBase(TimerNotify):
    def __init__(self, *args, **kwargs):
        self.__stream_map = StreamMap(*args,**kwargs)
        self.__stream_change_subscriber_list = [] 
        self.__sync_data_time_last = int(time.time()) #master/slave sync time last
        self.__is_master = False
        now_ts = int(time.time())
        self.__create_stream_time_last = now_ts
        self.__check_stream_time_last = now_ts
        self.__check_stream_alias_time_last = now_ts
        self.__check_json_time_last = now_ts
        self.__alias_stream_manager = AliasStreamManager()

    #               
    def __add2memory(self, stream_info):
        #add to memory map
        if (stream_info == None) or (not self.__stream_map.add(stream_info.stream_id, stream_info)):
            return False

        return True

     #               
    def __save(self, stream_info):
        #add to memory map
        if not self.__add2memory(stream_info):
            logging.error("StreamManagerBase::__save __stream_map.add failed! stream.%d",stream_info.stream_id)
            return False

        return self.__save_to_db(stream_info)

    def __save_to_db(self, stream_info):
        if stream_info == None:
           return False
        return lpersist.add_key_value(str(stream_info.stream_id), stream_info.to_dict())
        

    #                  
    def __remove(self, destroy_req):
        stream_id = int(destroy_req.stream_id)
        if destroy_req.alias != '':
	    stream_id = self.__alias_stream_manager.get_stream_id(destroy_req.app_id, destroy_req.alias)

        app_id = destroy_req.app_id
        if destroy_req.potocol_ver < 2:
            app_id = None
        return self.__remove_by_stream_id(stream_id, destroy_req.is_need_delay, app_id)


    def __remove_by_stream_id(self, stream_id, is_need_delay, app_id = None):
        stream_id = int(stream_id)
        stream_info = self.__stream_map.get(stream_id)
        if stream_info == None:
            return False

        if app_id != None and app_id != stream_info.app_id:
            return False

        if True == is_need_delay:
            #delay delete stream
            self.__stream_map.remove_delay(stream_id, 1)
            self.__save_to_db(stream_info)
            return True
        return self.__completely_delete_ex(stream_info, True)

    def destory_alias(self, app_id, alias_str, is_need_delay = True):
        try:
	    
	    app_alias_obj = self.__alias_stream_manager.get_alias_obj(app_id, alias_str)
	    if app_alias_obj == None:
	       return
            self.__stream_map.remove_by_stream_id_v2(app_alias_obj.stream_id, is_need_delay, self.__save_to_db)
            self.__alias_stream_manager.completely_delete(alias_str, app_id)
        except Exception as e:
            logging.error("StreamManager::destory_alias exception, alias_str:%s app_id:%s exception:%s",alias_str, str(app_id), str(e))

    #            
    def __completely_delete(self, stream_id, do_destroy = True):
        return self.__completely_delete_ex(self.__stream_map.get(stream_id), do_destroy)

    def __completely_delete_ex(self, stream_info, do_destroy = True):
        if stream_info == None:
            return False

        #remove from memory map
        if not self.__stream_map.remove_by_stream_id(stream_info.stream_id):
            return False

        #remove from redis db
        lpersist.del_key_value(str(stream_info.stream_id))

        self.__safe_notify_destroy(stream_info, do_destroy)

        return True

    def get_stream_count(self):
        return len(self.__stream_map.get_maps())

    def get_app_stream_cnt(self, app_id):
        return self.__stream_map.get_app_stream_cnt(app_id)

    def get_stream_info(self, app_id, stream_id, alias_str, is_valid = True):
        si = None
        try:
            if alias_str != None and alias_str != '':
	        stream_id = int(self.__alias_stream_manager.get_stream_id(int(app_id), alias_str))
                si = self.__stream_map.get(stream_id)
            else:
                if stream_id != None and stream_id != 0:
                    si = self.__stream_map.get(stream_id)
                    if si.app_id != app_id:
                        return None

        except Exception as e:
            logging.warning('StreamManager::get_stream_info exception:%s', str(e))
        return si

    def get_alias_by_stream_id(self, stream_id):
        try:
             si = self.__stream_map.get(int(stream_id))
             if si == None:
                 return None
             return si.alias
        except Exception as e:
             logging.info('StreamManager::get_alias_by_stream_id exception:%s', str(e))
        return None

    def get_all_stream_json_str(self):
        return self.__stream_map.get_all_stream_json_str()

    def get_all_stream_valid_json_str(self):
        return self.__stream_map.get_all_stream_valid_json_str()

    def get_stream_stat_valid_json_str(self):
        return self.__stream_map.get_valid_streamid_stats_json_str()

    def get_stream_info_bin_changed_flag(self):
        return self.__stream_map.get_tream_list_change_state()

    def reset_stream_info_bin_changed_flag(self):
        self.__stream_map.reset_stream_list_change_state()

    def get_stream_info_list_v2(self):
         stream_info_lst = []
         for stream_id in self.__stream_map.get_maps():
	     si = self.__stream_map.get(stream_id)
             stream_info = StreamInfoPack()
             stream_info.stream_id = int(stream_id)
             stream_info.time_val = si.start_time
             stream_info_lst.append(stream_info)
         return stream_info_lst

    def gen_stream_id(self):
         return lpersist.gen_stream_id()


    #                     
    def __safe_notify_destroy(self, si, do_destroy):
        scl = self.__stream_change_subscriber_list
        for sc in scl:
            try:
                sc.on_stream_destroy(si, do_destroy)
            except Exception, e:
                logging.exception("StreamManagerBase::__safe_notify_destroy find exception:%s", str(e))

    def __safe_notify_create(self, si, do_create, is_hd = False):
        scl = self.__stream_change_subscriber_list
        for sc in scl:
            try:
                sc.on_stream_create(si, do_create, is_hd)
            except Exception:
                logging.exception("StreamManagerBase::__safe_notify_create find exception")

    def subscribe_stream_change(self, sc):
        for s in self.__stream_change_subscriber_list:
            if s == sc:
                return
        self.__stream_change_subscriber_list.append(sc)
    
    def unsubscribe_stream_change(self, sc):
        self.__stream_change_subscriber_list.remove(sc)

    #   /               
    def is_master(self):
        return self.__is_master


    def __load_from_db(self):
        sinfo_map = {}
        try:
            all_si = lpersist.load_all_kv()
            for key in all_si:
                si = StreamInfo()
                si_d = all_si[key]
                if not si.from_dict(si_d):
                    logging.error("StreamManagerBase::__load_from_db can't parse %s for key %s",
                                  str(si_d), key)
                    continue
    
                sinfo_map[int(key)] = si

            if len(sinfo_map) <= 0:
                logging.warning("StreamManagerBase::__load_from_db Loading redis data is empty!")
        except:
            logging.error("StreamManagerBase::__load_from_db can't load from redis")
            raise
        return sinfo_map

    def reload_from_db(self, caller):
        logging.info("StreamManagerBase::reload_from_db caller:%s", str(caller))
        sinfo_map = {}
        try:
            sinfo_map = self.__load_from_db()
        except Exception as e:
            logging.exception("StreamManagerBase::reload_from_db find exception:%s", str(e))
            return
        
        #               
        cur_time = int(time.time())
        for stream_id in sinfo_map:
	    si = sinfo_map.get(stream_id)
            stream_id = int(stream_id)
            old_si = self.__stream_map.get(stream_id)
            if not old_si:#                                    
                si.update_time = cur_time
                self.__add2memory(si)
                self.__safe_notify_create(si, False)

            else:#                  
                old_si.local_update(si)
  
        #                           
        key_delta = set(self.__stream_map.keys()) - set(sinfo_map.keys())
        for key in key_delta:
            self.__completely_delete(key, False)

    #            redis      
    def handle_timeout(self):
        curr_time = int(time.time())
        self.check_master_slave()

        if (-1 == self.__sync_data_time_last) or (curr_time - self.__sync_data_time_last) >= 10:
            try:
                if self.__is_master and (-1 != self.__sync_data_time_last):
                    return
                self.reload_from_db('timer')
                self.__alias_stream_manager.reload_from_db('timer') #      alias   stream            
            except Exception as e:
                logging.exception("StreamManagerBase::handle_timeout find exception:%s", str(e))
            self.__sync_data_time_last = curr_time

        else:
            pass
        
        #check_json_state
        #self.__stream_map.check_state()

    #                     cdn receiver      
    def check_stream_timeout(self):
        global CHECK_STREAM_TIMEOUT_INT
        global DESTORY_DELAY_INTERVAL_INT
        global MAX_DESTORY_ALIAS_DELAY_INTERVAL_INT
        global NONE_P2P_DESTORY_DELAY_INTERVAL_INT
	global CHECK_STREAM_ALIAS_TIMEOUT_INT

        curr_time = int(time.time())
        if curr_time - self.__check_stream_time_last < CHECK_STREAM_TIMEOUT_INT:
            return

        for stream_id in self.__stream_map.keys():
            si = self.__stream_map.get(stream_id)
            
            if 1 == si.delete_flag:
                timeout_len = DESTORY_DELAY_INTERVAL_INT
                if si.p2p == 0:
                    timeout_len = NONE_P2P_DESTORY_DELAY_INTERVAL_INT

                if(curr_time - si.delete_start_time >= timeout_len):
                    logging.info('delay __completely_delete stream_id:%s alias:%s app_id:%s' ,str(stream_id), str(si.alias), str(si.app_id))
                    if si.delete_start_time < 0:
                       si.delete_start_time = curr_time
                       continue
                    self.__completely_delete(stream_id, True)

            elif (0 == si.delete_flag) and (curr_time - si.update_time >= DESTORY_DELAY_INTERVAL_INT):
                logging.info('upload timeout __remove_by_stream_id stream_id:%s, alias:%s, app_id:%s', str(stream_id), str(si.alias), str(si.app_id))
                self.__remove_by_stream_id(stream_id, False)
            else:
                pass


        self.__check_stream_time_last = curr_time

        #            24                  
        if curr_time - self.__check_stream_alias_time_last >= CHECK_STREAM_ALIAS_TIMEOUT_INT:
            self.__alias_stream_manager.check_timeout(MAX_DESTORY_ALIAS_DELAY_INTERVAL_INT)
	    self.__check_stream_alias_time_last = curr_time
       
    #                  /      
    def startup(self, reactor_svc, db_server_ip, db_server_port, db_server_idx):
       try:
           lpersist.init_persist(db_server_ip, db_server_port, db_server_idx)
           self.reload_from_db('startup')
           self.__alias_stream_manager.reload_from_db('startup')
           reactor_svc.register_timer(self)

       except Exception as e:
           logging.exception("StreamManagerBase::Startup find exception." + str(e))
           lpersist.fini_persist()
           raise
   
    def stop(self):
       try:
           lpersist.fini_persist()
       except Exception as e:
           logging.exception("StreamManagerBase::Stop find exception." + str(e))

    def flush_update_time_all(self, curr_time):
        self.__stream_map.flush_stream_update_time(curr_time)

        
#                  
class StreamManager(StreamManagerBase):
    """StreamManager class for managing the stream of life and stream state maintenance """
    def __init__(self, *args, **kwargs):
        self.__receiver_report_time_last = int(time.time())
        StreamManagerBase.__init__(self,*args, **kwargs)
        #return super(StreamManager, self).__init__(*args, **kwargs)

    #lapi                  
    def create_stream(self, create_req):
        si = StreamInfo()
        si.start_time               = timeval_t()
        si.stream_id                = create_req.stream_id
        si.update_time              = int(time.time())
        si.res                      = create_req.res
        si.app_id                   = int(create_req.app_id)
        si.rt                       = create_req.rt
        si.alias                    = create_req.alias
        si.nt                       = create_req.need_transcoding
        si.delete_flag              = 0
        si.net_stream_upsche_addr   = create_req.net_stream_upsche_addr
        si.net_stream_src_url       = create_req.net_stream_media_src
        si.upload_client_type       = create_req.upload_client_type
        si.net_stream_media_src_type     = create_req.net_stream_media_src_type
        si.upload_url_json_str      = ''
        si.play_list_json_str        = ''
        si.play_token               = make_pl_sche_token(create_req.stream_id, lctrl_conf.pl_sche_secret)
        si.p2p                      = create_req.p2p_flag
        create_req.play_token       = si.play_token

        return self.__create_stream_impl(create_req, si)

    def __create_stream_impl(self, create_req,  stream_info = StreamInfo()):
        upload_dict_old = {}
        download_dict_old = {}
        int_errocde_play_list_json_str = ''

        extend_para_dict = {"append_content":"&alias=" + str(create_req.alias) + "&app_id=" + str(create_req.app_id)}

        #make get_playlist
        (download_dict_old, stream_info.play_list_json_str, int_errocde_play_list_json_str) = make_get_playlist(create_req, extend_para_dict, 1)
        if download_dict_old == None or stream_info.play_list_json_str == None:
            return (False, None, None)

        if create_req.need_transcoding == 1:
            (download_dict_old_temp, stream_info.play_list_json_str_v2, int_errocde_play_list_json_str) = make_get_playlist(create_req, extend_para_dict, 2)
            if download_dict_old_temp == None or stream_info.play_list_json_str_v2 == None:
               return (False, None, None)
        else:
            stream_info.play_list_json_str_v2 = int_errocde_play_list_json_str

        #make get_upload_url
        (upload_dict_old, stream_info.upload_url_json_str) = make_get_upload_url(create_req, extend_para_dict)
        if upload_dict_old == None or stream_info.upload_url_json_str == None:
            return (False, None, None)  

        #save to redis db
        
        if not self._StreamManagerBase__save(stream_info):
            logging.error("StreamManager::__create_stream_impl __save failed! stream.%d",create_req.stream_id)
            return (False, None, None)

        self._StreamManagerBase__alias_stream_manager.add(stream_info.alias, stream_info.stream_id, stream_info.app_id, True)
        
        self._StreamManagerBase__safe_notify_create(stream_info, True, create_req.need_transcoding)

        return self.__make_create_result(create_req,  stream_info, upload_dict_old, download_dict_old)

    def __make_create_result(self, create_req,  stream_info, upload_dict_old, download_dict_old):
        json_download = {}
        if stream_info.alias != '':
            json_download["alias"] = create_req.alias
        else:
            json_download["stream_id"] = str(create_req.stream_id)
        json_download["download_list"] = []
 
        json_download["download_list"] = list(download_dict_old)
        json_dict = {}
        json_dict["cs_id"] =  str(create_req.stream_id)
        json_dict["upload"] = upload_dict_old
        json_dict["download"] = json_download
        ret_json = generate_json_ex(ECODE_SUCC, json_dict, str(create_req.potocol_ver))
        ext_params = {}
        ext_params['alias'] = create_req.alias
        try:
            #if alias != '':
            #    json_dict = None
            #else:
            ext_params['stream_id'] = str(create_req.stream_id)
            if create_req.potocol_ver == 2:
                return err_process(create_req.potocol_ver, ECODE_SUCC, True, ret_json, ext_params)

            if create_req.potocol_ver >= 4:
                json_dict = None
            ret_json_v3 = generate_json_for_create_stream(ECODE_SUCC, ext_params, json_dict)
            return err_process(create_req.potocol_ver, ECODE_SUCC, True, ret_json_v3, ext_params)
        except Exception as e:
            logging.info('StreamManager::__make_create_result exception:' + str(e))
        return (False, None, None)
    

    def destroy_stream(self, destroy_req):
	try:
            self._StreamManagerBase__remove(destroy_req)
            self._StreamManagerBase__alias_stream_manager.completely_delete(destroy_req.alias, destroy_req.app_id)
        except Exception as e:
            logging.info('StreamManager::get_upload_url exception:%s', str(e))
        return True

    def get_upload_url(self, app_id, stream_id, alias_str):
        try:
            si = self.get_stream_info(app_id, stream_id, alias_str)
            if si == None:
                return None
            return si.upload_url_json_str

        except Exception as e:
            logging.info('StreamManager::get_upload_url exception:%s', str(e))
        return None

    def get_alias_streamid_map(self):
        try:
            return self._StreamManagerBase__stream_map.get_alias_streamid_map_json_str()
        except Exception as e:
            logging.info('StreamManager::get_alias_streamid_map exception:%s', str(e))
        return ujson.encode({})
    
    def get_stream_list(self, app_id, protocol_ver):
        try:
            if protocol_ver == 1:
               return self._StreamManagerBase__stream_map.get_valid_stream_list_json_str(app_id, True)
            elif protocol_ver == 2:
               return self._StreamManagerBase__alias_stream_manager.get_alias_list(app_id)
            else:
                pass

        except Exception as e:
            logging.info('StreamManager::get_stream_list exception:%s', str(e))
        return ujson.encode({})

    def get_stream_stat(self):
        try:
            return self._StreamManagerBase__stream_map.get_valid_streamid_stats_json_str()
        except Exception as e:
            logging.info('StreamManager::get_stream_stat exception:%s', str(e))
        return ujson.encode({})

    def get_playlist(self, app_id, stream_id, alias_str, ver):
        try:
            si = self.get_stream_info(app_id, stream_id, alias_str)
            if si == None:
                return None
            if 1 == ver:
                return si.play_list_json_str
            else:
                return si.play_list_json_str_v2

        except Exception as e:
            logging.info('StreamManager::get_playlist exception:%s', str(e))
        return None


    def check_master_slave(self):
        global TRIGGER_SERVER_TIME_INTERVAL_INT
        curr_time = int(time.time())
        self._StreamManagerBase__is_master = (curr_time - self.__receiver_report_time_last <= TRIGGER_SERVER_TIME_INTERVAL_INT)
 

    def check_master_to_slave(self):
        global TRIGGER_SERVER_TIME_INTERVAL_INT
        curr_time = int(time.time())
        #      1                                          rcv_block_up_time         master/slave                     5                                 bug
        if curr_time - self.__receiver_report_time_last >= TRIGGER_SERVER_TIME_INTERVAL_INT:
            self.reload_from_db('check_master_to_slave')
            self.flush_update_time_all(curr_time)

        self.__receiver_report_time_last = curr_time

    def update_time_for_alias_stream_map(self, si, update_time):
        self._StreamManagerBase__alias_stream_manager.update_time(si.app_id, si.alias, si.stream_id, update_time)

    #cdn                  
    def receiver_keepalive(self, ip_str, port, outbound, inbound, server_stream_list):
        curr_time = int(time.time())
        self.check_master_to_slave()

        #               
        for ss in server_stream_list:
            self._StreamManagerBase__stream_map.flush_stream_state(ss.stream_id, curr_time, ss.block_seq, self.update_time_for_alias_stream_map)

        #               
        self.check_stream_timeout()
    

    def forward_keepalive(self):
        self.check_master_to_slave()

    def export_info_to_db(self, dst_db_ip, dst_db_port, dst_db_index):
        try:
            return self.__export_info_to_db(dst_db_ip, dst_db_port, dst_db_index)
        except Exception as e:
            logging.exception('StreamManager::__export_info_to_db exception:%s! dst_db_ip:%s, dst_db_port:%s dst_db_index:%s',
                    str(e), str(dst_db_ip), str(dst_db_port), str(dst_db_index))
        return False

    def __export_info_to_db(self, dst_db_ip, dst_db_port, dst_db_index):
        logging.info('StreamManager::export_info_to_db start ...! dst_db_ip:%s, dst_db_port:%s dst_db_index:%s',
                str(dst_db_ip), str(dst_db_port), str(dst_db_index))
        dbi = DatabaseInfo(dst_db_ip, dst_db_port, dst_db_index)
        export_obj = ExportToDb()
        if not export_obj.open(dbi):
            logging.error('StreamManager::export_info_to_db failed! dst_db_ip:%s, dst_db_port:%s dst_db_index:%s',
                    str(dst_db_ip), str(dst_db_port), str(dst_db_index))
            return False

        logging.info('StreamManager::export_info_to_db start export... dst_db_ip:%s, dst_db_port:%s dst_db_index:%s', 
                str(dst_db_ip), str(dst_db_port), str(dst_db_index))


        ret = export_obj.export(lpersist.get_stream_id_last(), 
                self._StreamManagerBase__stream_map.get_maps(), 
                self._StreamManagerBase__alias_stream_manager.get_alias_map())

        export_obj.close()
        export_obj = None

        logging.info('StreamManager::export_info_to_db %s!', 'successed!' if ret else 'failed!')

        return ret
