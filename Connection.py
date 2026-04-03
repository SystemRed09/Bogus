from httpx import get, Response
from enum import Enum
from subprocess import DEVNULL, STDOUT, call

class ErrorCode(Enum):
    ConnectionRefusedError = 403
    ConnectionError = 400

class Connection:
    TIMEOUT_TIME = 1.0

    ip4: str
    error: ErrorCode | None
    response: Response | None
    def __init__(self, ip4) -> None:
        self.ip4 = ip4
        self.error = None
        self.response = None

        # Ping to ensure no hanging response and secure connection
        isOn = call(f"ping -W {self.TIMEOUT_TIME} -c 1 {ip4}",
                    shell=True, stdout=DEVNULL, stderr=STDOUT)
        if isOn == 1:
            self.error = ErrorCode.ConnectionError
            return

        try:
            self.response = get(f"http://{ip4}/webglue/isw/status?_=0")
        except ConnectionRefusedError:
            self.error = ErrorCode.ConnectionRefusedError
        except ConnectionError:
            self.error = ErrorCode.ConnectionError

    @property
    def body(self) -> str:
        if self.response is None:
            return ""
        return self.response.text