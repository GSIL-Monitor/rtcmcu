#coding:utf-8 
import logging
import ujson
from stream_info import *
from json_data_manager import *
from stream_count import *

'''
note:stream_id & app_id type is int
'''
class StreamMap():
    def __init__(self, *args, **kwargs):
        self.__app_info_stat_map = {}
        self.__stream_info_map = {}
        self.__is_already_changed = False
        self.__kwargs = kwargs
        self.__args = args
	self.__stream_count = StreamCount() 

        self.__json_data_manager = None
        self.init_json_data_manager()

        self.update_cache()

    #(stream_id)      
    def __call__(self,stream_id):
        return self.get(stream_id)

    def keys(self):
        return self.__stream_info_map.keys()

    def items(self):
        return self.__stream_info_map.items()

    def get_maps(self):
        return self.__stream_info_map

    def get_app_stream_cnt(self, app_id):
	return self.__stream_count.count(app_id)

    def clear(self):
        self.__stream_info_map.clear()
        self.update_cache()

    def get(self, stream_id):
        if not self.__stream_info_map.has_key(stream_id):
            return None
        return self.__stream_info_map[stream_id]

    def get_by_alias(self, app_id, alias, is_valid = True):
        if alias == None or alias == '' or app_id == None or app_id == '0':
            return None

        for stream_id in self.__stream_info_map:
	    si = self.__stream_info_map.get(stream_id)
            if si.app_id == app_id and si.alias == alias:
                if is_valid and si.delete_flag == 0:
                    return si
                elif not is_valid:
                    return si
                else:
                    pass

        return None

    def get_stream_id_by_alias(self, app_id, alias):
        si = self.get_by_alias(app_id, alias)
        if si != None:
            return si.stream_id
        return 0

    def add(self, stream_id, si = StreamInfo()):
        if si == None or stream_id == None or stream_id == 0:
            logging.error('StreamMap::add stream_id error, stream_id:%s',str(stream_id))
            return False

        if si.app_id == '' or si.app_id == 0 or si.app_id == None:
            logging.error('StreamMap::add app_id error, app_id:%s',str(si.app_id))
            return False

        if self.__stream_info_map.has_key(stream_id):
            logging.error('StreamMap::add already existed stream_id:%s',str(stream_id))
            return False
        self.__stream_info_map[stream_id] = si
	self.__stream_count.add(si.app_id, stream_id, si.nt)

        self.update_cache()
        return True

    def remove_by_stream_id(self, stream_id):
        if stream_id == None or stream_id == 0:
            return False
        if self.__stream_info_map.has_key(stream_id):
            si = self.__stream_info_map.get(stream_id)
	    self.__stream_count.remove(si.app_id, stream_id)

            del self.__stream_info_map[stream_id]

            self.update_cache()
            return True
        return False

    def remove_by_stream_id_v2(self, stream_id, is_delay = False, cbProc = None):
	si = self.__stream_info_map[stream_id]

        if True == is_delay:
            si.delete_flag = 1
            si.delete_start_time = int(time.time())
            cbProc(si)
            #logging.info('StreamMap::remove_by_stream_id_v2, stream_id:%s', str(stream_id))

        if False == is_delay:
	    self.__stream_count.remove(si.app_id, stream_id)
            del self.__stream_info_map[stream_id]

        self.update_cache()

        return True
 
    def remove_delay(self, stream_id, delete_flag = 1):
        if stream_id == None or stream_id == 0:
            return False

        if self.__stream_info_map.has_key(stream_id):
            si = self.__stream_info_map[stream_id];
            si.delete_flag = delete_flag
            si.delete_start_time = int(time.time())
	    self.__stream_count.remove(si.app_id, stream_id)
            self.update_cache()
            return True
        return True

    def update_cache(self):
        logging.debug('update_cache change...')
        self.__is_already_changed = True
        self.__json_data_manager.set_flag()

    def reset_stream_list_change_state(self):
        self.__is_already_changed = False

    def get_tream_list_change_state(self):
        return self.__is_already_changed

    def flush_stream_update_time(self, cur_time):
        for stream_id in self.__stream_info_map:
	    si_temp = self.__stream_info_map.get(stream_id)
            si_temp.update_time = cur_time
            logging.debug('flush_stream_update_time stream_id:%s si_temp.update_time:%s', str(si_temp.stream_id), str(si_temp.update_time))

    def flush_stream_state(self, stream_id, cur_time, block_seq, call_pfn):
        if not self.__stream_info_map.has_key(stream_id):
            return False
        si = self.__stream_info_map[stream_id];
        if block_seq > si.block_seq:
            si.update_time = cur_time
            si.block_seq = block_seq
            call_pfn(si, cur_time)
        else:
            pass
        return True


    def init_json_data_manager(self):
        self.__json_data_manager = JsonDataManager()
        self.__json_data_manager.add('alias_streamid_map', self.__encode_alias_streamid_map_json)
        self.__json_data_manager.add('all_stream_json', self.__encode_all_stream_json)
        self.__json_data_manager.add('all_stream_valid_json', self.__encode_all_stream_valid_json)
        self.__json_data_manager.add('valid_streamid_stats_json', self.__encode_valid_streamid_stats_json)


    def fini_json_data_manager(self):
        self.__json_data_manager.clear()
        self.__json_data_manager = None
   
    def check_state(self):
        self.__json_data_manager.check()
 
    def __encode_all_stream_json(self):
        return self.__encode_stream_json(None, False, False)

    def __encode_all_stream_valid_json(self):
        return self.__encode_stream_json(None, True, False)

    def __encode_valid_streamid_stats_json(self):
        return self.__encode_stream_stat_info_json(True)

    def __encode_alias_streamid_map_json(self):
        return self.__encode_stream_json(None, True, True, 'alias_streamid_list', True)

    def get_all_stream_json_str(self):
        return self.__json_data_manager.get('all_stream_json')

    def get_all_stream_valid_json_str(self):
        return self.__json_data_manager.get('all_stream_valid_json')

    def get_alias_streamid_map_json_str(self):
        return self.__json_data_manager.get('alias_streamid_map')

    def get_valid_stream_list_json_str(self, app_id, by_alias = False):
        return self.__encode_valid_stream_list_json(app_id, by_alias)

    def get_valid_streamid_stats_json_str(self):
        return self.__json_data_manager.get('valid_streamid_stats_json')

    def __encode_valid_stream_list_json(self, app_id, by_alias = False):
        return self.__encode_stream_json(app_id, True, False)

    def __encode_stream_json(self, app_id = None, is_valid = True, is_min = True, list_name = 'stream_id_list', is_must_alias = False):
        stream_id_array = []
        cur_time = int(time.time())

        for stream_id in self.__stream_info_map:
	    si_temp = self.__stream_info_map.get(stream_id)
            if ((True == is_valid) and 1 == si_temp.delete_flag) or (app_id != None and app_id != si_temp.app_id):
                continue

            if is_must_alias and si_temp.alias == '':
                continue


            temp_dict = {
                    'stream_id': str(si_temp.stream_id),
                    'alias': str(si_temp.alias)
                    }
            if True == is_min:
                 temp_dict['app_id'] = str(si_temp.app_id) 
            else:
                temp_dict['last_update_time'] = si_temp.update_time
                if False == is_valid:
                    temp_dict['app_id'] = str(si_temp.app_id)
                    temp_dict['delete_flag'] = str(si_temp.delete_flag)
                    temp_dict['upload_type'] = str(si_temp.upload_client_type)
                    temp_dict['time_dif'] = (cur_time - si_temp.update_time)
                    temp_dict['delete_start_time'] = si_temp.delete_start_time
                    temp_dict['create_time'] = si_temp.start_time.tv_sec
                    temp_dict['nt'] = si_temp.nt

            stream_id_array.append(temp_dict)

        ret_dict = {}
        ret_dict["error_code"] = "0"
        ret_dict[list_name] = stream_id_array
        return ujson.encode(ret_dict)


    def __encode_stream_stat_info_json(self,  is_valid = True):
        try:
            return self. __encode_stream_stat_info_json_none_safe(is_valid)
        except Exception as e:
            logging.warning('__encode_stream_stat_info_json Exception:%s', str(e))

    def __encode_stream_stat_info_json_none_safe(self,  is_valid = True):

        stream_info_stat_result_map = {}#{{},{},{},{}}
        
        total_count = 0
        for stream_id in self.__stream_info_map:
	    si_temp = self.__stream_info_map.get(stream_id)
            if ((True == is_valid) and 1 == si_temp.delete_flag):
                continue

            sisr = stream_info_stat_result_map.get(si_temp.app_id)
            if sisr == None:
                sisr = {}
                stream_info_stat_result_map[si_temp.app_id] = sisr

            total_count += 1
            cnt = 0
            if sisr.has_key(si_temp.upload_client_type):
                cnt = sisr.get(si_temp.upload_client_type)
            sisr[si_temp.upload_client_type] = cnt + 1          
        
        stat_result = []
        self.__app_info_stat_map.clear()
        for app_id in stream_info_stat_result_map:
	    stat_data = stream_info_stat_result_map.get(app_id)
            stat_data['app_stream_count'] = self.__stat_steam_count_for_app(stat_data)
            self.__app_info_stat_map[app_id] = stat_data['app_stream_count'] #      appid                
            stat_data['app_id'] = str(app_id)
            stat_result.append(stat_data)

        ret_dict = {}
        ret_dict["error_code"] = "0"
        ret_dict["total_stream_count"] = total_count
        ret_dict["stat_result"] = stat_result
        return ujson.encode(ret_dict)

    def __stat_steam_count_for_app(self, item_map):
        ret_val = 0
        if item_map == None:
            return ret_val
        for key in item_map:
	    val = item_map.get(key)
            ret_val += int(val)

        return ret_val

    def get_stream_cnt(self, app_id):
        if self.__app_info_stat_map.has_key(app_id):
            return self.__app_info_stat_map.get(app_id)
        return 0
