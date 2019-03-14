#!/usr/bin/env python3

import socket
import time


def send_command(s, IP, PORT, sec, cmd, seq, bits):
    """
    send_cmd(socket, str, str, str, float) -> None

    s = socket
    IP = IP Address
    PORT = Port
    cd = AT command to be sent
    sec = how long to continuously send.
    """
    # print(IP, PORT)
    # print(s)
    # s.connect((IP, PORT))
    if sec > 1:
        sleep_time = .03
    else:
        sleep_time = sec / 10
    start = time.time()
    while time.time() < (start + sec):
        print("sending")
        s.sendto(cmd.format(seq, bits).encode('utf-8'), (IP, PORT))
        time.sleep(sleep_time)
        seq += 1
    # s.close()
    return seq


def main():
    drone_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # drone_ip = "127.0.0.1"
    drone_ip = "192.168.1.1"
    drone_at_port = 5556

    at = "AT*REF={},{}\r"
    # 18, 20, 22, 24 set to 1
    def_set_bits = 290717696
    takeoff_bit = 2**9
    # cmd = def_set_bits + takeoff_bit
    seq = 1

    seq = send_command(drone_socket, drone_ip, drone_at_port, 1, at, seq,
                       def_set_bits + takeoff_bit)

    time.sleep(4)

    seq = send_command(drone_socket, drone_ip, drone_at_port, 1, at, seq,
                       def_set_bits)


if __name__ == "__main__":
    main()
