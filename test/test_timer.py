from multiprocessing import Pool
from os import cpu_count
from berny_aux.timer import Timer
from math import sqrt

#def f(x):
#    y=0.0
#    y+=x*x
#    return y
#def f(x):
#    y = 0.0
#    for i in range(10000000):
#        y+=x*x
#    return y

if __name__ == '__main__':
    print(cpu_count())
    t = Timer()
    t.start()
    with Pool() as p:
        #result = (p.map(f, list(range(cpu_count()))))
        result = (p.map(sqrt, list(range(cpu_count()))))
    #with Pool() as p:
    #    #f = lambda x: x*x
    #    for i in range(1000):
    #        #result = (p.map((lambda x: (x*x)), list(range(cpu_count()))))
    #        result = (p.map(f, list(range(cpu_count()))))
    t.stop()
    print(t.elapsed_time.wall_time)
    print(t.elapsed_time.process_time)
    
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
      
    # timeit statement 
    print(timeit.timeit(setup = mysetup, 
                        stmt = mycode, 
                        number = 10) * 0.1)

    # timeit statement 
    print(timeit.timeit(setup = "from berny_aux.timer import Timer; t = Timer()", 
                        stmt = "t.start(); t.split(); t.stop(); t.elapsed_time; t.split_time", 
                        number = 10000 ) * 0.0001)
