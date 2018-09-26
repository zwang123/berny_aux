import time

class Timer(object):
    """ A Timer class that supports start/stop/split/reset 
        error < 2 ms
        func call overhead < 0.05 ms unless len(self.split_time) > 10000
    """

    def __init__(self, msg=''):
        """ initialize and reset a timer """
        self.msg = msg
        self.reset()

    def __str__(self):
        elapsed = self.elapsed_time
        split = self.split_time
        for_msg = ' for ' + self.msg if self.msg else ''
        return \
        '    total    : wall time{} {:10.3f} sec, process time {:10.3f} sec\n' \
                .format(for_msg, 
                        elapsed.wall_time, elapsed.process_time) + \
        '\n'.join(
        '    split {:3d}: wall time{} {:10.3f} sec, process time {:10.3f} sec' \
                .format(i, for_msg, t.wall_time, t.process_time) \
                for i, t in enumerate(split)
        )

    def reset(self):
        """ reset to zero, clear split, and stop """
        # self.__now only valid if self.stopped
        self.__zero = self.__get_now()
        self.__split = [] #or numpy.ndarray?
        self.__split_total = Time()
        self.__now = self.__zero
        self.__stopped = True
        return self

    def start(self):
        """ start the timer if stopped """
        if self.stopped:
            stopped_time = self.__get_now() - self.__now
            self.__zero += stopped_time
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
            self.__split_total += self.__split[-1]
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
        
    def __repr__(self):
        return '{}(wall_time={}, process_time={})'.format(
                self.__class__.__name__, self.wall_time, self.process_time)
        
    def __str__(self):
        return self.__repr__()

#from numpy import ndarray, array
#class Time(ndarray):
#    def __new__(cls, wall_time=0.0, process_time=0.0):
#        return super(Time, cls).__new__(cls, 
#                (2,), dtype=float, 
#                buffer=array((wall_time, process_time), dtype=float))
#
#    #def __init__(self, wall_time=0.0, process_time=0.0):
#    #    print(array((wall_time, process_time), dtype=float))
#    #    super().__init__((2,), dtype=float, buffer=(wall_time, process_time))
#    #    #self = array((wall_time, process_time), dtype=float)
#
#    @property
#    def wall_time(self):
#        return self[0]
#
#    @property
#    def process_time(self):
#        return self[1]
