from berny_aux.timer import Timer, Time
from time import process_time, sleep
# importing the required module 
import timeit 

# code snippet to be executed only once 
mysetup = """
from multiprocessing import Pool
from os import cpu_count
from math import sqrt
"""
      
# code snippet whose execution time is to be measured 
mycode = """
with Pool() as p:
    result = (p.map(sqrt, list(range(cpu_count()))))
"""

if __name__ == '__main__':
    
    eval(repr(Time()))

    number = 10

    exec(mysetup, globals(), locals())
    print("cpu count:", cpu_count())
    tmp = Timer().start()
    t = Timer()
    t1 = Timer()
    for _ in range(2):
        t.reset()
        t1.reset()
        t.start()
        t1.start()
        for i in range(number):
            exec(mycode, globals(), locals())
            t.split()
            t1.split()
        t.stop()
        print(t)
        sleep(0.5)
        print(t1)
        print("Timer wall time", t.elapsed_time.wall_time/number)
        print("Timer process time", t.elapsed_time.process_time/number)
        #print("Timer split time", t.split_time)
        #print(repr(t.split_time))
    
    # timeit statement 
    print("timeit wall time",
          timeit.timeit(setup = mysetup, 
                        stmt = mycode, 
                        number = number) / number)
    
    # timeit statement 
    print("timeit process time",
          timeit.timeit(setup = mysetup, 
                        stmt = mycode, 
                        timer = process_time,
                        number = number) / number)

    # timeit statement 
    print("Timer method time",
          timeit.timeit(setup = "from berny_aux.timer import Timer;"+\
                                " t = Timer()", 
                        stmt = "t.start(); t.split(); t.stop();"+\
                               " t.elapsed_time; t.split_time", 
                        number = 20000 ) * 0.00005)
