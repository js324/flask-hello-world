from flask import Flask
from flask import request
from collections import Counter
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
            firstStack = [int(ele) for ele in dataRow[1].split()]
            secondStack = [int(ele) for ele in dataRow[2].split()]
            cnt1 = 0
            cnt2 = 0
            total = 0
            totalCount = 0
            while (cnt1 < len(firstStack) and cnt2 < len(secondStack)):
                if (firstStack[cnt1] < secondStack[cnt2]):
                    if (firstStack[cnt1]+total <= maxLimit):
                        total += firstStack[cnt1]
                        cnt1 += 1
                        totalCount += 1
                    else:
                        break
                else: 
                    if (secondStack[cnt2]+total <= maxLimit):
                        total += secondStack[cnt2]
                        cnt2 += 1
                        totalCount += 1
                    else:
                        break
            while (cnt2 < len(secondStack) and secondStack[cnt2]+total <= maxLimit):
                total += secondStack[cnt2]
                cnt2 += 1
                totalCount += 1
            while (cnt1 < len(firstStack) and firstStack[cnt1]+total <= maxLimit):
                total += firstStack[cnt1]
                cnt1 += 1
                totalCount += 1
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

                