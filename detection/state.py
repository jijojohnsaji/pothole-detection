# detection/state.py
import threading

_lock = threading.Lock()
_trigger = False
_last_conf = 0.0

def set_trigger(conf: float):
    global _trigger, _last_conf
    with _lock:
        _trigger = True
        _last_conf = float(conf)

def pop_trigger():
    """
    Returns (triggered: bool, confidence: float) and clears the trigger if it was set.
    """
    global _trigger, _last_conf
    with _lock:
        if _trigger:
            _trigger = False
            return True, _last_conf
        return False, 0.0