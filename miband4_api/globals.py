def init():
    global band
    global start_log_ts
    global end_log_ts
    global logged_data
    global finish_flag
    global now_ts

    band = None
    start_log_ts = None
    end_log_ts = None
    now_ts = None
    logged_data = {}
    finish_flag = False

