import copy

def method1( lines, page, ans, pf, Page_Fault, Page_Replaces, Page_Frames ) :
    tmp = []
    for i in range ( len(lines) ):
        find = False
        for p in range ( len(page) ):
            if ( page[p] == lines[i] ) : 
                find = True
                pf[i] = True 

        if not find:
            Page_Fault += 1
                
            if len(page) != size: 
                Page_Frames += 1
                page.append( lines[i] )
            else: Page_Replaces += 1
                    
            for p in range ( len(page)-2, -1, -1 ):
                page[p+1] = page[p]

            page[0] = lines[i]

        tmp = copy.deepcopy( page )
        ans.append( tmp )
        pf.append( False )

    return ans, pf, Page_Fault, Page_Replaces, Page_Frames 

def method2( lines, page, ans, pf, Page_Fault, Page_Replaces, Page_Frames ) :
    tmp = []
    for i in range ( len(lines) ):
        find = False
        
        for p in range ( len(page) ):
            if ( page[p] == lines[i] ) : 
                find = True
                pf[i] = True 
                tmp = page[p]
                for j in range (p, -1, -1):
                    page[j] = page[j-1]

                page[0] = tmp

        if not find:
            Page_Fault += 1
                
            if len(page) != size: 
                Page_Frames += 1
                page.append( lines[i] )
                for p in range ( len(page)-2, -1, -1 ):
                    page[p+1] = page[p]

                page[0] = lines[i]
            else: 
                Page_Replaces += 1
                min = 0
                minpage = 0
                for p in range ( len(page) ):
                    for j in range( i, -1, -1 ):
                        if lines[j] == page[p] :
                            if min == 0 or j < min:
                                min = j
                                minpage = p
                            break 

                for j in range (int(minpage), -1, -1):
                    page[j] = page[j-1]

                page[0] = lines[i]
            
        tmp = copy.deepcopy( page )
        ans.append( tmp )
        pf.append( False )

    return ans, pf, Page_Fault, Page_Replaces, Page_Frames 

def method3_4( lines, page, ans, pf, Page_Fault, Page_Replaces, Page_Frames, method ) :
    tmp = []
    f = []
    for _ in range( len(lines)+1 ):
        f.append( 0 )
    
    for i in range ( len(lines) ):
        f[int(lines[i])] += 1
        find = False
        for p in range ( len(page) ):
            if ( page[p] == lines[i] ): 
                find = True
                pf[i] = True 

        if not find:
            Page_Fault += 1
                
            if len(page) != size: 
                Page_Frames += 1
                page.append( lines[i] )
                for p in range ( len(page)-2, -1, -1 ):
                    page[p+1] = page[p]

                page[0] = lines[i]
            else:   
                Page_Replaces += 1
                key = 0

                if method == 3:
                    min = 0
                     
                    for j in range( len(page) ):
                        if min == 0 or min >= f[int(page[j])] :
                            min = f[int(page[j])]
                            key = j
                    
                elif method == 4 : 
                    max = 0
                     
                    for j in range( len(page) ):
                        if max == 0 or max <= f[int(page[j])] :
                            max = f[int(page[j])]
                            key = j
                    
                f[int(page[key])] = 0
                for j in range (int(key), -1, -1):
                    page[j] = page[j-1]

                page[0] = lines[i]

        tmp = copy.deepcopy( page )
        ans.append( tmp )
        pf.append( False )

    return ans, pf, Page_Fault, Page_Replaces, Page_Frames 

def method5( lines, page, ans, pf, Page_Fault, Page_Replaces, Page_Frames ) :
    tmp = []
    f = []
    for _ in range( len(lines)+1 ):
        f.append( 0 )

    for i in range ( len(lines) ):
        find = False
        f[int(lines[i])] += 1

        for p in range ( len(page) ):
            if ( page[p] == lines[i] ) : 
                find = True
                pf[i] = True 
                tmp = page[p]
                for j in range (p, -1, -1):
                    page[j] = page[j-1]

                page[0] = tmp
        
        if not find:
            Page_Fault += 1
                
            if len(page) != size: 
                Page_Frames += 1
                page.append( lines[i] )
                for p in range ( len(page)-2, -1, -1 ):
                    page[p+1] = page[p]

                page[0] = lines[i]
            else: 
                Page_Replaces += 1

                key = 0
                min = 0
                     
                for j in range( len(page) ):
                    if min == 0 or min >= f[int(page[j])] :
                        min = f[int(page[j])]
                        key = j

                f[int(page[key])] = 0
                for j in range (int(key), -1, -1):
                    page[j] = page[j-1]

                page[0] = lines[i]
                
        tmp = copy.deepcopy( page )
        ans.append( tmp )
        pf.append( False )

    return ans, pf, Page_Fault, Page_Replaces, Page_Frames 

def HandleMethod( method, lines, six ):
    page = []
    ans = []
    pf = []
    for _ in range( len(lines)+1 ):
        pf.append( False )

    Page_Fault = 0
    Page_Replaces = 0
    Page_Frames = 0

    if method == 1:
        ans, pf, Page_Fault, Page_Replaces, Page_Frames  = method1( lines, page, ans, pf, Page_Fault, Page_Replaces, Page_Frames )
    elif method == 2:
        ans, pf, Page_Fault, Page_Replaces, Page_Frames  = method2( lines, page, ans, pf, Page_Fault, Page_Replaces, Page_Frames )
    elif method == 3:
        ans, pf, Page_Fault, Page_Replaces, Page_Frames  = method3_4( lines, page, ans, pf, Page_Fault, Page_Replaces, Page_Frames, method )
    elif method == 4:
        ans, pf, Page_Fault, Page_Replaces, Page_Frames = method3_4( lines, page, ans, pf, Page_Fault, Page_Replaces, Page_Frames, method )
    elif method == 5:
        ans, pf, Page_Fault, Page_Replaces, Page_Frames = method5( lines, page, ans, pf, Page_Fault, Page_Replaces, Page_Frames )

    WriteFile( fileName, ans, pf, Page_Fault, Page_Replaces, Page_Frames, method, six )
    return 
            
def ReadFile( fileName ):
    f = open( fileName, 'r' )
    temp = f.readline().split()
    method = int(temp[0])
    size = int(temp[1])

    temp = f.readline().rstrip()  # 讀取一行字串並移除換行符號
    lines = []
    for char in temp:
        lines.append( char )

    return method, size, lines

def WriteFile( fileName, ans, pf, Page_Fault, Page_Replaces, Page_Frames, method, six ):
    fileName = "out_" + fileName
    f = open( fileName, "a" )

    if method == 1:
        print('--------------FIFO-----------------------', file=f)
    elif method == 2:
        print('--------------LRU-----------------------', file=f)
    elif method == 3:
        print('--------------Least Frequently Used Page Replacement-----------------------', file=f)
    elif method == 4:
        print('--------------Most Frequently Used Page Replacement -----------------------', file=f)
    elif method == 5:
        print('--------------Least Frequently Used LRU Page Replacement-----------------------', file=f)
    
    for i in range( len(lines) ) :
        print( lines[i], end = '	', file=f ) 

        for j in range ( len(ans[i]) ) :
            print( ans[i][j], end = '', file=f )

        if size <= 3: 
            print( "\t", end = '', file=f )
        else: 
            if len(ans[i]) < 4:
                print( "\t\t", end = '', file=f )
            else:
                print( "\t", end = '', file=f )

        if pf[i] == False: print( "F", file=f )
        else: print( "", file=f )
    
    print( "Page Fault = %d  Page Replaces = %d  Page Frames = %d"  % (Page_Fault, Page_Replaces, Page_Frames), file=f)
    if six and method != 5:
        print( "", file=f )

if __name__ == '__main__':
    while 1:
        fileName = input( "請輸入檔案名稱:\n" )
        fileName = fileName + ".txt" ;

        method, size, lines = ReadFile( fileName )
        six = False
        if method == 6:
            six = True
            for i in range(5) :
                HandleMethod( i+1, lines, six )

        else: HandleMethod( method, lines, six )
