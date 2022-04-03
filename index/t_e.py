import threading
import time

def run(n):
    print("task", n)
    time.sleep(1)
    print('{} 2s'.format(n))
    time.sleep(1)
    print('{} 1s'.format(n))
    time.sleep(1)
    print('{} 0s'.format(n))
    time.sleep(1)

def run_w(n):
    i = 0
    while True:
        i = i + 1
        print('{} {}'.format(n,i))
        time.sleep(1)

if __name__ == '__main__':
    t1 = threading.Thread(target=run, args=("t",))
    t2 = threading.Thread(target=run_w, args=("t2",))
    t1.start()
    t2.start()