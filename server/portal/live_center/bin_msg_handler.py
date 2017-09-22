�  #coding:utf-8 
import reactor
import socket
import lutil
import struct
import logging
import time

from data_struct_defs import IOHandler
from stream_manager import * 
from streaminfo_pack import StreamInfoListPack, StreamInfoPack
from stream_change_notify import IStreamChangeNotify
from proto import *
from lutil_ex import *

MAX_TIMEOUT = 20 * 1000
MAX_PKG_SIZE = 10 * 1024 * 1024


class BinMsgHandler(IOHandler):
    """                                          CDN"""
    def __init__(self, reactor_svc, sock, addr, sm, cb_handler_die):
        self.cb_handler_die = cb_handler_die 
        self.sock = sock
        self.addr = addr
        self.reactor = reactor_svc
        self.reactor.add_fd(self.sock, self, reactor.IO_IN)

        self.rbuf = ""
        self.wbuf = ""
        self.active_tick = get_current_tick()
        self.sm = sm

        #self.send_white_list()


    def on_handler_die(self):
        #logging.info('BinMsgHandler::on_handler_die close connection:%s', str(self.addr))
        self.reactor.remove_fd(self.sock, self)
        self.sock.close()
        self.sock = None
        self.cb_handler_die(self)

    def send_pkg(self, pkg):
        if None == self.sock or len(pkg) <= 0:
            return
        if 0 == len(self.wbuf):
            self.reactor.set_fd_event(self.sock, self,
                                      reactor.IO_IN | reactor.IO_OUT)
        self.wbuf += pkg

    def handle_receiver_keepalive(self, pkg):
        #logging.debug("handle_receiver_keepalive in len:%d", len(pkg))
        ip_str = ''
        (port, outb, inb, scnt) = range(4)
        tmp_scnt = 0
        try:
            tmp_pkg = pkg[0:struct.calcsize(r2p_keepalive_pat)]
            (ip, port, outb, inb, scnt) = struct.unpack(r2p_keepalive_pat,
                                                        tmp_pkg)
            tmp_scnt = scnt
            ip_str = lutil.ip2str(ip)
            pkg = pkg[struct.calcsize(r2p_keepalive_pat):]
            curr_time = time.time()
            ss_list = []
            while scnt > 0:
                scnt -= 1
                tmp_pkg = pkg[0:struct.calcsize(receiver_stream_status_pat)]
                (sid, fcnt, kts, bseq) = struct.unpack(receiver_stream_status_pat,
                                                       tmp_pkg)
                pkg = pkg[struct.calcsize(receiver_stream_status_pat):]
                ss = ServerStreamInfo()
                ss.stream_id = sid
                ss.mark_time = int(curr_time)
                ss.block_seq = bseq
                ss_list.append(ss)

        except IndexError as e:
            logging.exception("handle_receiver_keepalive find exception:" + str(e))
            return

        except struct.error as e:
            logging.exception("handle_receiver_keepalive find exception:" + str(e))
            return

        #for sid_tmp in ss_list:
        #    logging.debug('handle_receiver_keepalive scnt:%s sid_tmp:%s', str(tmp_scnt), str(sid_tmp.stream_id)) 

        self.sm.receiver_keepalive(ip_str, port, outb, inb, ss_list)
	self.send_white_list()


    def handle_forward_keepalive(self, pkg):
        #logging.debug("handle_forward_keepalive in len:%d", len(pkg))
        self.sm.forward_keepalive()
	self.send_white_list()

    def send_white_list(self):
        try:
           pkg_v2 = gen_stream_list_pkg_v3(self.sm)
           if len(pkg_v2) > 0:
               self.send_pkg(pkg_v2)
        except Exception as e:
            logging.exception("send_white_list find exception:" + str(e))


    def handle_pkg(self, pkg):
        try:
            #magic, ver, cmd, size
            head_size = struct.calcsize(comm_head_pat)
            tmp_pkg = pkg[0:head_size]
            (_, _, cmd, _) = struct.unpack(comm_head_pat, tmp_pkg)

            if f2p_keepalive_cmd == cmd:
                self.handle_forward_keepalive(pkg[head_size:])

            elif r2p_keepalive_cmd == cmd:
                self.handle_receiver_keepalive(pkg[head_size:])

            elif f2p_white_list_req == cmd:
                self.send_white_list()

            else:
                logging.info("BinMsgHandler::handle_pkg unknown pkg cmd %d.", cmd)

        except IndexError as e:
            logging.exception("BinMsgHandler::handle_pkg  find IndexError:" + str(e))

        except struct.error as e:
            logging.exception("BinMsgHandler::handle_pkg  find struct.error:"+ str(e))

        except Exception as e:
            logging.exception("BinMsgHandler::handle_pkg  find Exception:"+ str(e))

    def handle_io(self, evt):
        self.active_tick = get_current_tick()
        if evt & reactor.IO_IN:
            (ecode, tmp) = lutil.safe_recv(self.sock, 4 * 1024, True)
            if 0 != ecode:
                #logging.info('BinMsgHandler::handle_io IO_IN error:%s addr:%s rbuf:%d', str(ecode), str(self.addr), len(self.rbuf))
                self.on_handler_die()
                return

            self.rbuf += tmp
            while None != self.sock:
                pkg_len = parse_pkg_len(self.rbuf)
                if -1 == pkg_len:
                    return
                if (pkg_len < struct.calcsize(comm_head_pat) or pkg_len >= MAX_PKG_SIZE):
                    logging.warning("BinMsgHandler::handle_pkg IO_IN  pkg too big, pkg_len: %d addr:%s", pkg_len, str(self.addr))
                    self.on_handler_die()
                    return
                elif len(self.rbuf) >= pkg_len:
                    pkg = self.rbuf[0:pkg_len]
                    self.rbuf = self.rbuf[pkg_len:]
                    self.handle_pkg(pkg)
                else:
                    break
        elif evt & reactor.IO_OUT:
            (ecode, num) = lutil.safe_send(self.sock, self.wbuf)
            if 0 != ecode:
                #logging.debug("BinMsgHandler::handle_pkg  IO_OUT find conn error.code:%d addr:%s", ecode, str(self.addr))
                self.on_handler_die()
                return
            self.wbuf = self.wbuf[num:]
            if 0 == len(self.wbuf):
                self.reactor.set_fd_event(self.sock, self, reactor.IO_IN)
        else:
            self.on_handler_die()

