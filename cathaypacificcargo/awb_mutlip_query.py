from time import sleep, time
import requests
from bs4 import BeautifulSoup
import js2py
import os
import pathlib
import common

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

worker_folder = pathlib.Path(__file__).parent.resolve()
data_folder = os.path.join(worker_folder, 'data')

logger = common.init_logger(worker_folder, "awb_mutlip_query")

start_number = 6022000
end_number = 7000000
batch_number = str(start_number)[0]
multi_query_result_path = os.path.join(data_folder, f"multi_query_result_{batch_number}.csv")
logger.info(f"multi_query_result_path={multi_query_result_path}" )
if os.path.exists(multi_query_result_path):
    with open(multi_query_result_path, 'r',  encoding="utf-8") as f:
        last_line = f.readlines()[-1]
    start_number = int(last_line.split(',')[0][4:-1])

logger.info(f"start_number={start_number}")
increase_number = int(start_number)

inc_number = 0
while True:
    if inc_number == 0:
        inc_number = start_number

    # 組出查詢參數
    multiAWBNo= ""
    for i in range(100):
        inc_number+=1
        dig = check_7dig(str(inc_number))
        number_8dig =  f"{inc_number}{dig}"
        multiAWBNo += f"160-{number_8dig}-;"

        if  inc_number >= end_number:
            logger.info(f"already over end number. ( {start_number} ~ {end_number})")
            exit()

    logger.info("start query multi AWB number")
    url = f"https://www.cathaypacificcargo.com/%E7%AE%A1%E7%90%86%E6%82%A8%E7%9A%84%E8%B2%A8%E4%BB%B6/%E8%B2%A8%E4%BB%B6%E8%BF%BD%E8%B9%A4/tabid/109/language/zh-HK/Default.aspx?MultiAWBNo={multiAWBNo}"
    r = requests.get(url)

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
            logger.info(columns)

            if columns[0]:
                strColumns =  ",".join(columns[1:])   #remove first column
                with open(multi_query_result_path, "a", encoding="utf-8") as f: 
                    f.write(f"{strColumns}\n")

    logger.info("wait 5 secons....")
    sleep(5)