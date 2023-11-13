from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/portfolio-operations', methods = ['POST'])
def user():
    finans = []
    if request.method == 'POST':
        
        data = request.json['inputs']
        print(data)
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
