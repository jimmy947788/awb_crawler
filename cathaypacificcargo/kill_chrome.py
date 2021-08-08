import psutil
import os
import sys

if os.name == 'nt':
    chromiumPath = "C:/Users/Jimmy Wu/AppData/Local/pyppeteer/pyppeteer/local-chromium/588429/chrome-win32/chrome.exe"
else:
    chromiumPath = "/usr/bin/chromium-browse"
print(f"chromiumPath={chromiumPath}")

PROCNAME = chromiumPath.split('/')[-1]
print(f"PROCNAME={PROCNAME}")

for proc in psutil.process_iter():
    # check whether the process name matches
    if proc.name() == PROCNAME:
        proc.kill()
sys.exit(1)