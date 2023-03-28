from threading import Thread
from typing import Callable, Tuple, Dict, Optional


class ThreadWithReturnValue:
    """
    Create a wrapper for thread that can get the target return value via join method
    """
    def __init__(
            self, func: Callable, func_args: Optional[Tuple] = None,
            func_kwargs: Optional[Dict[str, object]] = None
    ):
        """
        Init method
        :param func: target function
        :param func_args: args for target function
        :param func_kwargs: kwargs for target function
        """
        self.__result: object = None
        self.__func: Callable = func
        if func_args is None:
            func_args: Tuple = ()
        if func_kwargs is None:
            func_kwargs: Dict[str, object] = {}
        self.__func_args: Tuple = func_args
        self.__func_kwargs: Dict[str, object] = func_kwargs
        self.__thread = Thread(target=self.__thread_func)
        self.__thread_has_been_execute: bool = False    # whether the inner thread has been executed (only execute the thread once)

    def __thread_func(self):
        """
        Function that will be running by the thread
        :return:
        """
        self.__thread_has_been_execute = True   # mark that the inner thread has been executed => can not be executed anymore
        self.__result = self.__func(
            *self.__func_args, **self.__func_kwargs
        )

    def start(self) -> None:
        """
        Execute the thread
        :return:
        """
        if self.__thread_has_been_execute:
            raise ValueError("The thread has been executed before")
        self.__thread.start()

    def join(self, timeout: Optional[float] = None):
        """
        Join to the main thread
        :param timeout: timeout for join
        :return: the result of inner function
        """
        if not self.__thread_has_been_execute:
            raise ValueError("The thread hasn't been executed")
        self.__thread.join(timeout=timeout)
        return self.__result
