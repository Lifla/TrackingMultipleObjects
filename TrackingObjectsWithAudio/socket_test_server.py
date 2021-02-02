import socket

if __name__ == '__main__':
    # audio_queue = Queue()
    # audio_process = Process(target=audio_loop, args=(audio_queue,))
    # audio_process.start()
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.setblocking(0)
    sock.bind('\0user.audio.test')
    sock.listen(1)
    print('waiting for audio program to connect...')
    # conn = {}
    # addr = ''
    while True:
        try:
            conn, addr = sock.accept()
            conn.setblocking(0)
            break
        except BlockingIOError:
            pass

    while True:
        # get audio
        # if not audio_queue.empty():
        #     print(audio_queue.get_nowait())
        try:
            print(conn.recv(1024).decode())
        except :
            pass
    # audio_process.kill()
    # audio_process.join()
    conn.close()
    sock.close()