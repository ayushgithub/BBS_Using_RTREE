import heapq, pdb

class node(object):
    def __init__(self, Region = None, index = None, father = None, MinKey = None, MaxKey = None, Children = None):
        self.Region = Region
        self.index = index
        self.father = father
        self.MinKey = NumMinKey
        self.MaxKey = NumMaxKey
        self.Children = []

def RegionArea(Region):
    Area = 1
    for i in range(NumDimension):
        minstr = str(i) + 'min'
        maxstr = str(i) + 'max'
        Area *= Region[maxstr] - Region[minstr]
    return Area
    pass

def IncreasedRegion(Region1, Region2):
    EnclosingDict = dict.fromkeys(DefaultKeys, None)
    for i in range(NumDimension):
        minstr = str(i) + 'min'
        maxstr = str(i) + 'max'
        EnclosingDict[minstr] = min(Region1[minstr], Region2[minstr])
        EnclosingDict[maxstr] = max(Region1[maxstr], Region2[maxstr])
    X = RegionArea(EnclosingDict)
    Y = RegionArea(Region1)
    return X - Y
    pass

def MergeRegion(Region1, Region2):
    if Region1 == None:
        return Region2
    elif Region2 == None:
        return Region1
    else:
        EnclosingDict = dict.fromkeys(DefaultKeys, None)
        for i in range(NumDimension):
            minstr = str(i) + 'min'
            maxstr = str(i) + 'max'
            EnclosingDict[minstr] = min(Region1[minstr], Region2[minstr])
            EnclosingDict[maxstr] = max(Region1[maxstr], Region2[maxstr])    
        return EnclosingDict
    pass


def ChooseLeaf(root, node):
    if len(root.Children) == 0:
        return root
    elif len(root.Children[0].Children) == 0:
        return root
    else:
        TempIndex = 0
        Best = float("inf")
        for i in range(len(root.Children)):
            if IncreasedRegion(root.Children[i].Region, node.Region) < Best:
                Best = IncreasedRegion(root.Children[i].Region, node.Region)
                TempIndex = i
        return ChooseLeaf(root.Children[TempIndex], node)
    pass

def SplitNode(Node):
    if Node.father == None:
        Node.father = node()
        Node.father.Children.append(Node)
        Child1 = node(father = Node.father)
        Child2 = node(father = Node.father)
        SeedList = PickSeeds(Node, Child1, Child2)
        Seed2 = Node.Children.pop(SeedList[1])
        Seed1 = Node.Children.pop(SeedList[0])
        Child1.Children.append(Seed1)
        Child2.Children.append(Seed2)
        Seed1.father = Child1
        Seed2.father = Child2
        Child1.Region = MergeRegion(Child1.Region, Seed1.Region)
        Child2.Region = MergeRegion(Child2.Region, Seed2.Region)
        while len(Node.Children) > 0:
            Next = PickNext(Node, Child1, Child2)
            if len(Child1.Children) > len(Child2.Children) and len(Child2.Children) + len(Node.Children) == Node.MinKey:
                for child in Node.Children:
                    Child2.Region = MergeRegion(Child2.Region, child.Region)
                    Child2.Children.append(child)
                    child.father = Child2
                Node.Children = []
                break
            elif len(Child2.Children) > len(Child1.Children) and len(Child1.Children) + len(Node.Children) == Node.MinKey:
                for child in Node.Children:
                    Child1.Region = MergeRegion(Child1.Region, child.Region)
                    Child1.Children.append(child)
                    child.father = Child1
                Node.Children = []
                break
            else:
                if Next[1] == 1:
                    child = Node.Children.pop(Next[0])
                    Child2.Region = MergeRegion(Child2.Region, child.Region)
                    child.father = Child2
                    Child2.Children.append(child)
                else:
                    child = Node.Children.pop(Next[0])
                    Child1.Region = MergeRegion(Child1.Region, child.Region)
                    child.father = Child1
                    Child1.Children.append(child)
        Node.father.Children.remove(Node)
        Node.father.Children.append(Child1)
        Node.father.Children.append(Child2)
        Node.father.Region = MergeRegion(Node.father.Region, Child1.Region)
        Node.father.Region = MergeRegion(Node.father.Region, Child2.Region)

    else:
        Child1 = node(father = Node.father)
        Child2 = node(father = Node.father)
        SeedList = PickSeeds(Node, Child1, Child2)
        Seed2 = Node.Children.pop(SeedList[1])
        Seed1 = Node.Children.pop(SeedList[0])
        Child1.Children.append(Seed1)
        Child2.Children.append(Seed2)
        Seed1.father = Child1
        Seed2.father = Child2
        Child1.Region = MergeRegion(Child1.Region, Seed1.Region)
        Child2.Region = MergeRegion(Child2.Region, Seed2.Region)
        while len(Node.Children) > 0:
            Next = PickNext(Node, Child1, Child2)
            if len(Child1.Children) > len(Child2.Children) and len(Child2.Children) + len(Node.Children) == Node.MinKey:
                for child in Node.Children:
                    Child2.Region = MergeRegion(Child2.Region, child.Region)
                    Child2.Children.append(child)
                    child.father = Child2
                Node.Children = []
                break
            if len(Child2.Children) > len(Child1.Children) and len(Child1.Children) + len(Node.Children) == Node.MinKey:
                for child in Node.Children:
                    Child1.Region = MergeRegion(Child1.Region, child.Region)
                    Child1.Children.append(child)
                    child.father = Child1
                Node.Children = []
                break
            if Next[1] == 1:
                child = Node.Children.pop(Next[0])
                Child2.Region = MergeRegion(Child2.Region, child.Region)
                child.father = Child2
                Child2.Children.append(child)
            else:
                child = Node.Children.pop(Next[0])
                Child1.Region = MergeRegion(Child1.Region, child.Region)
                child.father = Child1
                Child1.Children.append(child)
        Node.father.Children.remove(Node)
        Node.father.Children.append(Child1)
        Node.father.Children.append(Child2)
        Node.father.Region = MergeRegion(Node.father.Region, Child1.Region)
        Node.father.Region = MergeRegion(Node.father.Region, Child2.Region)

    pass

def PickNext(node, Child1, Child2):
    WhichChild = 0
    Index = 0
    MaxDiffArea = 0
    for i in range(len(node.Children)):
#         Temp1 = IncreasedRegion(MergeRegion(Child1.Region, node.Children[i].Region), Child1.Region)
#         Temp2 = IncreasedRegion(MergeRegion(Child2.Region, node.Children[i].Region), Child2.Region)
        Temp1 = IncreasedRegion(Child1.Region, node.Children[i].Region)
        Temp2 = IncreasedRegion(Child2.Region, node.Children[i].Region)        
        if abs(Temp1 - Temp2) > MaxDiffArea:
            MaxDiffArea = abs(Temp1 - Temp2)
            Index = i
            if Temp1 - Temp2 > 0:
                WhichChild = 1
            else:
                WhichChild = 0
    return [Index, WhichChild]
    pass

def PickSeeds(node, Child1, Child2):

    Index1 = 0
    Index2 = 0
    MaxArea = 0
    for i in range(len(node.Children)):
        for j in range(i + 1, len(node.Children)):
            if RegionArea(MergeRegion(node.Children[i].Region, node.Children[j].Region)) - RegionArea(node.Children[i].Region) - RegionArea(node.Children[j].Region) > MaxArea:
                Index1 = i
                Index2 = j
                MaxArea = RegionArea(MergeRegion(node.Children[i].Region, node.Children[j].Region)) - RegionArea(node.Children[i].Region) - RegionArea(node.Children[j].Region)
    return [Index1, Index2]
    pass

def AdjustTree(node):
    Temp = node
    while Temp != None:
        if len(Temp.Children) > Temp.MaxKey:
            # Do something
            SplitNode(Temp)
        else:
            if Temp.father != None:
                Temp.father.Region = MergeRegion(Temp.father.Region, Temp.Region)
        Temp = Temp.father
    return
    pass

# def AdjustTree(node):
#     while node.father != None:
#         if len(node.Children) > node.MaxKey:
#             # Do something
#             SplitNode(node)
#         else:
#             if node.father != None:
#                 node.father.Region = MergeRegion(node.father.Region, node.Region)
#         node = node.father
#     # return node
#     pass

def Insert(root, node):
    NodeToInsert = ChooseLeaf(root, node)
    # pdb.set_trace()
    node.father = NodeToInsert
    NodeToInsert.Children.append(node)
    NodeToInsert.Region = MergeRegion(NodeToInsert.Region, node.Region)
    AdjustTree(NodeToInsert)
    if root.father != None:
        root = root.father
    return root
    pass

def Mindist(Region):
    Distance = 0
    for i in range(NumDimension):
        key = str(i) + 'min'
        Distance += Region[key]
    return Distance
    pass

def MinList(Region):
    TempList = []
    for i in range(NumDimension):
        key = str(i) + 'min'
        TempList.append(Region[key])
    return TempList
    pass

def IsDominate(pointList, elementList):
    for i in range(NumDimension):
        if elementList[i] < pointList[i]:
            return False
    return True
    pass

def Dominate(element):
    elementList = MinList(element.Region)
    for point in SkylinePoints:
        pointList = MinList(point.Region)
        if IsDominate(pointList, elementList):
            return True
    return False    
    pass

def BBS(root):
    for child in root.Children:
        heapq.heappush(Heap, (Mindist(child.Region), child))
    while True:
        try:
            element = heapq.heappop(Heap)[1]
            if Dominate(element):
                continue
            elif len(element.Children) != 0:
                for child in element.Children:
                    if not Dominate(child):
                        heapq.heappush(Heap, (Mindist(child.Region),child))
            else:
                SkylinePoints.append(element)

        except:
            print "GG"
            for points in SkylinePoints:
                print points.Region
            break
    pass

DiskPageSize = 0
KeySize = 0
PointerSize = 0
Dimension = []
NumDimension = 0
NumMaxKey = 0
NumMinKey = 0
DefaultDict = {}
DefaultKeys = []
Heap = []
SkylinePoints = []
Root = None
if __name__ == "__main__":
    with open('query2.txt','r') as f:
        # Dimension = [i- 1 for i in map(int, f.readline().strip().split())]
        Dimension = map(int, f.readline().strip().split())
        NumDimension = len(Dimension)
        DiskPageSize = int(f.readline().strip())
        string = f.readline().strip().split()
        PointerSize = int(string[0])
        KeySize = int(string[1])
        NumMaxKey = divmod(DiskPageSize, PointerSize + KeySize)[0]
        NumMinKey = NumMaxKey/2
        DefaultKeys = []
        for i in range(NumDimension):
            DefaultKeys.append(str(i) + 'min')
            DefaultKeys.append(str(i) + 'max')
        DefaultDict = dict.fromkeys(DefaultKeys, None)

    Root = node()
    with open('sample2.txt','r') as f:
        for Object in f:
            Object = map(int, Object.strip().split())
            Object2 = [Object[i] for i in Dimension]
            i = 0
            TempDict = {}
            TempDict = dict.fromkeys(DefaultKeys, None)
            while i < NumDimension:
                key0 = str(i) + 'min'
                key1 = str(i) + 'max'
                TempDict[key0] = Object2[i]
                TempDict[key1] = Object2[i]
                i += 1
            Root = Insert(Root, node(Region = TempDict, index = Object[0]))
        BBS(Root)
