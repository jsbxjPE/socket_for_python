import threading
def w():
    while 1:
        t1 = threading.Thread(target=q())
        t1.start()

def q():
    print('t2')