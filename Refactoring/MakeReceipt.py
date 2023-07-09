import json
import math
import pprint

def statement(invoice, plays):

    def renderPlainText(statementData, plays):
        def playFor(aPerformance):
            return plays[aPerformance['playID']]

        def amountFor(aPerformance):
            result = 0

            if playFor(aPerformance)['type'] == "tragedy":
                result = 40000
                if aPerformance['audience'] > 30:
                    result += 1000 * (aPerformance['audience'] - 30)
            elif playFor(aPerformance)['type'] == "comedy":
                result = 30000
                if aPerformance['audience'] > 20:
                    result += 10000 + 500 * (aPerformance['audience'] - 20)
                result += 300 * aPerformance['audience']
            else:
                assert True, "Unknown genre : {:s}".format(playFor(aPerformance)['type'])
            return result

        def volumeCreditFor(aPerformance):
            result = 0
            # accumulating point
            result += max([aPerformance['audience'] - 30, 0])

            # give additional point per each 5 peoples
            if "comedy" == playFor(aPerformance)['type'] :
                result += math.floor(aPerformance['audience'] / 5)
            return result

        def usd(aNumber):
            return aNumber/100

        def getTotalVolumeCredits():
            result = 0
            for perf in statementData['performances']:
                result += volumeCreditFor(perf)
            return result

        def getTotalAmount():
            result = 0
            for perf in statementData['performances']:
                result += amountFor(perf)
            return result

        result = "bills (Name : {:s})\n".format(statementData['customer'])

        for perf in statementData['performances']:
            # show bills
            result += "\t{:15s} : $ {:7.2f} ({:3d} Seats)\n".format(playFor(perf)['name'], usd(amountFor(perf)), perf['audience']) 

        result += "Total : $ {:.2f}\n".format(usd(getTotalAmount()))
        result += "Accumulated point : {:.0f} points\n".format(getTotalVolumeCredits())
        print(result)
        return result
    
    # Main loop 
    STATEMENTDATA = {}
    STATEMENTDATA['customer']       = invoice['customer']
    STATEMENTDATA['performances']   = invoice['performances']
    return renderPlainText(STATEMENTDATA, plays)

def openJSON(fileName:str):
    with open(fileName) as f:
        result = json.load(f)
    # pprint.pprint(result)
    return result

if __name__ == "__main__":
    # Read json files
    invoices = openJSON('invoices.json')
    plays = openJSON("plays.json")
    receipt_text = statement(invoice=invoices, plays=plays)
    with open('result.txt','w') as f:
        f.write(receipt_text)
        f.close