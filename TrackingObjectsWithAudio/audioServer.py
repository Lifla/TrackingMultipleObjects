#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib.

Matplotlib and NumPy have to be installed.

"""
import argparse
import queue
import sys

import numpy as np
import sounddevice as sd
import socket

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-w', '--window', type=float, default=200, metavar='DURATION',
    help='visible time slot (default: %(default)s ms)')
parser.add_argument(
    '-i', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-b', '--blocksize', type=int, help='block size (in samples)')
parser.add_argument(
    '-r', '--samplerate', type=float, help='sampling rate of audio device')
parser.add_argument(
    '-n', '--downsample', type=int, default=10, metavar='N',
    help='display every Nth sample (default: %(default)s)')
args = parser.parse_args(remaining)
if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1
q = queue.Queue()


def audio_callback(indata, frames, time, status):
    global plotdata
    global connected
    """This is called (from a separate thread) for each audio block."""
    # if status:
    #     print(status, file=sys.stderr)
    abs_samples = [abs(x) for x in indata]

    volume_data = [sum(abs_samples)[0] / len(abs_samples)]
    q.put(volume_data)

    # update plotdata
    shift = len(volume_data)
    plotdata = np.roll(plotdata, -shift, axis=0)
    plotdata[-shift:, :] = volume_data

    cut_value = np.average(plotdata[-3:, :])
    medium_shot_value = np.average(plotdata[-30:, :])

    cut_detect = True if cut_value > 0.15 else False
    medium_shot_detect = True if medium_shot_value > 0.07 else False

    if not connected:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.setblocking(0)
        try:
            sock.connect('\0user.audio.test')
            connected = True
            print('connected to video server')
        except ConnectionRefusedError:
            pass
        except BlockingIOError:
            pass

    if cut_detect:
        print('cut')
        print(cut_value)
        if connected:
            try:
                sock.sendall('cut'.encode())
            except:
                sock.close()
                connected = False
                print('disconnected from video server')
    if medium_shot_detect:
        print('medium shot')
        print(medium_shot_value)
        if connected:
            try:
                sock.sendall('medium'.encode())
            except:
                sock.close()
                connected = False
                print('disconnected from video server')


try:
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        args.samplerate = device_info['default_samplerate']

    length = int(args.window * args.samplerate / (1000 * args.downsample))
    plotdata = np.zeros((length, len(args.channels)))
    connected = False

    stream = sd.InputStream(
        device=args.device, channels=max(args.channels),
        samplerate=args.samplerate, callback=audio_callback)
    with stream:
        while True:
            pass
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))