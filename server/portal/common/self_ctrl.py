#coding:utf-8
import os
import sys
import signal
import socket
import atexit
import reactor
import lutil
from data_struct_defs import * 


class SelfCtrl(IOHandler):
    """            """
    def __init__(self, abs_path, base_name, load_log_callback, default_cfg_name):
        self.abs_path = abs_path
        self.base_name = base_name
        self.sock = None
        self.safe_quit = False
        self.default_cfg_name = default_cfg_name
        self.load_log_callback = load_log_callback

    def gen_pid_file(self):
        return os.path.join(self.abs_path,  self.base_name + '.pid')

    def del_sock_file(self):
        try:
            os.remove(self.gen_sock_file())
        except OSError:
            pass

    def gen_sock_file(self):
        return os.path.join(self.abs_path, self.base_name + '.sock')

    def gen_out_file(self, file_path, filename):
        log_path = self.gen_log_path(file_path)
        return os.path.join(log_path, filename)

    def gen_log_file(self, file_path):
        log_path = self.gen_log_path(file_path)
        return os.path.join(log_path,
                            "%s.log" % (self.base_name))

    def gen_log_path(self, log_path):
        if not os.path.exists(log_path):
            os.makedirs(log_path, 0755)
        return log_path

    def handle_io(self, evt):
        if evt & reactor.IO_IN:
            (ecode, pkg) = lutil.safe_recv(self.sock, 1024)
            if 0 == ecode:
                self.dispatch_cmd(pkg)
        else:
            logging.warning("SelfCtrl::handle_io unknown event %d", evt)

    def create_local_socket(self):
        self.del_sock_file()
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM, 0)
        self.sock.bind(self.gen_sock_file())
        atexit.register(self.del_sock_file)
        self.rsvc.add_fd(self.sock, self, reactor.IO_IN)

    def send_cmd(self, cmd):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM, 0)
        sock_file = self.gen_sock_file()
        sock.sendto(cmd, 0, sock_file)

    def dispatch_cmd(self, pkg):
        pkg = pkg.strip()
        if "safe_quit" == pkg:
            self.safe_quit = True
            logging.info("SelfCtrl::dispatch_cmd trigger safe_quit")
            self.hsvc.stop()
        elif 'reload_conf' == pkg:
            self.load_conf()
        else:
            logging.info("SelfCtrl unknown cmd %s", str(pkg))

    def load_conf(self):
        conf_file_name = self.default_cfg_name 
        argc = len(sys.argv)
        if argc > 2:
            conf_file_name = sys.argv[2]
        conf_file = os.path.join(self.abs_path, conf_file_name)
        self.load_log_callback(conf_file)


