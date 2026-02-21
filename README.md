# CPU Scheduling Simulator

這份程式是一個 **CPU 排程演算法模擬器**，可讀取指定格式的輸入檔（`.txt`），依照選擇的排程方法模擬 CPU 執行流程（甘特圖），並輸出每個行程（process）的 **Waiting Time** 與 **Turnaround Time** 到 `out_檔名.txt`。

---

## 功能總覽

支援以下排程演算法：

- **FCFS (First Come First Serve)**：先到先服務（非搶占）
- **RR (Round Robin)**：時間片輪轉（搶占，需 time slice）
- **SJF (Shortest Job First)**：最短工作優先（非搶占）
- **SRTF (Shortest Remaining Time First)**：最短剩餘時間優先（搶占）
- **HRRN (Highest Response Ratio Next)**：最高回應比優先（非搶占）
- **PPRR (Priority Round Robin)**：具優先權的 RR（搶占，需 time slice）
- **All (method = 7)**：一次輸出上述 6 種演算法結果

---

## 程式流程

1. 從輸入檔讀取：
   - `method`：排程方法代號
   - `timeSlice`：RR/PPRR 使用的時間片
   - process 資料：`[PID, CPU Burst, Arrival Time, Priority]`
2. 依 `method` 呼叫對應演算法產生：
   - `result`：甘特圖（每個時間單位 CPU 正在跑的 PID）
   - `ans`：每個 PID 的 turnaround / waiting 結果
3. 將結果寫入 `out_檔名.txt`

---

## 輸入檔格式

輸入檔副檔名為 `.txt`，檔案內容格式如下：

### 第 1 行
```scheme
<method> <timeSlice>
```

- `method`：1~7
- `timeSlice`：RR / PPRR 使用；若不是 RR/PPRR 仍需給一個整數（可填 0 或任意值）

### 第 2 行
表頭（程式會讀掉，不影響）
```scheme
ID CPU Burst Arrival Time Priority
```

### 第 3 行起：每個 process 一行
```scheme
<PID> <CPU_Burst> <Arrival_Time> <Priority>
```

#### 範例
```scheme
2 3
ID CPU Burst Arrival Time Priority
1 5 0 2
2 3 1 1
3 8 2 3
```

---

## 方法代號對照表

| method | 演算法 |
|-------:|--------|
| 1 | FCFS |
| 2 | RR |
| 3 | SJF |
| 4 | SRTF |
| 5 | HRRN |
| 6 | PPRR (Priority RR) |
| 7 | All（一次輸出 FCFS/RR/SJF/SRTF/HRRN/PPRR） |

---

## 輸出說明

輸出檔名固定為：

- `out_<原本輸入檔名>.txt`

內容包含：

1. **甘特圖（Gantt Chart）**
   - 每個時間單位輸出一個字元（由 PID 映射而來）
   - 程式使用 `serial` 將數字 PID 轉成 `0-9A-Z-` 等字元
   - 當 CPU idle 時，程式使用 `36`，映射成 `'-'`

2. **Waiting Time**
3. **Turnaround Time**

若 `method = 7`，會依序印出 6 種排程方法的甘特圖與綜合表格（Waiting/Turnaround）。

---

## 執行方式

確保你的環境有 Python 3。

```bash
python main.py
```

程式會提示你輸入檔名（不含 .txt）：

```scheme
請輸入檔案名稱:
input
```

程式會自動讀取 `input.txt`，並輸出 `out_input.txt`。

---

## 資料結構約定（process row）

程式使用 list 表示每個 process：

- `row[0]`：PID
- `row[1]`：CPU Burst（在 SRTF/RR/PPRR 會被遞減；原始值會暫存）
- `row[2]`：Arrival Time
- `row[3]`：Priority（PPRR 使用，數字越小代表優先權越高）
- `row[4]`：Finish Time（程式後續補上，初始為 -1；HRRN 時也會暫作 ratio 欄位）

---

## 主要函式簡介

- `Non_preemptive(data, method)`
  - 處理 **FCFS / SJF / HRRN**（非搶占）

- `SRTF(data)`
  - 處理 **SRTF**（搶占）

- `RR(data, timeSlice)`
  - 處理 **RR**（搶占 + time slice）

- `PPRR(data, timeSlice)`
  - 處理 **Priority RR**（優先權搶占 + time slice）

- `ReadFile(fileName)` /` WriteFile(...)` / `WriteFile_7(...)`
  - 負責 I/O

- `HandleMethod(data, method, timeSlice)`
  - 統一分派 method 與輸出格式處理
