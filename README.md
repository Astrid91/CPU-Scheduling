# CPU-Scheduling
根據使用者輸入的 input 檔，讀取方法種類、time slice，以及各個
process，以二維串列的方式儲存 process 相關資訊，並根據 Arrival 
Time 以及 Process ID 先進行排列，跟根據方法種類進行不同的 CPU 排程
方法。排程完成後，依據題目格式及檔名要求寫入對應檔案，輸出檔中應
包含該排程方法的甘特圖，以及每個 process 的 Waiting Time 及
Turnaround Time。
### 方法一：First Come First Serve (FCFS) 
FCFS 是根據 process 的 Arrival Time 依序排序的，且為不可奪取的
排程法(Non-preemptive)，若 Arrival Time 相同，則根據 Process ID 來
決定先後順序。

首先，設置一 while 迴圈，且 timer 累加，當 timer 為某 process 抵
達的時間，便將其加入到 ready queue 中。每輪都會檢查 running list 是
否為空，若為空則取 ready queue 當中的第一個 process 進入到
running list；此外，也會檢查此 timer 時間是否為某個 process 做完的
時間，若剛好做完，則記錄該 process 的完成時間，並將 running list 清
空，然後檢查 ready queue 當中是否還有在等待的 process，若有則將其
放入 running list，若 ready queue 為空且後面還有其他的 process 還沒
進來，則繼續等待新的 process，否則表示該任務完成，使用 break 出迴
圈，並回傳甘特圖及計算每個 process 的 Waiting Time 及 Turnaround 
Time。
### 方法二：Round Robin (RR) 
RR 是先以 Arrival Time 和 Process ID 排序後，每個 process 可以根
據 time slice 輪流分配到 CPU 資源，當 Timeout 時，則排到 ready queue
的最後，換下一個 process 使用 CPU，若 process 做完，也輪到下一個
process 使用，且該 process 能擁有完整的一段 time slice。RR 為可奪取
的排程法(preemptive)。

首先，設置一 while 迴圈，且 timer 累加，當 timer 為某 process 抵
達的時間，便將其加入到 ready queue 中。每輪都會檢查 running list 是
否為空，若為空則取 ready queue 當中的第一個 process 進入到
running list；每輪的 timer 也會檢查此 timer 時間是否 Timeout 或為某
個 process 做完的時間，若為 Timeout，則將正在執行的 Process 放回
ready queue 的最後面排隊，若為某 process 剛好做完，則記錄該 process
的完成時間，並將 running list 清空，接著皆會檢查 ready queue 當中是
否還有在等待的 process，若有則將其放入 running list，若 ready
queue 為空且後面還有其他的 process 還沒進來，則繼續等待新的
process，否則表示該任務完成，使用 break 出迴圈，並回傳甘特圖及計算
每個 process 的 Waiting Time 及 Turnaround Time。
### 方法三：Shortest Job First (SJF) 
SJF 是根據最短的 CPU Burst Time 來排序的，為不可奪取的排程
法(Non-preemptive)，若 CPU Burst 相同，則根據 Arrival Time 和
Process ID 來決定先後順序。

其實作方式和方法一的 FCFS 很類似，差別只在於每當有新的 process
進來時要先根據其 CPU Burst 排序，CPU Burst 越小，會排在 ready queue
的越前面，先被處理。
### 方法四：Shortest Remaining Time First (SRTF) 
SRTF 是根據剩餘最短的 CPU Burst Time 來排序的，和方法三的 SJF
不同的地方在於，CPU Scheduling 需在每輪的 timer 檢查所有 process 中
剩餘最短的 CPU Burst Time 是哪個 process，為可奪取的排程法
(preemptive)。

其實作方式也和方法三很相似，差別在於每一輪的 timer 除了要檢查
running list 是否為空，以及是否為某個 process 做完的時間，還要比較
此時位於 running list 中的 process 的 CPU Burst Time 是否小於 ready 
queue 當中第一個 process 的 CPU Burst Time，若小於等於，則可以繼續
使用 CPU 資源；若大於，則需要換給下一個 CPU Burst Time 更小的
process 使用，原先的 process 加入到 ready queue，再根據 CPU Burst 
Time 排序。如此一來便可實現每輪皆由當下剩餘最短 CPU Burst Time 的
process 來取得 CPU 資源。
### 方法五：Height Response Time First (HRTF) 
HRTF 是根據反應時間比率(Response Ratio)來排序的，若 Response 
Ratio 相同，則依照 Arrival Time 和 Process ID 來決定先後順序。HRTF
為不可奪取(Non-preemptive)的排程法。

其實作方法和方法一類似，差別只在於每當一個 process 做完，要
CPU Scheduling 要選取下一個 process 時，要根據 ready queue 中
process 的反應時間比率來重新排序，選出 Response Ratio 最高的
process 作為下一個取得 CPU 資源的 process。
### 方法六：Preemptive Priority + RR (PPRR) 
PPRR 是結合 Preemptive Priority 以及 Round Robin，先依照
Priority 的優先順序排序，若有 Priority 相同的 process，則採用 RR 的
方式來輪流取得 CPU 資源。

其實作方式與方法二的 RR 相似，差別在於每輪 timer 還需要多比較此
時佔有 running list 的 process 的 Priority 是否優先權大於 ready 
queue 中排在第一位的 process，若 ready queue 當中 process 的
Priority 較小，則可以奪取 CPU 資源，原 process 則放回到 ready 
queue，並再根據 Priority 將 ready queue 排序好。
# 方法七：ALL 
方法七為方法一到六的集大成。
