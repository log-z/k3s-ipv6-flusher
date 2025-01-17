import os
from pathlib import Path

TMP_DIR = Path('.tmp')
PID_FILENAME = TMP_DIR.joinpath('k3s-ipv6-flusher.pid')
MARK_FILENAME = TMP_DIR.joinpath('k3s-ipv6-flusher.mark')

DEFAULT_INTERVAL = 60

def get_interval():
    """获取运行间隔
    """

    interval = os.getenv('IPV6_FLUSHER_INTERVAL', DEFAULT_INTERVAL)
    return float(interval)
