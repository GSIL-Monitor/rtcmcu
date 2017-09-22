�  import time
import sys

sys.path.append('../')
import lstream
import lctrl_conf
import lpersist

#db_opt = lpersist.mysql_db_t('10.10.69.198', 3306, 'root', 'happy', 'ddstream')
db_opt = lpersist.redis_db_t('127.0.0.1', 16379,
                             lctrl_conf.db_server_idx,
                             lpersist.HASH_TABLE_NAME)

for ri in lctrl_conf.reserve_room_id:
    room_id = ri
    stream_id = lctrl_conf.reserve_room_id[ri]

    si = lstream.stream_info_t()
    si.stream_id = stream_id
    si.byte_per_second = 38400
    si.start_time = int(time.time())
    si.update_time = int(time.time())
    si.site_user_id_str = str(room_id)
    si.user_id_str = str(room_id)
    si.room_id_str = str(room_id)

    key = lstream.make_stream_info_map_key(si.user_id_str,
                                           si.room_id_str)
    val_d = si.to_dict()

    db_opt.add_key_value(key, val_d)
