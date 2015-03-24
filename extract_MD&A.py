#scan all the 10ks in the same folder and extract MD&A

from os import listdir
from os.path import isfile, join
import urllib
from HTMLParser import HTMLParser
import re, math

#I/O
def fileList():
    files = [ f for f in listdir('./') if isfile(join('./',f)) and f.endswith('.htm') ]
    return files

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def scan(filename, debug = False):
    page = urllib.urlopen(filename)
    text = strip_tags(page.read()).lower()

    #split by  keyword item
    t = text.split("item")

    if debug:
        print [len(s) for s in t]

    #select the start point
    idx = []
    for i in range(len(t)):
        if re.match('^7[^a]', t[i].strip()):
            idx.append(i)

    if debug:
        print 'count of "item 7": %d' % len(idx)

    #select the end point
    results = []
    for i in idx:
        res = t[i]
        endPoint = i+1

        isValid = 0
        
        while endPoint < len(t):
            if re.match('^[7][a]', t[endPoint].strip()):
                if t[endPoint][0:100].find('quantitative') >= 0 and t[endPoint][0:100].find('qualitative') >= 0:
                    isValid = 1
                    break
            res = ' '.join((res, t[endPoint]))
            endPoint += 1

        if (len(res) < 10000):
            isValid = 0

        if res[0:100].find('discussion') < 0 and res[0:100].find('analysis') < 0:
            isValid = 0

        if isValid:
            results.append(res)

    if debug:
        print [len(s) for s in results]

    #selecting the best answer
    if len(results) > 0:
        score = [0 for i in range(len(results))]
        meanOfLength = sum([len(s) for s in results])/len(results)
        for i in range(len(results)):
            if results[i].find('discussion') > -1:
                score[i] += 1
            if results[i].find('analysis') > -1:
                score[i] += 1
            if results[i].find('unaudited') > -1:
                score[i] += 1
            if results[i].find('forward looking') > -1:
                score[i] += 1
            if results[i].find('critical accounting') > -1:
                score[i] += 1
            if results[i][100:len(results[i])].find('7. managements discussion and analysis') >= 0:
                score[i] -= 3
            #length penalty
            score[i] -= math.log(abs(len(results[i]) - 80000), 10) / float(3)

        if debug:
            print 'scores: %s' % ['%3.3f' % score[i] for i in range(len(results))]
            
        best_result = results[0]
        best_score = - float("Inf")
        for i in range(len(results)):
            if score[i] > best_score:
                best_result = results[i]
                best_score = score[i]

        print 'MD&A score of %s: %d, length %d' % (filename, best_score, len(best_result))

        with open('./MD&A/%s.MD&A.txt' % filename.rstrip('.htm'), 'w') as outfile:
            outfile.write(best_result)
    else:
        raise Exception('no result found')

if __name__ == "__main__":
    fileList = fileList()

    failureLog = []
    for f in fileList:
        try:
            scan(f)
        except:
            failureLog.append(f)
            print 'Error! %s' % f

     #scan('MEREDITH CORP-08-24-2011.htm', True)
