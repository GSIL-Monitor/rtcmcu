#coding:utf-8
from stream_id_helper import *

UNKNOWN_BLOCK_SEQ = -1
DESTORY_DELAY_INTERVAL_INT = 5*60 #P2P               seconds
NONE_P2P_DESTORY_DELAY_INTERVAL_INT = 30 #   P2P               seconds
TOKEN_VALID_TIME_LEN_INT = 5*60 #seconds
MAX_DESTORY_ALIAS_DELAY_INTERVAL_INT = 12*60*60 #seconds
CHECK_DESTORY_DELAY_INTERVAL_INT = 60 #seconds
CHECK_STREAM_TIMEOUT_INT = 10 #seconds
CHECK_STREAM_ALIAS_TIMEOUT_INT = 10*60 #seconds
TRIGGER_SERVER_TIME_INTERVAL_INT = 60 #seconds

MAX_TIMEOUT = 1000 * 10
REQ_TIMEOUT = 1000 * 3
DELAY_SEND_RESPONSE_INTERVAL_INT = 1000 #1 milliseconds

HTTP_MSG = {}
HTTP_MSG[200] = "OK"
HTTP_MSG[500] = "Internal Server Error"
HTTP_MSG[405] = "Method Not Allowed"

ECODE_MIN = 20006
ECODE_MAX = 29999
ECODE_SUCC = 0
ECODE_FAIL = 1
ECODE_INVALID_PARA = 2
ECODE_NOT_EXIST = 3
ECODE_SERVER_INNER_ERROR = 4
ECODE_TOKEN_ERROR = 5

ECODE_STREAM_COUNT_MAX = ECODE_MIN
ECODE_TRANS_COUNT_MAX  = ECODE_MIN + 1

VIDEO_RT = {}
VIDEO_RT[DefiType.ORGIN] = "1300"
VIDEO_RT[DefiType.HD] = "1300"
VIDEO_RT[DefiType.SD]  = "800"
VIDEO_RT[DefiType.SMOOTH]  = "400"

AUDIO_RT = {}
AUDIO_RT[DefiType.ORGIN]  = "60"

VIDEO_RES = {}
VIDEO_RES[DefiType.SMOOTH] = "672x378"
VIDEO_RES[DefiType.SD]     = "960x540"
VIDEO_RES[DefiType.HD]     = "1280x720"

DEFAULT_EXT_PARAM_DICT = {"append_content":""}

EXPORT_DATA_TOKEN = '98765'
