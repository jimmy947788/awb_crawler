from time import sleep, time
import requests
from bs4 import BeautifulSoup
import js2py
import os
import pathlib

if __name__ == '__main__':

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

workerFolder = pathlib.Path().resolve()
print(f"workerFolder={workerFolder}" )

init_number = 6022000
csvFile = os.path.join(workerFolder, "data/awb_query_result.csv")
print(f"csvFile={csvFile}" )
if os.path.exists(csvFile):
    with open(csvFile, 'r',  encoding="utf-8") as f:
        last_line = f.readlines()[-1]
    init_number = int(last_line.split(',')[0][4:-1])

print(f"init_number={init_number}")
increase_number = int(init_number)

inc_number = 0
while True:
    if inc_number == 0:
        inc_number = init_number

    numbers = ""
    for i in range(100):
        #numbers = "160-64539565-;160-64539554-;160-64539543-;160-64539532-;160-64539521-;160-64539510-"
        inc_number+=1
        dig = check_7dig(str(inc_number))
        number_8dig =  f"{inc_number}{dig}"
        numbers += f"160-{number_8dig}-;"

    print("query AWE for website")
    url = "https://www.cathaypacificcargo.com/%E7%AE%A1%E7%90%86%E6%82%A8%E7%9A%84%E8%B2%A8%E4%BB%B6/%E8%B2%A8%E4%BB%B6%E8%BF%BD%E8%B9%A4/tabid/109/language/zh-HK/Default.aspx?MultiAWBNo="
    r = requests.get(url + numbers)

    if r.status_code == requests.codes.ok:
        #print(r.text)
        soup = BeautifulSoup(r.text)
        #print(soup)
        rows= soup.select("#dnn_ctr863_ViewTnT_ctl00_plMultipleAWB > div > div.content > div.content_article > table > tr")
        for rowTag in rows[1:]:
            #print(f"row={rowTag}, type={type(rowTag)}")
            columnTags=  rowTag.find_all("td")
            
            columns = []
            for tag in columnTags:
                columns.append(tag.text)
            print(columns)

            if columns[0]:
                strColumns =  ",".join(columns[1:])   #remove first column
                with open("data/awb_query_result.csv", "a", encoding="utf-8") as f: 
                    f.write(f"{strColumns}\n")

    print("wait 5 secons....")
    sleep(5)