## 專案說明
這是抓國泰行運公司航運單的爬蟲。<br/>
1. 先設定一個初始流水編號 ex: 60000000
2. 到航空公司提供查詢的網頁大量透過流水號批量查詢
3. 再對有興趣的航班去做詳細內容查詢

## 專案架構
- 國泰航運 [cathaypacificcargo](cathaypacificcargo/)
### 國泰航運
1. 多筆快速查詢
   - 爬蟲 [awb_mutlip_query.py](cathaypacificcargo/awb_mutlip_query.py)
   - 結果 [multi_query_result_{batch_no}.csv](cathaypacificcargo/data/multi_query_result_6.csv)
        >batch_no: 為建立初始查詢編號 multi_query_result_.csv 
2. 單筆詳細查詢
   - 清單 [interesting_awb_list.txt](cathaypacificcargo/data/interesting_awb_list.txt)
   - 爬蟲 [awb_detial_query.py](cathaypacificcargo/awb_detial_query.py)
   - 結果 [interesting_detial_result.csv](cathaypacificcargo/data/interesting_detial_result.csv)

### 參考資料
- [國泰航運查詢網頁](https://www.cathaypacificcargo.com/en-us/manageyourshipment/trackyourshipment.aspx)
- [航空運單號產生器](https://www.iatacodefor.com/airway-bill-series-generator/)
- [Air cargo tracking](https://www.track-trace.com/aircargo)