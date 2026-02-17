# shell_simulation.py
import threading
from collections import deque
import time


# Memory Management Parameters
TOTAL_FRAMES = 4
memory = [None] * TOTAL_FRAMES
fifo_queue = deque()
page_faults = 0

# Example process pages
process_pages = {
    "P1": [0, 1, 2],
    "P2": [0, 1],
    "P3": [0, 1, 2, 3]
}


# Paging System
def access_page(process, page, algorithm='FIFO'):
    global memory, fifo_queue, page_faults
    if page in memory:
        print(f"Process {process} accessed page {page} in memory")
        if algorithm == 'LRU':
            memory.remove(page)
            memory.append(page) 
    else:
        page_faults += 1
        print(f"Page fault! Process {process} needs page {page}")
        if None in memory:
            index = memory.index(None)
            memory[index] = page
        else:
            replace_page(algorithm, page)
    if algorithm == 'FIFO' and page not in fifo_queue:
        fifo_queue.append(page)
    print(f"Memory: {memory}\n")

def replace_page(algorithm, new_page):
    global memory, fifo_queue
    if algorithm == 'FIFO':
        old_page = fifo_queue.popleft()
        index = memory.index(old_page)
        memory[index] = new_page
        fifo_queue.append(new_page)
        print(f"FIFO replaced page {old_page} with {new_page}")
    elif algorithm == 'LRU':
        old_page = memory.pop(0)
        memory.append(new_page)
        print(f"LRU replaced page {old_page} with {new_page}")


# Producer-Consumer Problem
BUFFER_SIZE = 3
buffer = []
mutex = threading.Semaphore(1)
empty = threading.Semaphore(BUFFER_SIZE)
full = threading.Semaphore(0)

def producer():
    for i in range(5):
        empty.acquire()
        mutex.acquire()
        buffer.append(i)
        print(f"Producer added item {i} -> Buffer: {buffer}")
        mutex.release()
        full.release()
        time.sleep(0.5)

def consumer():
    for i in range(5):
        full.acquire()
        mutex.acquire()
        item = buffer.pop(0)
        print(f"Consumer consumed item {item} -> Buffer: {buffer}")
        mutex.release()
        empty.release()
        time.sleep(1)


# Simulate Shell Commands
def simulate_shell():
    global memory, fifo_queue, page_faults  # <-- ensure global is at start
    print("=== Memory Management Simulation (FIFO) ===")
    commands = [("P1",0), ("P1",1), ("P2",0), ("P3",0), ("P1",2), ("P2",1)]
    for proc, page in commands:
        access_page(proc, page, algorithm='FIFO')
    print(f"Total page faults (FIFO): {page_faults}\n")
    
    # Reset for LRU simulation
    memory = [None]*TOTAL_FRAMES
    fifo_queue.clear()
    page_faults = 0

    print("=== Memory Management Simulation (LRU) ===")
    for proc, page in commands:
        access_page(proc, page, algorithm='LRU')
    print(f"Total page faults (LRU): {page_faults}\n")

    print("=== Producer-Consumer Simulation ===")
    p = threading.Thread(target=producer)
    c = threading.Thread(target=consumer)
    p.start()
    c.start()
    p.join()
    c.join()

if __name__ == "__main__":
    simulate_shell()
