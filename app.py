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
            print(occs)
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
            heap = []
            for i in range(2, len(dataRow)):
                intervalTime = dataRow[i].split()
                heapq.heappush(heap, ([intervalTime[0], dataRow[i][1]], empNames[i-2]))
            print(heap)



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

                