import asyncio
import os
import sys
import traceback
from pyppeteer import browser, launch
import signal
import kill_chrome
import pathlib
import time
from datetime import datetime
import common
import awb_interesting_generator

async def getTextFromFrame(page, selector, timeout=30000):
    try:
        ##time.sleep(2)
        await page.waitForSelector(selector, { "timeout": timeout })
        element = await page.querySelector(selector)
        text = await page.evaluate('(element) => element.textContent', element)
        return text
    except:
        return ""

def printError(e):
    error_class = e.__class__.__name__ #取得錯誤類型
    detail = e.args[0] #取得詳細內容
    cl, exc, tb = sys.exc_info() #取得Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
    fileName = lastCallStack[0] #取得發生的檔案名稱
    lineNum = lastCallStack[1] #取得發生的行號
    funcName = lastCallStack[2] #取得發生的函數名稱
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    logger.error(errMsg)

def printMsg(number, msg):
    logger.info(f"[{number}] {msg}")

async def create_broeser():
    if os.name == 'nt':
            chromium_path = "C:/Users/Jimmy Wu/AppData/Local/pyppeteer/pyppeteer/local-chromium/588429/chrome-win32/chrome.exe"
    else:
        chromium_path = "/usr/bin/chromium-browser"
    #userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36';
    headless = True # True: 沒有瀏覽器
    options = {
        "args": [
            #'--disable-gpu',
            #'--disable-dev-shm-usage',
            ##'--disable-setuid-sandbox',
            #'--no-first-run',
            #'--no-zygote',
            #'--deterministic-fetch',
            #'--disable-features=IsolateOrigins',
            #'--disable-site-isolation-trials',
            '--no-sandbox',
            f'--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"'
        ],
        "headless": headless,
        "executablePath" :  chromium_path,
    }
    return await launch(options) #'executablePath': exepath,, 'slowMo': 30

async def get_awb_detail_tasks(number, taskId):
    t = time.process_time()
    printMsg(number, f"Task{taskId} start.")
    page = await browsers[taskId].newPage()
    try:  
        #await page.setUserAgent(userAgent)
        await page.setExtraHTTPHeaders({
            'authority' :'www.cathaypacificcargo.com',
            'path': '/en-us/manageyourshipment/trackyourshipment.aspx',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ko;q=0.5'
        })

        #await page.setViewport({'width': 0, 'height': 0})
        printMsg(number, "Go to page for get detial.")
        await page.goto(f"https://www.cathaypacificcargo.com/ManageYourShipment/TrackYourShipment/tabid/108/SingleAWBNo/{number}/language/en-US/Default.aspx", 
            { 
                "waitUntil" : "load",
                "timeout": 0 
            })                               
        #html = await page.content()

        origin = await getTextFromFrame(page, "#FreightStatus-Origin")
        logger.info(f"origin={origin}")
        destination = await getTextFromFrame(page, "#FreightStatus-Destination")
        logger.info(f"destination={destination}")

        status = ""
        flight = ""
        if origin and destination: 
            status = await getTextFromFrame(page, "#Latest_Status-Content > div > div:nth-child(2)", 5000)
            status = status.replace(",", " ")
            logger.info(f"status={status}")
            flight = await getTextFromFrame(page, "#Latest_Status-Content > div > div:nth-child(5)", 5000)
            logger.info(f"flight={flight}")
            printMsg(number, f"{origin} -> {destination} , {status} {flight}")

        async with locker:
            with open(interesting_detial_result_path, "a") as f: 
                f.write(f"{number},{origin},{destination},{status},{flight}\n")
    except Exception as e:
        printError(e)
    finally:
        #await resultPage.close()
        printMsg(number, "close page")
        await page.close()
        #await browser.close()

        elapsed_time = time.process_time() - t
        printMsg(number, f"Task{taskId}) done. (use {elapsed_time} s)")

async def run_batch_task(loop, batch_numbers):
    if len(browsers) != MAX_TASK_COUNT:
        for i in range(MAX_TASK_COUNT):
            b = await create_broeser()
            browsers.append(b)

    task_list =[]
    i = 0
    for number in batch_numbers:
        t = loop.create_task(get_awb_detail_tasks(number, i))
        task_list.append(t)
        i+=1
    
    await asyncio.wait(task_list)


def signal_handler(signum, frame):
    print('signal_handler: caught signal ' + str(signum))
    if signum == signal.SIGINT.value:
        print('SIGINT')
        loop.close()
        kill_chrome.main()
        sys.exit(1)

MAX_TASK_COUNT = 14
if __name__ == '__main__': 

    global interesting_detial_result_path
    global interesting_awb_path
    global locker
    global loop
    global logger
    global browsers

    worker_folder = pathlib.Path(__file__).parent.resolve()
    data_folder = os.path.join(worker_folder, 'data')

    logger = common.init_logger(worker_folder, "awb_detial_query")
    #awb_interesting_generator.main()
    # logger.info(f"chromium_path={chromium_path}")
    logger.info(f"worker_folder={worker_folder}" )
    logger.info(f"data_folder={worker_folder}" )
    logger.info(f"log_folder={worker_folder}" )


    already_query_numbers = []
    interesting_detial_result_path =  os.path.join(data_folder, "interesting_detial_result.csv")
    with open(interesting_detial_result_path, "r") as f: 
       for row in f:
           number = row.split(",")[0] 
           if number not in already_query_numbers:
                already_query_numbers.append(number)
    logger.info(f"interesting_detial_result.csv have { len(already_query_numbers) } lines.")

    interesting_awb_numbers = []
    interesting_awb_path =  os.path.join(data_folder, "interesting_awb_list.txt")
    with open(interesting_awb_path, 'r') as f:
       for row in f:
           number = row.strip()
           if number not in interesting_awb_numbers:
                interesting_awb_numbers.append(number)
    logger.info(f"interesting_awb_list.txt have { len(interesting_awb_numbers) } lines.")
    interesting_awb_numbers.reverse()

    signal.signal(signal.SIGINT, signal_handler)
    #print(signal.SIGINT)

    batch_numbers= []
    browsers = []
    locker = asyncio.Lock()
    #loop = asyncio.new_event_loop()
    #asyncio.set_event_loop(loop)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for number in interesting_awb_numbers:
        number = number.replace("\n", "")
        if not number :
            continue

        if number in already_query_numbers:
            logger.info(f"AWB {number} already get detial.")
            continue
        
        batch_numbers.append(number)
        #print(f"number={number}")
        
        if len(batch_numbers) == MAX_TASK_COUNT:
            ssss = ",".join(batch_numbers)
            logger.info(f"=====> batch task start")
            loop.run_until_complete(run_batch_task(loop, batch_numbers))
            logger.info(f"=====> batch task all done")
            batch_numbers.clear()
    
    loop.close()         
    #logger.info("kill alll chrome")
    kill_chrome.main() 
#asyncio.get_event_loop().run_until_complete(main())

