from audioTest import audio_loop
from multiprocessing import Process, Queue

if __name__ == '__main__':
    audio_queue = Queue()
    audio_process = Process(target=audio_loop, args=(audio_queue,))
    audio_process.start()

    while True:
        # get audio
        if not audio_queue.empty():
            print(audio_queue.get_nowait())