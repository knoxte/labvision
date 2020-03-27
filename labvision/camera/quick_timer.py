from threading import Timer
import time


def time_in_s():
    """
    Utility method that returns absolute time
    """
    return time.time()

def datetimestr(format="%Y%m%d_%H%M%S"):
    """
    Date and time string, formatted according to specifier.

    :param format:  keyword argument that specifies how
                    date time string should be formatted
    :return: formatted date time string
    """
    now = time.gmtime()
    return time.strftime(format, now)

class QuickTimer:
    """
    QuickTimer is designed to help run a function at a series of specified times

    inputs:
    time_list : list of time values in seconds at which func is to be executed
    func : function which is to be executed, takes "elapsed time" as first argument supplied by class.
    func_args : the positional arguments taken by the function
    func_kwargs : the keyword arguments taken by the function

    Example usage:
    def example_func(time_elapsed, func_args, func_kwargs):
        print(time_elapsed)
        print(datetimestr())

    timed_collect = QuickTimer(time_list=list(range(2,120,10)), func=example_func, func_args=None, func_kwargs=None)

    """

    def __init__(self, time_list=None, func=None, func_args=None, func_kwargs=None):
        self.counter = 0
        self.interval = time_list[0]
        self.t_start = time_in_s()
        self.t_elapsed = 0
        self.time_list = time_list

        self.func = func
        self.func_args = func_args
        self.func_kwargs = func_kwargs

        self.start()

    def start(self):
        self._timer = Timer(self.interval, self._run)
        self._timer.start()
        self.is_running = True

    def _run(self):
        self.is_running = False
        self.t_elapsed = time_in_s() - self.t_start
        self.func(self.t_elapsed, self.func_args, self.func_kwargs)

        if self.counter < (len(self.time_list) - 1):
            self.interval = self.time_list[self.counter + 1] - self.time_list[self.counter]
            self.start()
        else:
            self.stop()
        self.counter += 1

    def stop(self):
        self.is_running = False
        self._timer.cancel()

