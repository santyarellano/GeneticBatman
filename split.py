import threading


class Split(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self._default_args = self._target, self._args, self._kwargs

    def run(self, *args, **kwargs):
        super().run()
        self.reset()

    def reset(self, *args, **kwargs):
        self._target = self._default_args[0]
        self._args = args or self._default_args[1]
        self._kwargs = kwargs or self._default_args[2]
