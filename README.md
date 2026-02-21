# Page Replacement Simulator (FIFO / LRU / LFU / MFU / LFU+LRU)

這是一個用 **Python** 實作的「分頁置換（Page Replacement）」模擬器，能根據輸入檔案指定的方法與頁框（frame）大小，逐步模擬每次 page reference 後的記憶體頁框內容，並輸出每步是否發生 Page Fault，以及統計：
- **Page Fault**
- **Page Replaces**
- **Page Frames**

支援方法：
1. FIFO（First-In First-Out）
2. LRU（Least Recently Used）
3. LFU（Least Frequently Used）
4. MFU（Most Frequently Used）
5. LFU + LRU（同頻率時用 LRU 行為/並結合 LRU 的移動方式）
6. 一次輸出 1~5 全部方法（同一組輸入）

---

## 專案結構與輸出

### 輸入檔
程式會要求你輸入檔名（不含副檔名），並自動加上 `.txt` 讀取。

例如：
請輸入檔案名稱:
test

程式會讀取 `test.txt`

### 輸出檔
輸出檔名會自動加上 `out_` 前綴，並以 **append** 方式寫入：

- 輸入：`test.txt`
- 輸出：`out_test.txt`

> 注意：因為 `WriteFile()` 使用 `"a"` 模式（附加寫入），同一個輸出檔重跑會一直累加內容；若想每次重跑都重新產生，請自行刪除 `out_*.txt` 或把 `"a"` 改為 `"w"`。

---

## 輸入格式（Input Format）

輸入檔共兩行：

### 第 1 行：方法與頁框大小
格式：
```scheme
<method> <size>
```

- `method`: 1~6
- `size`: page frames 的容量（可放幾個頁）

範例：
```scheme
2 3
```

代表使用 LRU，page frame size = 3

### 第 2 行：reference string
程式會逐字元讀取這一行，把每個字元當作一次 page reference。

範例：
```scheme
70120304230321201701
```


---

## 執行方式（How to Run）

### 1) 直接執行
```bash
python main.py
```
### 2) 依提示輸入檔名（不含 .txt）
```scheme
請輸入檔案名稱:
test
```

---

## 輸出格式（Output Format）

輸出內容會先印出方法標題，接著每一行代表一次 reference：
- 左側：本次 reference 的 page（字元）
- 中間：目前頁框內容（由 `ans[i]` 印出）
- 右側：若發生 page fault，印 `F`

最後一行印統計：
```scheme
Page Fault = X  Page Replaces = Y  Page Frames = Z
```

---

## 各方法行為摘要（Algorithms）

這份程式的 page list 會經常把「最新加入/最新使用」的頁移到 page[0]，並用位移方式維護順序。

### (1) FIFO (`method1`)
- 命中：不動 page 順序
- 缺頁：
  - 若 frame 未滿：直接加入
  - 若 frame 已滿：視為替換（Page_Replaces +1）
- 無論缺頁或加入，都會把新頁放到 `page[0]`，其餘往後推

### (2) LRU (`method2`)
- 命中：把該頁移到最前面（`page[0]`）
- 缺頁：
  - frame 未滿：加入並放最前
  - frame 已滿：從過去 reference 中找出「最久沒被用到」的頁進行替換（透過回掃 lines 找最小的最後出現位置）

### (3) LFU (`method3_4` with method==3)
- 維護 `f[]`：記錄每個 page 出現次數（以 `int(lines[i])` 當 index）
- 缺頁且 frame 已滿：
  - 找 frame 內使用次數最少的頁替換
  - 被替換頁的次數會被重設為 0

### (4) MFU (`method3_4` with method==4)
- 與 LFU 類似，但替換「使用次數最多」的頁

### (5) LFU + LRU (`method5`)
- 也維護 `f[]` 次數
- 命中：同 LRU，把命中頁移到最前
- 缺頁且 frame 已滿：以 LFU 找出最少使用次數的頁替換（並重設其計數），新頁放最前
