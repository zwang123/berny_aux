import time

class Timer(object):
    """ A Timer class that supports start/stop/split/reset """

    def __init__(self):
        """ initialize and reset a timer """
        self.reset()

    def reset(self):
        """ reset to zero, clear split, and stop """
        # self.__now only valid if self.stopped
        self.__zero = self.__get_now()
        self.__split = [] #???
        self.__split_total = Time()
        #self.__last = self.__zero
        self.__now = self.__zero
        self.__stopped = True
        return self

    def start(self):
        """ start the timer if stopped """
        if self.stopped:
            stopped_time = self.__get_now() - self.__now
            self.__zero += stopped_time
            #self.__last += stopped_time
            self.__stopped = False
        return self

    def stop(self):
        """ stop the timer if started """
        if not self.stopped:
            self.__now = self.__get_now()
            self.__stopped = True
        return self

    def split(self):
        """ split the timer if started, does not stop """
        if not self.stopped:
            self.__split.append(self.get_split())
            self.__split = self.split_time
            self.__split_total += self.__split[-1]
            #pass
            #self.__last = self.__get_now()
        return self

    def get_split(self):
        return self.elapsed_time - self.__split_total

    @property
    def stopped(self):
        return self.__stopped

    @property
    def elapsed_time(self):
        return self.__now - self.__zero if self.stopped \
                else self.__get_now() - self.__zero

    @property
    def split_time(self):
        #return self.__split + [self.elapsed_time - np.sum(self.__split)]
        return self.__split + [self.get_split()]

    @classmethod
    def __get_now(cls):
        return Time(cls.__wall_time_func(), cls.__process_time_func())

    __wall_time_func = time.perf_counter
    __process_time_func = time.process_time

class Time(object):
    def __init__(self, wall_time=0.0, process_time=0.0):
        self.wall_time = wall_time
        self.process_time = process_time

    def __iadd__(self, other):
        self.wall_time += other.wall_time
        self.process_time += other.process_time
        return self

    def __sub__(self, other):
        return Time(self.wall_time - other.wall_time, 
                    self.process_time - other.process_time)

#from numpy import ndarray, array
#class Time(ndarray):
#    def __init__(self, wall_time=0.0, process_time=0.0):
#        #super().__init__((wall_time, process_time), dtype=float)
#        self = array((wall_time, process_time), dtype=float)
#
#    @property
#    def wall_time(self):
#        return self[0]
#
#    @property
#    def process_time(self):
#        return self[1]
