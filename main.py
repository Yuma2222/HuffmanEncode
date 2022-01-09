class HuffmanLeaf:
    def __init__(self, frequency, symbol, left=None, right=None):
        self.frequency = frequency
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = ''


def Heapify(arr, lowest, size):
    theSmallestOne = lowest
    leftChild = 2 * lowest + 1
    rightChild = 2 * lowest + 2

    if leftChild < size and arr[leftChild].frequency < arr[theSmallestOne].frequency:
        theSmallestOne = leftChild
    if rightChild < size and arr[rightChild].frequency < arr[theSmallestOne].frequency:
        theSmallestOne = rightChild

    if theSmallestOne != lowest:
        arr[lowest], arr[theSmallestOne] = arr[theSmallestOne], arr[lowest]
        Heapify(arr, theSmallestOne, size)


def HeapSort(arr):
    for i in range(len(arr) // 2 - 1, -1, -1):
        Heapify(arr, i, len(arr))

    for i in range(len(arr) - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        Heapify(arr, 0, i)


def countFrequency(file):
    frequencyDictionary = {}
    for char in open(file, 'r').read():
        if char in frequencyDictionary:
            frequencyDictionary[char] += 1
        else:
            frequencyDictionary[char] = 1
    return frequencyDictionary


def createNewTree(file):
    frequency = countFrequency(file)
    ourLeaves = []

    for k, v in frequency.items():
        ourLeaves.append(HuffmanLeaf(v, k))

    while len(ourLeaves) > 1:
        HeapSort(ourLeaves)

        left = ourLeaves[len(ourLeaves) - 1]
        left.code = 0
        ourLeaves.remove(left)

        right = ourLeaves[len(ourLeaves) - 2]
        right.code = 1
        ourLeaves.remove(right)

        newLeaf = HuffmanLeaf(left.frequency + right.frequency, left.symbol + right.symbol, left, right)
        ourLeaves.append(newLeaf)

    return ourLeaves


def addDictionary(ourLeaf, value=''):
    if ourLeaf.left:
        addDictionary(ourLeaf.left, value + str(ourLeaf.code))

    if ourLeaf.right:
        addDictionary(ourLeaf.right, value + str(ourLeaf.code))

    if not ourLeaf.left and not ourLeaf.right:
        open("output.txt", 'a').writelines(ourLeaf.symbol + ":" + value + str(ourLeaf.code) + "\n")


def EncodeFile(ourLeaf, value, file):
    if ourLeaf is None:
        return file
    if ourLeaf:
        if len(ourLeaf.symbol) <= 1:
            file = file.replace(ourLeaf.symbol, value)
    file = EncodeFile(ourLeaf.left, value + "0", file)
    file = EncodeFile(ourLeaf.right, value + "1", file)
    return file


def Huffman(ourTree, directory):
    open(directory, 'w').writelines(EncodeFile(ourTree[0], "", open("input.txt", 'r').read()) + "\n")
    addDictionary(ourTree[0])


if __name__ == '__main__':
    try:
        Huffman(createNewTree("input.txt"), "output.txt")
        print('Successfully executed code, check output file')
    except Exception as e:
        print('Code failed, exception: ', e)