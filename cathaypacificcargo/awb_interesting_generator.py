
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
        lines = f.readlines()
        print(f"multi_query_result.csv have { len(lines) } lines.")
        lines = list( dict.fromkeys(lines) )
        print(f"multi_query_result.csv remove duplicates have { len(lines) } lines.")

    for line in lines:
        line = line.strip().upper()
        if any(x in line for x in location_filter) and any(x in line for x in month_filter) :
            awb = line.split(',')[0]
            if awb:
                new_interesting_awb_list.append(awb)     

    """
    with open(interesting_awb_list_file, 'r',  encoding="utf-8") as f:
        lines = f.readlines()
        print(f"interesting_awb_list.txt have { len(lines) } lines.")
        lines = list( dict.fromkeys(lines) )
        print(f"interesting_awb_list.txt remove duplicates have { len(lines) } lines.")
        old_interesting_awb_list = lines
        #old_interesting_awb_last = old_interesting_awb[-1].strip()
    """

    print(f"save remove duplicates multi_query_result.csv ...")
    with open(interesting_awb_list_file, 'w',  encoding="utf-8") as f:
        for awb in new_interesting_awb_list:
            #print(f"add {awb} to list file.")
            f.write(f"{awb}\n")
    
    with open(interesting_awb_list_file, 'r',  encoding="utf-8") as f:
        lines = f.readlines()
        print(f"interesting_awb_list.txt have { len(lines) } lines.")

if __name__ == '__main__':
    main()