#coding:utf-8 
import time
import hashlib
import sys

class TokenHelper():
    """token                  """
    def __init__(self):
        pass

    @staticmethod
    def make_token(curr_time, stream_id, para1_str, para2_str, secret_key):
        curr_time_str = "%08x" % (int(curr_time) & 0xFFFFFFFF)
        stream_id_str = "%u" % (int(stream_id) & 0xFFFFFFFF)
        if len(para1_str) > 128:
            para1_str = para1_str[0:128]
        
        if len(para2_str) > 128:
            para2_str = para2_str[0:128]
        
        if len(secret_key) > 32:
            secret_key = secret_key[0:32]
        
        mstr = curr_time_str + stream_id_str + secret_key + para1_str + para2_str
        m = hashlib.md5()
        m.update(mstr)
        md5_str = m.hexdigest()
        return curr_time_str + md5_str[8:]

    @staticmethod
    def check_token(curr_time, stream_id, para1_str, para2_str, secret_key,
                    max_timeout, token):
        curr_time = int(curr_time)
        if len(token) != 32:
            return False
    
        time_val = 0
        try:
            time_val = int(token[0:8], 16)
            if abs(time_val - curr_time) > max_timeout:
                return False
        except:
            return False
    
        real_token = make_token(time_val, stream_id, para1_str, para2_str,
                                secret_key)
        return real_token == token
