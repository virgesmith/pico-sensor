from sdcard import SDCard
import uos
import picowireless as pw

pw.init()
print(pw.is_sdcard_detected())

with SDCard("/sd") as sd:

  print(f"Size: {sd.sectors/2048} MB") # to display card's capacity in MB

  files = [f"{sd.mount_point}/{f}" for f in uos.listdir("/sd")]

  for file in files:
    if file[-4:] == ".txt":
      with open(file) as fd:
        print(file)
        print(fd.read())


