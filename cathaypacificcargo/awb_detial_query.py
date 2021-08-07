import asyncio
import os
from pyppeteer import launch

async def getTextFromFrame(frame, selector):
    try:
        ##time.sleep(2)
        await frame.waitForSelector(selector)
        element = await frame.querySelector(selector)
        text = await frame.evaluate('(element) => element.textContent', element)
        return text
    except:
        return ""

async def main() : 

    if os.name == 'nt':
        chromiumPath = "C:/Users/Jimmy Wu/AppData/Local/pyppeteer/pyppeteer/local-chromium/588429/chrome-win32/chrome.exe"
    else:
        chromiumPath = "/usr/bin/chromium-browser"
    print(f"chromiumPath={chromiumPath}")

    userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36';
    headless = True # True: 沒有瀏覽器
    options = {
        "args": [
            '--no-sandbox',
            f'--user-agent="{userAgent}"'
        ],
        "headless": headless,
        "executablePath" :  chromiumPath
    }

    interesting_detial_result_file = os.path.join(os.getcwd(), "cathaypacificcargo/data/interesting_detial_result.csv")
    with open(interesting_detial_result_file, "r") as f: 
        numbers = f.readlines()
        numbers.reverse()
    last_number = numbers[0].split(',')[0]

    interesting_awb_file =  os.path.join(os.getcwd(), "cathaypacificcargo/data/interesting_awb_list.txt")
    with open(interesting_awb_file, 'r') as f:
        numbers = f.readlines()
        numbers.reverse()

    for number in numbers:
        number = number.replace("\n", "")
        if not number :
            continue

        if number >= last_number:
            continue
        
        print(f"number={number}")
        
        try:  
            browser = await launch(options) #'executablePath': exepath,, 'slowMo': 30
            page = await browser.newPage()
            await page.setUserAgent(userAgent)
            await page.setExtraHTTPHeaders({
                'authority' :'www.cathaypacificcargo.com',
                'path': '/en-us/manageyourshipment/trackyourshipment.aspx',
                'upgrade-insecure-requests': '1',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,ko;q=0.5'
            })

            await page.setViewport({'width': 0, 'height': 0})

            await page.goto(f"https://www.cathaypacificcargo.com/ManageYourShipment/TrackYourShipment/tabid/108/SingleAWBNo/{number}/language/en-US/Default.aspx", { "waitUntil" : "domcontentloaded" })
                                         
            html = await page.content()

            origin = await getTextFromFrame(page, "#FreightStatus-Origin")
            print(f"origin={origin}")
            destination = await getTextFromFrame(page, "#FreightStatus-Destination")
            print(f"destination={destination}")

            if origin and destination: 
                status = await getTextFromFrame(page, "#Latest_Status-Content > div > div:nth-child(2)")
                status = status.replace(",", " ")
                print(f"status={status}")
                flight = await getTextFromFrame(page, "#Latest_Status-Content > div > div:nth-child(5)")
                print(f"flight={flight}")
                print(f"{origin} -> {destination} , {status} {flight}")
                with open(interesting_detial_result_file, "a") as f: 
                    f.write(f"{number},{origin},{destination},{status},{flight}\n")
            else:
                with open(interesting_detial_result_file, "a") as f: 
                    f.write(f"{number},,,,\n")
            
        except Exception as e:
            print(e)
        finally:
            #await resultPage.close()
            ##await page.close()
            await browser.close()
           
asyncio.get_event_loop().run_until_complete(main())

