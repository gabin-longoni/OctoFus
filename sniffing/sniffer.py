#!/usr/bin/env python3

import os
import sys
import socket
import threading
from select import select
import errno
import logging

from scapy.all import plist, conf, Raw, IP, PcapReader
from scapy.data import ETH_P_ALL, MTU
from scapy.consts import WINDOWS

from sniffing.data.binrw import Buffer
from sniffing.data.msg import Msg
from sniffing.packet_parser import parse_packet

logger = logging.getLogger("OctoFus-Sniffer")

if os.name == "posix" and sys.platform == "darwin":
    import ctypes.macholib.dyld
    ctypes.macholib.dyld.DEFAULT_LIBRARY_FALLBACK.insert(0, "/opt/local/lib")

def sniff(
    store=False,
    prn=None,
    lfilter=None,
    stop_event=None,
    refresh=0.1,
    offline=None,
    *args,
    **kwargs
):
    logger.debug("Setting up sniffer...")
    if offline is None:
        L2socket = conf.L2listen
        s = L2socket(type=ETH_P_ALL, *args, **kwargs)
    else:
        s = PcapReader(offline)

    if WINDOWS:
        from scapy.arch.pcapdnet import PcapTimeoutElapsed
        read_allowed_exceptions = (PcapTimeoutElapsed,)

        def _select(sockets):
            return sockets
    else:
        read_allowed_exceptions = ()

        def _select(sockets):
            try:
                return select(sockets, [], [], refresh)[0]
            except OSError as exc:
                if exc.errno == errno.EINTR:
                    return []
                raise

    lst = []
    try:
        logger.debug("Started Sniffing")
        while True:
            if stop_event and stop_event.is_set():
                break
            sel = _select([s])
            if s in sel:
                try:
                    p = s.recv(MTU)
                except read_allowed_exceptions:
                    continue
                if p is None:
                    break
                if lfilter and not lfilter(p):
                    continue
                if store:
                    lst.append(p)
                if prn:
                    r = prn(p)
                    if r is not None:
                        print(r)
    except KeyboardInterrupt:
        pass
    finally:
        logger.debug("Stopped sniffing.")
        s.close()

    return plist.PacketList(lst, "Sniffed")

def raw(pa):
    return pa.getlayer(Raw).load

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP

LOCAL_IP = get_local_ip()

def from_client(pa):
    logger.debug("Determining packet origin...")
    dst = pa.getlayer(IP).dst
    src = pa.getlayer(IP).src
    if src == LOCAL_IP:
        logger.debug("Packet comes from local machine")
        return True
    elif dst == LOCAL_IP:
        logger.debug("Packet comes from server")
        return False
    logger.error(
        "Packet origin unknown\nsrc: %s\ndst: %s\nLOCAL_IP: %s", src, dst, LOCAL_IP
    )
    assert False, "Packet origin unknown"

buf1 = Buffer()
buf2 = Buffer()

def on_receive(pa, action):
    logger.debug("Received packet.")
    direction = from_client(pa)
    buf = buf1 if direction else buf2
    buf += raw(pa)
    msg = Msg.fromRaw(buf, direction)
    while msg:
        result = parse_packet(msg.json())
        action(result)
        msg = Msg.fromRaw(buf, direction)

def start_sniffing(action, capture_file=None):
    logger.debug("Launching sniffer in thread...")

    def _sniff(stop_event):
        if capture_file:
            sniff(
                filter="tcp port 5555",
                lfilter=lambda p: p.haslayer(Raw),
                stop_event=stop_event,
                prn=lambda p: on_receive(p, action),
                offline=capture_file,
            )
        else:
            sniff(
                filter="tcp port 5555",
                lfilter=lambda p: p.haslayer(Raw),
                stop_event=stop_event,
                prn=lambda p: on_receive(p, action),
            )
        logger.info("sniffing stopped")

    e = threading.Event()
    t = threading.Thread(target=_sniff, args=(e,))
    t.start()

    def stop():
        e.set()

    logger.debug("Started sniffer in new thread")

    return stop

if __name__ == "__main__":
    def on_msg(msg):
        global m
        m = msg
        from pprint import pprint

        pprint(msg.json()["__type__"])
        print(msg.data)
        print(Msg.from_json(msg.json()).data)
    
    stop = start_sniffing(on_msg)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        stop()
