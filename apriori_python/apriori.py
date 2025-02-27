from csv import reader
from collections import defaultdict
from itertools import chain, combinations
from optparse import OptionParser
from apriori_python.utils import *
import time
import matplotlib.pyplot as plt

def apriori(itemSetList, minSup, minConf):
    C1ItemSet = getItemSetFromList(itemSetList)
    # Final result global frequent itemset
    globalFreqItemSet = dict()
    # Storing global itemset with support count
    globalItemSetWithSup = defaultdict(int)

    L1ItemSet = getAboveMinSup(
        C1ItemSet, itemSetList, minSup, globalItemSetWithSup)
    currentLSet = L1ItemSet
    k = 2

    # Calculating frequent item set
    while(currentLSet):
        # Storing frequent itemset
        globalFreqItemSet[k-1] = currentLSet
        # Self-joining Lk
        candidateSet = getUnion(currentLSet, k)
        # Perform subset testing and remove pruned supersets
        candidateSet = pruning(candidateSet, currentLSet, k-1)
        # Scanning itemSet for counting support
        currentLSet = getAboveMinSup(
            candidateSet, itemSetList, minSup, globalItemSetWithSup)
        k += 1

    rules = associationRule(globalFreqItemSet, globalItemSetWithSup, minConf)
    rules.sort(key=lambda x: x[2])

    return globalFreqItemSet, rules

def aprioriFromFile(fname, minSup, minConf):
    C1ItemSet, itemSetList = getFromFile(fname)

    # Final result global frequent itemset
    globalFreqItemSet = dict()
    # Storing global itemset with support count
    globalItemSetWithSup = defaultdict(int)

    L1ItemSet = getAboveMinSup(
        C1ItemSet, itemSetList, minSup, globalItemSetWithSup)
    currentLSet = L1ItemSet
    k = 2

    # Calculating frequent item set
    while(currentLSet):
        # Storing frequent itemset
        globalFreqItemSet[k-1] = currentLSet
        # Self-joining Lk
        candidateSet = getUnion(currentLSet, k)
        # Perform subset testing and remove pruned supersets
        candidateSet = pruning(candidateSet, currentLSet, k-1)
        # Scanning itemSet for counting support
        currentLSet = getAboveMinSup(
            candidateSet, itemSetList, minSup, globalItemSetWithSup)
        k += 1
    rules = None
    #rules = associationRule(globalFreqItemSet, globalItemSetWithSup, minConf)
    #rules.sort(key=lambda x: x[2])

    return globalFreqItemSet, rules

def graph(options):
    print(int(options.minSup))
    print(int(options.minConf))
    x = []
    y = []
    for i in range(10, int(options.minSup), 10):
        start_time = time.time()
        aprioriFromFile(options.inputFile, i, options.minConf)
        x.append(i)
        y.append((time.time() - start_time))
    print(x)
    print(y)
    plt.plot(x, y, 'k-', marker='o', lw=0.5)
    plt.xlabel('Support threshold')
    plt.ylabel('Runtime (sec)')
    plt.grid(color='black', linestyle='-', linewidth=0.09)
    plt.title('Time against support threshold')
    print("Done")
    plt.show()


if __name__ == "__main__":
    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                         dest='inputFile',
                         help='CSV filename',
                         default=None)
    optparser.add_option('-s', '--minSupport',
                         dest='minSup',
                         help='Min support (float)',
                         default=0.5,
                         type='float')
    optparser.add_option('-c', '--minConfidence',
                         dest='minConf',
                         help='Min confidence (float)',
                         default=0.5,
                         type='float')

    (options, args) = optparser.parse_args()
    #graph(options)
    freqItemSet, rules = aprioriFromFile(options.inputFile, options.minSup, options.minConf)
    print(freqItemSet)