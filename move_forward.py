#!/usr/bin/env python3

import socket
import time
import threading
from struct import pack, unpack

at_ref = "AT*REF={},{}\r"
at_pcmd = "AT*PCMD_MAG={},{},{},{},{},{},{},{}\r"
at_calib = "AT*CALIB={},{}"
at_ftrim = "AT*FTRIM={}"
at_comwtg = "AT*COMWDG"

# drone_ip = "127.0.0.1"
drone_ip = "192.168.1.1"
drone_at_port = 5556
drone_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_command(sec, cmd, seq, *args):
    """
    send_cmd(socket, str, str, str, float) -> None

    s = socket
    drone_ip = drone_ip Address
    drone_at_port = Port
    cd = AT command to be sent
    sec = how long to continuously send.
    """
    sleep_time = .03
    # if sec > 1:
    #     sleep_time = .3
    # else:
    #     sleep_time = sec / 100
    start = time.time()
    while time.time() < (start + sec):
        drone_socket.sendto(cmd.format(seq, *args).encode('utf-8'),
                            (drone_ip, drone_at_port))
        time.sleep(sleep_time)
        seq += 1
    # s.close()
    return seq


def takeoff(seq):
    launch = str(0b10001010101000000001000000000)
    drone_socket.sendto(at_ftrim.format(seq).encode('utf-8'),
                        (drone_ip, drone_at_port))
    seq += 1
    time.sleep(4)

    drone_socket.sendto(at_ref.format(seq, launch).encode('utf-8'),
                        (drone_ip, drone_at_port))

    return seq + 1


def land(seq):
    land = str(0b10001010101000000000000000000)
    drone_socket.sendto(at_ref.format(seq, land).encode('utf-8'),
                        (drone_ip, drone_at_port))
    return seq + 1



def emergency(seq):
    land = str(0b10001010101000000000100000000)
    drone_socket.sendto(at_ref.format(seq, land).encode('utf-8'),
                        (drone_ip, drone_at_port))
    return seq + 1

def commwdg(seq):
    drone_socket.sendto(at_comwdg)


def main():
    # 18, 20, 22, 24 set to 1
    def_set_bits = 290717696
    takeoff_bit = 2**9
    # cmd = def_set_bits + takeoff_bit
    seq = 1

    forward = unpack('i', pack('f', .0000001))[0]
    turn = unpack('i', pack('f', 1))[0]
    vertical = unpack('i', pack('f', 1))[0]
    timer_t = 0.2
    com_watchdog_timer = threading.Timer(self.timer_t, commwdg)

    try:
        print("takeoff")
        seq = takeoff(seq)

        time.sleep(4)

        print("forward")
        # move forward
        seq = send_command(4, at_pcmd, seq, 1, 0, -1 * forward, 0, 0, 0, 0)

        time.sleep(2)

        print("hover")
        # hover
        seq = send_command(1, at_pcmd, seq, 0, 0, 0, 0, 0, 0, 0)

        time.sleep(2)

        print("land")
        # land
        seq = land(seq)

        time.sleep(1)

        print("takeoff")
        # takeoff
        seq = send_command(1, at_ref, seq, def_set_bits + takeoff_bit)
        time.sleep(4)

        print("turn")
        # turn
        seq = send_command(2, at_pcmd, seq, 1, 0, 0, 0, turn, 1, 0)
        time.sleep(2)

        print("hover")
        # hover
        seq = send_command(1, at_pcmd, seq, 0, 0, 0, 0, 0, 1, 0)
        time.sleep(2)

        print("forwards")
        # move forwards
        seq = send_command(4, at_pcmd, seq, 1, 0, -1 * forward, 0, 0, 1, 0)

        print("hover")
        # hover
        seq = send_command(1, at_pcmd, seq, 0, 0, 0, 1, 0, 0, 0)

        time.sleep(2)

        print("land")
        seq = land(seq)

    except KeyboardInterrupt as e:
        print("emergency")
        for x in range(10):
            emergency(seq)
            time.sleep(.1)


if __name__ == "__main__":
    main()
