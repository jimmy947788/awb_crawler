
import os
import pathlib

def main():
    workerFolder = pathlib.Path().resolve()
    print(f"workerFolder={workerFolder}" )

    batch_number = 6
    multi_query_result_file = os.path.join(workerFolder, f"cathaypacificcargo/data/multi_query_result_{batch_number}.csv")
    interesting_awb_list_file = os.path.join(workerFolder, f"cathaypacificcargo/data/interesting_awb_list.txt")

    location_filter = [ "HKG", "LHR"]
    month_filter = [ "AUG", "JUL"]
    new_interesting_awb_list = []
    with open(multi_query_result_file, 'r',  encoding="utf-8") as f:
        for row in f:
            row = row.strip().upper()
            if any(x in row for x in location_filter) and any(x in row for x in month_filter) :
                awb = row.split(',')[0]
                if awb and awb not in new_interesting_awb_list: 
                    new_interesting_awb_list.append(awb)   
    print(f"multi_query_result.csv have { len(new_interesting_awb_list) } lines.")


    print(f"save remove duplicates multi_query_result.csv ...")
    with open(interesting_awb_list_file, 'w',  encoding="utf-8") as f:
        for awb in new_interesting_awb_list:
            f.write(f"{awb}\n")
    print(f"interesting_awb_list.txt have { len(new_interesting_awb_list) } lines.")

if __name__ == '__main__':
    main()