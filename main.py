import queue

def Cal_ratio(empty, ready, timer):
    tmp = 0.0
    readylist = list(ready.queue)
    for i in range( len(readylist) ): 
        cpuBrust = readylist[i][1]
        if empty: waitime = 0
        else:  waitime = timer - readylist[i][2]

        tmp = ( waitime + cpuBrust ) / cpuBrust
        readylist[i][4] = tmp

    readylist = sorted(readylist, key=lambda x: (-x[4], x[2], x[0])) # 按造cpu brust / PID 進行排序
    for elem in readylist:
        ready.get()
        ready.put( elem ) # 將按cpu brust排序過的list放進去

def Non_preemptive( data, method ) : # FCFS(1)、SJF(3)、HRRN(5)
    ready = queue.Queue()
    running = [] # 正在執行的process
    result = []
    working = -1
    start = 0
    timer = 0
    cur = 0
    while 1 :
        while cur != len(data) and timer == data[cur][2] : # timer為某個process到的時間
            ready.put( data[cur] )
            cur = cur + 1         # process可以往後走一格
            
            if method == 3:
                readylist = sorted(list(ready.queue), key=lambda x: (x[1], x[2], x[0])) # 按造cpu brust 排序
                for elem in readylist:
                    ready.get()       # 刪除舊的
                    ready.put( elem ) # 將按cpu brust排序過的list放進去
            
        if len( running ) == 0 :      # 如果running裡面沒有process
            if method == 5:
                Cal_ratio( True, ready, timer )
            if ready.empty() == False: # ready queue不為空
                running = ready.get()  # 取得下一個process
                start = timer          # 記錄此process開始工作的timer
                working = running[0]   # 紀錄此時正在工作的人

            else: working = 36         # ready為空
                
        elif timer == start + running[1] : # timer為某個process做完的時間
            running = running[:0]
            for k in range( len( data ) ) : 
                if data[k][0] == working : # 找到完成工作的process
                    data[k][4] = timer     # 並記錄完成的時間
      
            if ready.empty() and cur == len(data) :
                break
            if ready.empty() :  # 沒有人正在等待cpu資源
                working = 36    # 表示此時cpu不需要處理process
            else :
                if method == 5:
                    Cal_ratio( False, ready, timer )
                
                running = ready.get() # 取得下一個process
                start = timer         # 記錄此process開始工作的timer
                working = running[0]  # 紀錄此時正在工作的人

        timer = timer + 1 
        result.append( working ) # 將甘特圖加上該process

    ans = []
    for i in range( len(data) ) :
        temp = []
        temp.append( data[i][0] )
        temp.append( data[i][4] - data[i][2] ) # turnaround time
        temp.append( temp[1] - data[i][1] )    # waiting time
        ans.append( temp )

    ans = sorted( ans, key=lambda x:(x[0]) )  # ans按造 PID 進行排序
    return result, ans            

def SRTF( data ) :                   # SRTF
    ready = queue.Queue()
    running = [] # 正在執行的process
    result = []
    working = -1
    timer = 0
    cur = 0
    while 1 :
        while cur != len(data) and timer == data[cur][2] : # timer為某個process到的時間
            data[cur][4] = data[cur][1] # 把cpu time存起來
            ready.put( data[cur] )
            cur = cur + 1               # process可以往後走一格

            readylist = sorted(list(ready.queue), key=lambda x: (x[1], x[2], x[0])) # 按cpu brust/Arrival/PID 排序
            for elem in readylist:
                ready.get()       # 刪除舊的
                ready.put( elem ) # 將按cpu brust排序過的list放進去


        if len( running ) == 0 :        # 如果running裡面沒有process
            if ready.empty() == False:  # ready queue不為空
                running = ready.get()   # 取得下一個process
                working = running[0]    # 紀錄此時正在工作的人

            else: working = 36          # ready為空

        elif running[1] == 0 :          # 某個process做完 
            running = running[:0]
            for k in range( len( data ) ) : 
                if data[k][0] == working :  # 找到完成工作的process
                    data[k][1] = data[k][4] # 把正確的cpu_burst存回去
                    data[k][4] = timer      # 並記錄完成的時間
      
            if ready.empty() and cur == len(data) :
                break
            if ready.empty() :  # 沒有人正在等待cpu資源
                working = 36    # 表示此時cpu不需要處理process
            else :     
                running = ready.get() # 取得下一個process
                working = running[0]  # 紀錄此時正在工作的人

        elif ready.qsize() != 0:
            tmp = ready.get()
            if running[1] > tmp[1]:
                ready.put( running )   # 把正在執行的人放回去
                readylist = sorted(list(ready.queue), key=lambda x: (x[1], x[2], x[0])) # 按cpu brust/Arrival/PID 排序
                for elem in readylist:
                    ready.get()        # 刪除舊的
                    ready.put( elem )  # 將按cpu brust排序過的list放進去

                running = tmp          # 取得下一個process
                working = running[0]   # 紀錄此時正在工作的人
            else:
                size = ready.qsize()
                tmp_ready = queue.Queue()
                tmp_ready.put( tmp )      # 把原本取出來的人放回去
                for _ in range( size ) :
                    if ready.empty() == False:
                        tmp = ready.get()
                        tmp_ready.put( tmp )      # 把原本取出來的人放回去

                readylist = sorted(list(tmp_ready.queue), key=lambda x: (x[1], x[2], x[0])) # 按cpu brust/Arrival/PID 排序
                while not ready.empty():
                    ready.get()
                for elem in readylist:
                    ready.put( elem ) # 將按cpu brust排序過的list放進去

        timer = timer + 1 
        if len( running ) != 0:
            running[1] = running[1] - 1
        result.append( working ) # 將甘特圖加上該process

    ans = []
    for i in range( len(data) ) :
        temp = []
        temp.append( data[i][0] )
        temp.append( data[i][4] - data[i][2] ) # turnaround time
        temp.append( temp[1] - data[i][1] )    # waiting time
        ans.append( temp )

    ans = sorted( ans, key=lambda x:(x[0]) )  # ans按造 PID 進行排序
    return result, ans    

def RR( data, timeSlice ) :          # RR
    ready = queue.Queue()
    running = [] # 正在執行的process
    result = []
    working = -1
    timer = 0
    slice = timeSlice
    cur = 0
    while 1 :
        while cur != len(data) and timer == data[cur][2] : # timer為某個process到的時間
            data[cur][4] = data[cur][1] # 把cpu time存起來
            ready.put( data[cur] )
            cur = cur + 1               # process可以往後走一格
            
        if len( running ) == 0 :        # 如果running裡面沒有process
            if ready.empty() == False:  # ready queue不為空
                slice = timeSlice
                running = ready.get()   # 取得下一個process
                working = running[0]    # 紀錄此時正在工作的人

            else: working = 36          # ready為空

        elif running[1] == 0 or slice == 0:  # 某個process做完 / timeout
            if running[1] == 0 :        # 做完
                running = running[:0]
                for k in range( len( data ) ) : 
                    if data[k][0] == working :  # 找到完成工作的process
                        data[k][1] = data[k][4] # 把正確的cpu_burst存回去
                        data[k][4] = timer      # 並記錄完成的時間

            elif slice == 0:            # timeout
                ready.put( running ) 

            if ready.empty() and cur == len(data) :
                break
            if ready.empty() :          # 沒有人正在等待cpu資源
                working = 36            # 表示此時cpu不需要處理process
            else :     
                slice = timeSlice
                running = ready.get()   # 取得下一個process
                working = running[0]    # 紀錄此時正在工作的人

        timer = timer + 1 
        if len( running ) != 0 :
            running[1] = running[1] - 1
            slice = slice - 1
        result.append( working )        # 將甘特圖加上該process

    ans = []
    for i in range( len(data) ) :
        temp = []
        temp.append( data[i][0] )
        temp.append( data[i][4] - data[i][2] ) # turnaround time
        temp.append( temp[1] - data[i][1] )    # waiting time
        ans.append( temp )

    ans = sorted( ans, key=lambda x:(x[0]) )  # ans按造 PID 進行排序
    return result, ans    

def PPRR( data, timeSlice ) :        # PPRR
    ready = queue.Queue()
    running = [] # 正在執行的process
    result = []
    working = -1
    timer = 0
    slice = timeSlice
    cur = 0
    while 1 :
        while cur != len(data) and timer == data[cur][2] : # timer為某個process到的時間
            data[cur][4] = data[cur][1]  # 把cpu time存起來
            ready.put( data[cur] )
            cur = cur + 1                # process可以往後走一格

            readylist = sorted(list(ready.queue), key=lambda x: (x[3])) # 按priority排序
            for elem in readylist:
                ready.get()       # 刪除舊的
                ready.put( elem ) # 將按cpu brust排序過的list放進去
            
        if len( running ) == 0 :  # 如果running裡面沒有process
            slice = timeSlice
            if ready.empty() == False:   # ready queue不為空
                running = ready.get()    # 取得下一個process
                working = running[0]     # 紀錄此時正在工作的人

            else: working = 36           # ready為空

        elif running[1] == 0 or slice == 0:  # 某個process做完 / timeout
            if running[1] == 0 :     # 做完
                running = running[:0]
                for k in range( len( data ) ) : 
                    if data[k][0] == working :  # 找到完成工作的process
                        data[k][1] = data[k][4] # 把正確的cpu_burst存回去
                        data[k][4] = timer      # 並記錄完成的時間

            elif slice == 0:  # timeout
                ready.put( running ) 
                readylist = sorted(list(ready.queue), key=lambda x: (x[3])) # 按priority 排序
                while not ready.empty():
                    ready.get()
                for elem in readylist:
                    ready.put( elem ) # 將按cpu brust排序過的list放進去
    
            if ready.empty() and cur == len(data) : 
                break
            elif ready.empty() :  # 沒有人正在等待cpu資源
                working = 36    # 表示此時cpu不需要處理process
            else :     
                slice = timeSlice
                running = ready.get() # 取得下一個process
                working = running[0]  # 紀錄此時正在工作的人
        
        elif len( running ) != 0 and ready.empty() == False:
            tmp = ready.get()
            if running[3] > tmp[3]:
                ready.put( running )     # 把正在執行的人放回去
                readylist = sorted(list(ready.queue), key=lambda x: (x[3])) # 按priority排序
                for elem in readylist:
                    ready.get()          # 刪除舊的
                    ready.put( elem )    # 將按cpu brust排序過的list放進去

                slice = timeSlice
                running = tmp            # 取得下一個process
                working = running[0]     # 紀錄此時正在工作的人

            else:
                size = ready.qsize()
                tmp_ready = queue.Queue()
                tmp_ready.put( tmp )     # 把原本取出來的人放回去
                for _ in range( size ) :
                    if ready.empty() == False:
                        tmp = ready.get()
                        tmp_ready.put( tmp )   

                readylist = sorted(list(tmp_ready.queue), key=lambda x: (x[3])) # 按priority排序
                while not ready.empty():
                    ready.get()
                for elem in readylist:
                    ready.put( elem )     # 將按cpu brust排序過的list放進去

        timer = timer + 1 
        if len( running ) != 0 :
            running[1] = running[1] - 1
            slice = slice - 1 
        result.append( working ) # 將甘特圖加上該process

    ans = []
    for i in range( len(data) ) :
        temp = []
        temp.append( data[i][0] )
        temp.append( data[i][4] - data[i][2] ) # turnaround time
        temp.append( temp[1] - data[i][1] )    # waiting time
        ans.append( temp )

    ans = sorted( ans, key=lambda x:(x[0]) )  # ans按造 PID 進行排序
    return result, ans    

def HandleMethod( data, method, timeSlice ):
    result = []
    ans = []
    data = sorted( data, key=lambda x:(x[2], x[0]) )  # 按造arrival time / PID 進行排序

    if method == 1:
        result, ans = Non_preemptive( data, method )
    
    elif method == 2:
        result, ans = RR( data, timeSlice )

    elif method == 3:
        result, ans = Non_preemptive( data, method )

    elif method == 4:
        result, ans = SRTF( data )

    elif method == 5:
        result, ans = Non_preemptive( data, method )

    elif method == 6:
        result, ans = PPRR( data, timeSlice )

    elif method == 7:
        tmp_result = []
        tmp_ans = []
        tmp_result, tmp_ans = Non_preemptive( data, 1 )
        result.append( tmp_result )
        ans.append( tmp_ans )

        tmp_result, tmp_ans = RR( data, timeSlice )
        result.append( tmp_result )
        ans.append( tmp_ans )

        tmp_result, tmp_ans = Non_preemptive( data, 3 )
        result.append( tmp_result )
        ans.append( tmp_ans )

        tmp_result, tmp_ans = SRTF( data )
        result.append( tmp_result )
        ans.append( tmp_ans )

        tmp_result, tmp_ans = Non_preemptive( data, 5 )
        result.append( tmp_result )
        ans.append( tmp_ans )

        tmp_result, tmp_ans = PPRR( data, timeSlice )
        result.append( tmp_result )
        ans.append( tmp_ans )
        
    serial = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H',
              'I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','-']
    
    if method != 7:
        for i in range( len(result) ) :
            result[i] = serial[result[i]]
    else:
        for i in range( len(result) ) :
            for j in range( len(result[i]) ) :
                result[i][j] = serial[result[i][j]]
    return result, ans

def ReadFile( fileName ):
    f = open( fileName, 'r' )
    
    temp = f.readline().split()
    method = int(temp[0])
    timeSlice = int(temp[1])

    temp = f.readline()  # 讀掉 ID  CPU Burst...
    data = []
    for line in f:
        templist = line.split()
        row = []
        if len(templist) != 0:
            for a in templist:    
                a=int(a)
                row.append(a)
        
            row.append(-1) # 之後用來紀錄finish時間
            data.append(row)

    f.close()
    return data, method, timeSlice

def WriteFile( fileName, method, result, ans ):
    fileName = "out_" + fileName
    f = open( fileName, "w" )

    if method == 1 : methodName = 'FCFS'
    elif method == 2 : methodName = 'RR'  
    elif method == 3 : methodName = 'SJF'
    elif method == 4 : methodName = 'SRTF'
    elif method == 5 : methodName = 'HRRN'
    elif method == 6 : methodName = 'PPRR'

    if method != 6:
        print( '%s' % methodName, file = f )
    else:
        tmp = 'Priority RR'
        print( '%s' % tmp, file = f )

    print( '==%12s==' % methodName, file = f )
    result = ''.join(result)
    print( str(result), file = f )
    print( '===========================================================', file = f )
    print( '', file = f )
    print( 'Waiting Time', file = f )
    print( 'ID\t%s' %  methodName, file = f )
    print( '===========================================================', file = f )
    for i in range( len(ans) ) :
        print( '%d\t%d' %( ans[i][0], ans[i][2] ), file = f )
    print( '===========================================================', file = f )
    print( '', file = f )
    print( 'Turnaround Time', file = f )
    print( 'ID\t%s' %  methodName, file = f )
    print( '===========================================================', file = f )
    for i in range( len(ans) ) :
        print( '%d\t%d' %( ans[i][0], ans[i][1] ), file = f )
    print( '===========================================================', file = f )
    print( '', file = f )
    f.close()

def WriteFile_7( fileName, result, ans ):
    fileName = "out_" + fileName
    f = open( fileName, "w" )
    print( 'All', file = f )

    for i in range( len(result) ) :
        if i == 0 : methodName = 'FCFS'
        elif i == 1 : methodName = 'RR'  
        elif i == 2 : methodName = 'SJF'
        elif i == 3 : methodName = 'SRTF'
        elif i == 4 : methodName = 'HRRN'
        elif i == 5 : methodName = 'PPRR'
        print( '==%12s==' % methodName, file = f )
        result[i] = ''.join(result[i])
        print( str(result[i]), file = f )

    print( '===========================================================', file = f )
    print( '', file = f )
    print( 'Waiting Time', file = f )
    print( 'ID\tFCFS\tRR\tSJF\tSRTF\tHRRN\tPPRR', file = f )
    print( '===========================================================', file = f )
    
    for i in range( len(ans[0]) ) :
        print( '%d' % ans[0][i][0], end = '', file = f )
        for j in range( 6 ):
            print( '\t%d' % ans[j][i][2], end = '', file = f )

        print( '', file = f )

    print( '===========================================================', file = f )
    print( '', file = f )
    print( 'Turnaround Time', file = f )
    print( 'ID\tFCFS\tRR\tSJF\tSRTF\tHRRN\tPPRR', file = f )
    print( '===========================================================', file = f )

    for i in range( len(ans[0]) ) :
        print( '%d' % ans[1][i][0], end = '', file = f )
        for j in range( 6 ):
            print( '\t%d' % ans[j][i][1], end = '', file = f )

        print( '', file = f )
    print( '===========================================================', file = f )
    print( '', file = f )
    f.close()

if __name__ == '__main__':
    while 1:
        fileName = input( "請輸入檔案名稱:\n" )
        fileName = fileName + ".txt" ;

        data, method, timeSlice = ReadFile( fileName )
        result, ans = HandleMethod( data, method, timeSlice )
        if method == 7:
            WriteFile_7( fileName, result, ans )
        else: WriteFile( fileName, method, result, ans )
