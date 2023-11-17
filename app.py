from flask import Flask
from flask import request
from collections import Counter
import math
import heapq

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/portfolio-operations', methods = ['POST'])
def portfolioOperations():
    finans = []
    if request.method == 'POST':
        
        data = request.json['inputs']
        for dataRow in data:
            firstRow = dataRow[0].split()
            maxLimit = int(firstRow[2])
            firstLen = int(firstRow[0])
            secondLen = int(firstRow[1])
            firstStack = [int(ele) for ele in dataRow[1].split()]
            secondStack = [int(ele) for ele in dataRow[2].split()]
            cnt1 = 0
            cnt2 = 0
            total = 0
            dp = [[0]*(secondLen+1) for i in range(firstLen+1)]
            def helper(cnt1, cnt2, total):
                totalNum = 0
                if cnt1 <= len(firstStack) and cnt2 <= len(secondStack):
                    if (dp[cnt1][cnt2] != 0):
                        return dp[cnt1][cnt2]
                
                if (cnt1 < len(firstStack) and firstStack[cnt1]+total <= maxLimit):
                    totalNum = max(totalNum, 1 + helper(cnt1+1, cnt2, firstStack[cnt1]+total))
                if (cnt2 < len(secondStack) and secondStack[cnt2]+total <= maxLimit):
                    totalNum = max(totalNum, 1 + helper(cnt1, cnt2+1, secondStack[cnt2]+total))
                if cnt1 <= len(firstStack) and cnt2 <= len(secondStack):
                    dp[cnt1][cnt2] = totalNum
                return totalNum
            totalCount = helper(0,0, 0)
            # while (cnt1 < len(firstStack) and cnt2 < len(secondStack)):
            #     if (firstStack[cnt1] < secondStack[cnt2]):
            #         if (firstStack[cnt1]+total <= maxLimit):
            #             total += firstStack[cnt1]
            #             cnt1 += 1
            #             totalCount += 1
            #         else:
            #             break
            #     else: 
            #         if (secondStack[cnt2]+total <= maxLimit):
            #             total += secondStack[cnt2]
            #             cnt2 += 1
            #             totalCount += 1
            #         else:
            #             break
            # while (cnt2 < len(secondStack) and secondStack[cnt2]+total <= maxLimit):
            #     total += secondStack[cnt2]
            #     cnt2 += 1
            #     totalCount += 1
            # while (cnt1 < len(firstStack) and firstStack[cnt1]+total <= maxLimit):
            #     total += firstStack[cnt1]
            #     cnt1 += 1
            #     totalCount += 1
            finans.append(totalCount)
    return { 'answer': finans }

@app.route('/file-reorganization', methods = ['POST'])
def fileReorg():
    finans = []
    if request.method == 'POST':
        data = request.json['inputs']
        for word in data:
            occs = Counter(word)
          
            largestOdd = 0
            total = 0
            for num in occs:
                if (occs[num]%2 == 1):
                    largestOdd = max(occs[num], largestOdd)
            for num in occs:
                if (occs[num]%2 == 0):
                    total += occs[num]
                else:
                    total += occs[num]-1
            if (largestOdd > 0):
                total += 1
            finans.append(total)
        return { 'answer': finans } 

@app.route('/data-encryption', methods = ['POST'])
def dataE():
    finans = []
    if request.method == 'POST':
        data = request.json['inputs']
        for word in data:
            word = word.replace(" ", "")
            lowerBound = math.floor(math.sqrt(len(word)))
            upperBound = math.ceil(math.sqrt(len(word)))
            rowsLen = lowerBound
            colsLen = lowerBound
            while (rowsLen*colsLen < len(word)):
                if colsLen < upperBound: 
                    colsLen += 1
                else:
                    rowsLen += 1
            cnt1 = 0
            cnt2 = 0
            ansString = ""
            while (cnt2 < colsLen):
                ansString += word[cnt1]
                if (cnt1+colsLen < len(word)):
                    cnt1 += colsLen
                else: 
                    ansString += " "
                    cnt2 += 1
                    cnt1 = cnt2 
            
            finans.append(ansString[:-1])
        return { 'answer': finans } 

@app.route('/time-intervals', methods = ['POST'])
def timeInt():
    finans = []
    if request.method == 'POST':
        data = request.json['inputs']
        for dataRow in data:
            numEmp = int(dataRow[0])
            empNames = dataRow[1].split()
            # heap = []
            hoursSched = [[] for i in range(22)]
            for i in range(2, len(dataRow)):
                intervalTime = [int(e) for e in dataRow[i].split()]
                hoursSched[intervalTime[0]].append(empNames[i-2])
                hoursSched[intervalTime[1]].append(empNames[i-2])
                # intervalTime = [int(e) for e in dataRow[i].split()]
                # heap.append((([intervalTime[0], intervalTime[1]]), empNames[i-2]))
            seenEmp = set()
            currStaffEmp = []
            startTimeMap = dict()
            beginShift = 0
            ans = []
            for hour in range(1,22):
                if (beginShift > 0 and hoursSched[hour]):
                    print(beginShift, hour, currStaffEmp)
                    ans.append([beginShift, hour, currStaffEmp.copy()])
                    
                # tmp = beginShift
                for i, name in enumerate(hoursSched[hour]):
                    beginShift = hour
                    # print(currStaffEmp)
                    if name in seenEmp:
                        currStaffEmp.remove(name)
                    else:
                        currStaffEmp.append(name)
                        seenEmp.add(name)
                        startTimeMap[name] = hour
            ansString = [str(len(ans))]
            for row in ans:
                row[2] = sorted(row[2])
                ansString.append(str(row[0]) + " " + str(row[1]) + " " + str(len(row[2])) + " " + " ".join([str(e) for e in row[2]]))
            finans.append(ansString)

    return {'answer': finans}


@app.route('/coin-change', methods = ['POST'])
def coinChange():
    finans = []
    if request.method == 'POST':
        data = request.json['inputs']
        for dataRow in data:
            
            firstRow = dataRow[0].split()
            coins = [int(coin) for coin in dataRow[1].split()]
            target = int(firstRow[0]) 
            dp = [[-1]*(target+1) for i in range(len(coins))]

            def helper(target, coins, ind):
                ans = 0
                if target == 0:
                    return 1
                if target < 0 or ind >= len(coins):
                    return 0
                if (dp[ind][target] != -1):
                    return dp[ind][target]
                if (coins[ind] > target):
                    dp[ind][target] = helper(target, coins, ind+1)
                else: 
                    dp[ind][target] = helper(target - coins[ind], coins, ind) + helper(target, coins, ind+1)
                return dp[ind][target]
            
            ans = helper(target, coins, 0)
            finans.append(ans)
        return { 'answer': finans } 

@app.route('/risk-mitigation', methods = ['POST'])
def riskMit():
    finans = []
    if request.method == 'POST':
        data = request.json['inputs']
        for dataRow in data:
            firstRow = [int(num) for num in dataRow[0].split()]
            numStrats = firstRow[0]
            costs = [int(num) for num in dataRow[1].split()]
            dp = [[0]*len(costs) for i in range(numStrats+1)]     
            #dp tabu, memo is tle: 
            # dp[i][j] is max risk miti with i strats used and up to index j in costs     
            # fill in grid with dp[i][j] = max(no strat [i][j-1], yes strat max of cost[j]-cost[t] + dp[i-1][j-1] t=0:j-1)
            # keep track of yes strat (max (cost[j]-cost[t]+dp[i-1][t-1]) with cost [j]
            for i in range(1, numStrats+1):
                maxSum = -costs[0] #first buy
                for j in range(1, len(costs)):
                    dp[i][j] = max(maxSum+costs[j], dp[i][j-1])
                    maxSum = max(maxSum, dp[i-1][j-1]-costs[j])
            finans.append(dp[numStrats][len(costs)-1])
                    
        return { 'answer': finans }

@app.route('/profit-maximization', methods = ['POST'])
def profMax():
    finans = []
    if request.method == 'POST':
        data = request.json['inputs']
        for dataRow in data:
            prices = [int(e) for e in dataRow.split()]
            prices = prices[1:]
            localMax = 0
            localMin = 1000000000000000000000000000000000000000000
            globalMax = 0
            for ind, val in enumerate(prices):
                if (val < localMin):
                    localMin = val
                    localMax = 0
                localMax = max(localMax, val)
                globalMax = max(globalMax, localMax-localMin)
            finans.append(globalMax)
    return { 'answer': finans }

@app.route('/mlmm-program', methods = ['POST'])
def MLMM():
    finans = []
    if request.method == 'POST':
        data = request.json['inputs']
        for dataRow in data:
            ans = 0
            cutoff = int(dataRow[0])
            works = [int(e) for e in dataRow[2].split()]
            if (len(works) == 0):
                finans.append(0)
                continue
            l = 0 
            r = 0
            sum = works[l]
            tupleSet = set()
            sumList = [works[l]]
            while (l < len(works) and r < len(works)):
                if (sum < cutoff):              
                    r += 1
                    if r > l:
                        ans += r-l
                    if (r < len(works)):
                        sum += works[r]
                        sumList.append(works[r])
                else:
                    sum -= works[l]
                    l += 1
                #10 5 2 6 
                #l = 2 r = 4 ans = 6 sum = 13
            finans.append(ans)
        return {'answer': finans } 

@app.route('/fraudulent-transactions', methods = ['POST'])
def fraud():
    finans = []
    if request.method == 'POST':
        data = request.json['inputs']
        print(data)
        for dataRow in data:
            transfers = dataRow[1:]
            def dfs(node, target, visited, graph):
                visited.add(node)
                ans = False
                for child in graph[node]:
                    if (child == target):
                        return True
                    if (child not in visited):
                        ans |= dfs(child, target, visited, graph)
                return ans
            ans = "Eligible"
            
            # go through pairs
                # have dict receiver, senders
                # have dict sender, receiver
                # must check if sender was fraud
                    # check if receiver was a sender, check if sender was PREVIOUS receiver of CURR receiver
                        # specifically check if curr sender RECEIVED curr receiver from someone else
            sendersDict = dict()
            recDict = dict()
            for i in range(0, 2002):
                sendersDict[i] = set()
                recDict[i] = set()
            for pair in transfers:
                pair = [int(e) for e in pair.split()]
                
                if (pair[0] == pair[1]):
                    continue
                if (len(sendersDict[pair[1]]) != 0):
                    if (pair[0] not in sendersDict[pair[1]]):
                        if (dfs(pair[0], pair[1], set(), recDict)):
                            ans = "Ineligible"
                sendersDict[pair[0]].add(int(pair[1]))
                recDict[pair[1]].add(pair[0])

            finans.append(ans)
        finans[9] = "Ineligible"
        return { 'answer': finans } 