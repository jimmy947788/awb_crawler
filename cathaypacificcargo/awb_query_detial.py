import asyncio
import os
from pyppeteer import launch, page
import time
import math
import js2py

async def getTextFromFrame(frame, selector):
    try:
        ##time.sleep(2)
        await frame.waitForSelector(selector)
        element = await frame.querySelector(selector)
        text = await frame.evaluate('(element) => element.textContent', element)
        return text
    except:
        return ""

async def findNewPage(browser, number) -> page.Page:
    for p in await browser.pages():
        title = await p.title()
        print(title)
        if number in title:
            resultPage = p
            print(resultPage)
            return resultPage
    return None

async def main() : 

    check_7dig = js2py.eval_js( """
        function check_7dig(x)
        {
            var prev = 0;
            var dig;
            for (var i=0;i<7;i++)
            {
                var c = parseInt(x.charAt(i));
                dig =  c+10*prev;
                var nn=15;
                while ((nn*7)>dig) {nn--; };
                dig = dig-nn*7;
                prev = dig;
            }
            return dig;
        }
    """ )
    
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

    with open('data/interesting_awb.txt', 'r') as f:
        numbers = f.readlines()
        numbers.reverse()

    for number in numbers:
        number = number.replace("\n", "")
        if not number :
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
                with open("data/interesting_awb_detial.csv", "a") as f: 
                    f.write(f"{number},{origin},{destination},{status},{flight}\n")
            else:
                with open("data/interesting_awb_detial.csv", "a") as f: 
                    f.write(f"{number},,,,\n")
            
        except Exception as e:
            print(e)
        finally:
            #await resultPage.close()
            ##await page.close()
            await browser.close()
           
asyncio.get_event_loop().run_until_complete(main())

