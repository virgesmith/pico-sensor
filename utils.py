import time
import ujson


def secrets():
  with open("secrets.json","r") as fh:
    creds = ujson.load(fh)
  return creds


def utc_time_str() -> str:
  """e.g. 2022-09-07T10:00:00Z"""
  (y, m, d, h, min, s, _, _) = time.gmtime()
  return f"{y:04d}-{m:02d}-{d:02d}T{h:02d}:{min:02d}:{s:02d}Z"

