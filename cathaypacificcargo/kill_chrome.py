import psutil
import os
import sys
import traceback

def main():
    try:
        if os.name == 'nt':
            PROCNAME = "chrome"
        else:
            PROCNAME = "chromium"
        print(f"PROCNAME={PROCNAME}")

        for proc in psutil.process_iter():
            # check whether the process name matches
            #print(f"name : {proc.name()}")
            if "chromium" in proc.name() :
                print(f"kill process {proc.pid}:{proc.name()} ")
                proc.kill()
    except Exception as e:
        error_class = e.__class__.__name__ #取得錯誤類型
        detail = e.args[0] #取得詳細內容
        cl, exc, tb = sys.exc_info() #取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2] #取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        print(errMsg)

if __name__ == '__main__':
    main()
    sys.exit(1)