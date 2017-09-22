#coding:utf-8 
import os
import logging
from report_log_stats import *
from access_log import *

import lctrl_conf

class MyUDPLogger(logging.handlers.DatagramHandler):
    log_mode = 'FILE'
    def emit(self, record):
        try:
            if MyUDPLogger.log_mode == 'FILE':
                return
            msg = self.format(record)
            if len(msg) > 1400:
                msg = msg[0:1400]
            self.send(msg + "\n")
        except Exception as e:
            print str(record + str(e))
            self.handleError(record)

class LogHandler(object):
    """description of class"""

    def __init__(self, **kwargs):
        self.log_server_addr = ''
        self.udp_handler = None
        self.app_name = kwargs.get('app_name',['log_handler'])
        
        self.log_level_dict = {'DEBUG': logging.DEBUG,
                          'INFO': logging.INFO,
                          'ERROR': logging.ERROR,
                          'WARNNING': logging.WARNING}

        self.log_server_addr = kwargs.get('log_server_addr',['10.106.20.22:2111'])
        self.set_log(kwargs.get('log_level_name',['DEBUG']), kwargs.get('log_mode',['NET_FILE']))
        self.log_path = kwargs.get('store_path',['/opt/logs/'])
        self.__open_log(self.gen_log_file(), kwargs.get('local_addr',['']))

        #            Access      
        self.access_log = AccessLog(self.log_path, self.app_name)

        #      log               
        self.report = ReportLogStat(kwargs.get('local_addr',['']),
                                    kwargs.get('reporter_pipe',['/tmp/rpt.pip']))

        logging.info('LogHandler::init end! log_mode:%s log_level_name:%s log_server_addr:%s', 
                MyUDPLogger.log_mode, self.log_level_name, str(self.log_server_addr))

	#self.access_log.startup()


    def get_report_obj(self):
        return self.report

    def write_access_log(self, first_line, client_addr):
        self.access_log.add_v3(first_line, client_addr)

    def set_log(self, log_level_name, log_mode):
        self.log_level_name = str(log_level_name)
        self.log_mode = log_mode
        MyUDPLogger.log_mode = self.log_mode
        logging.getLogger().setLevel(self.log_level_dict.get(self.log_level_name, logging.INFO))

    def get_abs_path(self):
        return os.path.dirname(os.path.abspath(__file__))

    def get_base_name(self):
        return os.path.basename(sys.argv[0]).split('.')[0]

    def gen_log_path(self, log_path):
        if not os.path.exists(log_path):
            os.makedirs(log_path, 0755)
        return log_path

    def gen_out_file(self, abs_path, filename):
        return os.path.join(self.gen_log_path(abs_path), filename)

    def gen_log_file(self):
        return os.path.join(self.gen_log_path(self.log_path), "%s.log" % (self.get_base_name()))

    def __open_log(self, log_file, public_addr):
        logging.info('LogHandler::__open_log, log_file(%s) public_addr(%s), loglevel:%s', str(log_file), str(public_addr), 
                str(self.log_level_dict.get(self.log_level_name, logging.INFO)))
        fmt_str = '%(asctime)s %(levelname)-8s(%(filename)s:%(lineno)d)%(message)s'
        logging.basicConfig(format=fmt_str, filename='/dev/null')

        root = logging.getLogger()
        root.setLevel(self.log_level_dict.get(self.log_level_name, logging.INFO))

        new_h = logging.handlers.TimedRotatingFileHandler(log_file, 'midnight')
        fmt = logging.Formatter(fmt_str)
        new_h.setFormatter(fmt)
        root.addHandler(new_h)

        self.udp_handler = MyUDPLogger(self.log_server_addr[0], self.log_server_addr[1])
        fmt_str = public_addr + "\tLOG\t"+ self.app_name + "\t%(asctime)s\t%(levelname)s\t%(filename)s:%(lineno)d\t%(message)s"
        fmt = logging.Formatter(fmt_str)
        self.udp_handler.setFormatter(fmt)
        root.addHandler(self.udp_handler)
        logging.info('LogHandler::__open_log end! fmt_str:%s', fmt_str)



