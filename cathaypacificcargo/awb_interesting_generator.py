
import os
import pathlib


if __name__ == '__main__':
    workerFolder = pathlib.Path().resolve()
    print(f"workerFolder={workerFolder}" )

    batch_number = 6
    multi_query_result_file = os.path.join(workerFolder, f"cathaypacificcargo/data/multi_query_result_{batch_number}.csv")
    interesting_awb_list_file = os.path.join(workerFolder, f"cathaypacificcargo/data/interesting_awb_list.txt")

    location_filter = [ "HKG", "LHR"]
    month_filter = [ "AUG", "JUL"]
    new_interesting_awb = []
    with open(multi_query_result_file, 'r',  encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().upper()
            if any(x in line for x in location_filter) and any(x in line for x in month_filter) :
                awb = line.split(',')[0]
                if awb:
                    new_interesting_awb.append(awb)

    
    with open(interesting_awb_list_file, 'r',  encoding="utf-8") as f:
        old_interesting_awb = f.readlines()
        old_interesting_awb_last = old_interesting_awb[-1].strip()

    for awb in new_interesting_awb:
        if awb > old_interesting_awb_last: 
            with open(interesting_awb_list_file, 'a',  encoding="utf-8") as f:
                f.write(f"{awb}\n")
