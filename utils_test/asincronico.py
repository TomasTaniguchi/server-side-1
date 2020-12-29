import multiprocessing
import time
from threading import current_thread
from utils.rx_test import Observable
from utils.rx_test import ThreadPoolScheduler

optimal_thread_count = multiprocessing.cpu_count() + 1
poo_scheduler = ThreadPoolScheduler(optimal_thread_count)
print(optimal_thread_count)

def intense_calculation(value):
    time.sleep(1)
    return value


# create Process 1
Observable.from_(["Alpha", "Beta", "Gama", "Delta", "Epsilon"])\
    .map(lambda s: intense_calculation(s)) \
    .subscribe_on(poo_scheduler) \
    .subscribe(on_next=lambda s: print("PROCESS 1 :("+current_thread().name+") ("+s+") "), \
               on_error=lambda e: print("e"),
               on_completed=lambda: print("PROCESS 1 done !"))


# create Process 2
Observable.from_(["Alpha", "Beta", "Gama", "Delta", "Epsilon"])\
    .map(lambda s: intense_calculation(s)) \
    .subscribe_on(poo_scheduler) \
    .subscribe(on_next=lambda s: print("PROCESS 2 :("+current_thread().name+") ("+s+") "), \
               on_error=lambda e: print("e"),
               on_completed=lambda: print("PROCESS 2 done !"))

# create Process 3
Observable.from_(["Alpha", "Beta", "Gama", "Delta", "Epsilon"])\
    .map(lambda s: intense_calculation(s)) \
    .subscribe_on(poo_scheduler) \
    .subscribe(on_next=lambda s: print("PROCESS 3 :("+current_thread().name+") ("+s+") "), \
               on_error=lambda e: print("e"),
               on_completed=lambda: print("PROCESS 3 done !"))


input("Press any key to exit\n")