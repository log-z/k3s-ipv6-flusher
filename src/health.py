import os
import sys
import conf
import datetime

def startup_check():
    """启动检查
    """

    if os.path.exists(conf.PID_FILENAME):
        print('K3s IPv6 Flusher is running.')
    else:
        print('K3s IPv6 Flusher is stop.', file=sys.stderr)
        sys.exit(1)

def readiness_check():
    """就绪检查
    """

    if os.path.exists(conf.MARK_FILENAME):
        print('K3s IPv6 Flusher is readiness.')
    else:
        print('K3s IPv6 Flusher is not readiness.', file=sys.stderr)
        sys.exit(1)

def liveness_check():
    """存活检查
    """

    if os.path.exists(conf.MARK_FILENAME):
        window_sec = conf.get_interval() * 2
        now = datetime.datetime.now()
        last_modified_timestamp = os.path.getmtime(conf.MARK_FILENAME)
        last_modified_datetime = datetime.datetime.fromtimestamp(last_modified_timestamp)

        if last_modified_datetime + datetime.timedelta(seconds=window_sec) >= now:
            print('K3s IPv6 Flusher is liveness.')
            sys.exit(0)

    print('K3s IPv6 Flusher is not liveness.', file=sys.stderr)
    sys.exit(1)

if __name__ == '__main__':
    help_info = 'Usage: python health.py [startup|readiness|liveness]'

    if len(sys.argv) < 2:
        print(help_info, file=sys.stderr)
        sys.exit(1)
    
    action = sys.argv[1]
    if action == 'startup':
        startup_check()
    elif action == 'readiness':
        readiness_check()
    elif action == 'liveness':
        liveness_check()
    else:
        print(help_info, file=sys.stderr)
        sys.exit(1)
