#coding:utf-8
import logging
import time
import ujson
from alias_stream_map import *
import lpersist
from lutil_ex import *

class AliasStreamManager():
    def __init__(self):
        self.__app_alias_map = {} #hash_map<app_id, AliasStreamMap>

    def __str__(self):
        str_info = ''
        for app_id in self.__app_alias_map:
	    asm_obj = self.__app_alias_map.get(app_id)
            if len(str_info) > 0:
                str_info += ';'
            str_info += str(asm_obj)
        return str_info


    def get_alias_map(self):
        try:
            return self.__get_alias_map()
        except Exception as e:
            logging.exception('__get_alias_map failed! exception:%s', str(e))
        return None

    def __get_alias_map(self):
        ret_dict = {}
        for app_id in self.__app_alias_map:
	    asm_map = self.__app_alias_map.get(app_id).get_maps()
            for alias in asm_map:
		asv =  asm_map.get(alias)
                ret_dict[pack_key(app_id, alias)] = asv.to_dict()
        return ret_dict

    def get_stream_id(self, app_id, alias):
	return self.get_alias_obj(app_id, alias).stream_id

    def get_alias_obj(self, app_id, alias):
        if alias == None or alias == '' or app_id == 0 or app_id == None:
            return None
        app_obj = self.__app_alias_map.get(app_id, None)
        if app_obj == None:
            logging.warning('get_alias_obj failed! app_obj = None, app_id(%d), alias(%s)', app_id, alias)
            return None
        return app_obj.get(alias)

    def get_app_obj(self, app_id):
        if app_id == 0 or app_id == None:
            #logging.debug('get_app_obj failed! invalid param, app_id(%d)', app_id)
            return None
        return self.__app_alias_map.get(app_id, None)

    def update_time(self, app_id, alias, stream_id, update_time):
        alias_map = self.get_app_obj(app_id)
        if alias_map == None:
            return False

        return alias_map.update(alias, stream_id, update_time)


    def add_ex(self, asv, is_add_to_db = False):#AliasStreamValue
        if not isinstance(asv, AliasStreamValue):
            logging.warning('add_ex failed! invalid param asv(%s)', str(asv))
            return False
        app_obj = self.__app_alias_map.get(asv.app_id, None)
        if app_obj == None:
            app_obj = AliasStreamMap()
            self.__app_alias_map[asv.app_id] = app_obj

        if is_add_to_db:
            self.add_to_db_ex(asv)
        return app_obj.add_ex(asv)
        
    def add(self, alias, stream_id, app_id, is_add_to_db = False):
        try:
            return self.add_none_safe(alias, stream_id, app_id, is_add_to_db)
        except Exception as e:
            logging.exception('add failed! exception:(%s)', str(e))
        return False

    def add_none_safe(self, alias, stream_id, app_id, is_add_to_db = False):
        if alias == None or alias == '' or \
                stream_id == 0 or stream_id == None or \
                app_id == 0 or app_id == None:
                    logging.warning("AppAliasStreamMap::add alias(%s), stream_id(%s) app_id(%s)", 
                            str(alias), str(stream_id), str(app_id))
                    return False
        app_obj = self.__app_alias_map.get(app_id, None)
        if app_obj == None:
            app_obj = AliasStreamMap()
            self.__app_alias_map[app_id] = app_obj

        asv = app_obj.add(alias, stream_id, app_id)

        if (asv != None) and (is_add_to_db == True):
            self.add_to_db_ex(asv)

        return asv != None

    def delete_bat(self, keys):
        for key in keys:
           self.delete_ex(key)
        return True

    def delete_ex(self, key_str):
        ret = unpack_key(key_str)
        if not ret[0]:
           logging.warning('delete_ex failed! unpack_key return False , key_str(%s)', str(key_str))
           return False
        return self.delete(ret[2], int(ret[1]))

    def completely_delete(self, alias, app_id):
        try:
	   if alias == None or alias == '' or app_id == 0 or app_id == None:
	       return
           self.delete(alias, app_id)
           self.detele_ex_from_db(alias, app_id)
        except Exception as e:
           logging.exception('completely_delete find exception:%s', str(e))

       
    def delete(self, alias, app_id):
        if alias == None or alias == '' or \
                app_id == 0 or app_id == None:
                    logging.warning("AppAliasStreamMap::delete alias(%s), app_id(%s)",
                             str(alias), str(app_id))
                    return False
        app_obj = self.__app_alias_map.get(app_id, None)
        if app_obj == None:
            return True

        app_obj.delete(alias)

        if len(app_obj.keys()) <= 0:
            del self.__app_alias_map[app_id]

        return True

    #               
    def add_to_db_ex(self, asv):
        if not isinstance(asv, AliasStreamValue):
            logging.warning('add_to_db_ex failed! invalid params, asv(%s)', str(asv))
            return False
        return self.add_to_db(pack_key(asv.app_id, asv.alias), asv.to_dict())


    def add_to_db(self, key_str, val_d):
        if key_str == None or key_str == '' or val_d == None or val_d == '':
            logging.warning('add_to_db failed! invalid params, key_str(%s) val_d(%s)', str(key_str), str(val_d))
            return False
        if not lpersist.add_alias_stream_info(key_str, val_d):
            logging.warning('add_to_db faild! add_alias_stream_info return False key_str(%s) val_d(%s)', str(key_str), str(val_d))
        return True

    def detele_from_db(self, key_str):
        if key_str == None or key_str == '':
            logging.warning('detele_from_db failed! invalid params, key_str(%s)', str(key_str))
            return False
        lpersist.del_alias_stream_info(key_str)

        return True

    def detele_ex_from_db(self, alias, app_id):
        return self.detele_from_db(pack_key(app_id, alias))


    def __load_from_db(self):
        app_alias_stream_map = {}
        try:
            all_as = lpersist.load_all_alias_stream_info()
            for key in all_as:
		as_d = all_as.get(key)
                as_obj = AliasStreamValue()
                if not as_obj.from_dict(as_d):
                    logging.error("__load_from_db alias_stream_map can't parse %s for key %s",
                                  str(as_d), key)
                    continue
    
                app_alias_stream_map[str(key)] = as_obj

            if len(app_alias_stream_map) <= 0:
                logging.warning("__load_from_db alias_stream_map Loading redis data is empty!")
        except:
            logging.error("__load_from_db can't load alias_stream_map from redis")
            raise
        return app_alias_stream_map

    def reload_from_db(self, caller):
        logging.info("reload_from_db caller:%s", str(caller))
        as_map = {}
        try:
            as_map = self.__load_from_db()
        except Exception as e:
            logging.exception("reload_from_db find exception:%s", str(e))
            return
        
        #               
        cur_time = int(time.time())
        for appid_alias in as_map:
	    as_obj = as_map.get(appid_alias)
            as_obj.last_update_time = cur_time
            self.add_ex(as_obj)
  
        #                           
        key_delta = set(self.get_alias_stream_keys()) - set(as_map.keys())
        self.delete_bat(key_delta)


    def check_timeout(self, timeout_len):
        try:
            self.check_timeout_none_safe(timeout_len)
        except Exception as e:
            logging.exception("AppAliasStreamMap::check_timeout find exception:%s", str(e))

    def check_timeout_none_safe(self, timeout_len):
        cur_time = int(time.time())
        for app_id in self.__app_alias_map.keys():
            app_obj = self.__app_alias_map.get(app_id)
            app_obj.check_timeout(cur_time, timeout_len, self.detele_ex_from_db)
            if len(app_obj.keys()) <= 0:
	        logging.info('check_timeout_none_safe len == 0 app_id(%s)', str(app_id))
                del self.__app_alias_map[app_id]

    def get_alias_stream_keys(self):
        as_keys = []
        for app_id in self.__app_alias_map:
	    app_obj = self.__app_alias_map.get(app_id).get_maps()
            for alias in app_obj:
		asv = app_obj.get(alias)
                as_keys.append(pack_key(asv.app_id, asv.alias))
        return as_keys


    def get_alias_list(self, app_id):
        stream_id_array = []
        app_obj = self.__app_alias_map.get(app_id, None)
        if app_obj != None:
            stream_id_array = app_obj.get_alias_list(int(time.time()))
        ret_dict = {}
        ret_dict["error_code"] = 0
        ret_dict['stream_id_list'] = stream_id_array
        return ujson.encode(ret_dict) 
