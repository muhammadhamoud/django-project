import threading
from typing import Callable


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


    # def __init__(
    #     self,
    #     group: None = None,
    #     target: Callable[..., object] | None = None,
    #     name: str | None = None,
    #     args: threading.Iterable[threading.Any] = ...,
    #     kwargs: threading.Mapping[str, threading.Any] | None = None,
    #     *,
    #     daemon: bool | None = None
    # ) -> None:
    #     super().__init__(group, target, name, args, kwargs, daemon=daemon)
