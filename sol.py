import heapq

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
	return RegionArea(EnclosingDict) - RegionArea(Region1)
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

def SplitNode(node):
	if node.father == None:
		node.father = node()
		node.father.Children.append(node)
		Child1 = node(father = node.father)
		Child2 = node(father = node.father)
		SeedList = PickSeeds(node, Child1, Child2)
		Seed1 = node.Children.pop(SeedList[0])
		Seed2 = node.Children.pop(SeedList[1])
		Child1.Children.append(Seed1)
		Child2.Children.append(Seed2)
		Seed1.father = Child1
		Seed2.father = Child2
		MergeRegion(Child1.Region, Seed1.Region)
		MergeRegion(Child2.Region, Seed2.Region)
		while len(node.Children) > 0:
			Next = PickNext(node, Child1, Child2)
			if len(Child1.Children) > len(Child2.Children) and len(Child2.Children) + len(node.Children) == node.MinKey:
				for child in node.Children:
					Child2.Region = MergeRegion(Child2.Region, child.Region)
					Child2.Children.append(child)
					child.father = Child2
				node.Children = []
				break
			if len(Child2.Children) > len(Child1.Children) and len(Child1.Children) + len(node.Children) == node.MinKey:
				for child in node.Children:
					Child1.Region = MergeRegion(Child1.Region, child.Region)
					Child1.Children.append(child)
					child.father = Child1
				node.Children = []
				break
			if Next[1] == 1:
				child = node.Children[Next[0]]
				Child2.Region = MergeRegion(Child2.Region, child.Region)
				child.father = Child2
				Child2.Children.append(child)
			else:
				child = node.Children[Next[0]]
				Child1.Region = MergeRegion(Child1.Region, child.Region)
				child.father = Child1
				Child1.Children.append(child)
		node.father.Children.remove(node)
		node.father.Children.append(Child1)
		node.father.Children.append(Child2)
		node.father.Region = MergeRegion(node.father.Region, Child1.Region)
		node.father.Region = MergeRegion(node.father.Region, Child2.Region)

	else:
		Child1 = node(father = node.father)
		Child2 = node(father = node.father)
		SeedList = PickSeeds(node, Child1, Child2)
		Seed1 = node.Children.pop(SeedList[0])
		Seed2 = node.Children.pop(SeedList[1])
		Child1.Children.append(Seed1)
		Child2.Children.append(Seed2)
		Seed1.father = Child1
		Seed2.father = Child2
		MergeRegion(Child1.Region, Seed1.Region)
		MergeRegion(Child2.Region, Seed2.Region)
		while len(node.Children) > 0:
			Next = PickNext(node, Child1, Child2)
			if len(Child1.Children) > len(Child2.Children) and len(Child2.Children) + len(node.Children) == node.MinKey:
				for child in node.Children:
					Child2.Region = MergeRegion(Child2.Region, child.Region)
					Child2.Children.append(child)
					child.father = Child2
				node.Children = []
				break
			if len(Child2.Children) > len(Child1.Children) and len(Child1.Children) + len(node.Children) == node.MinKey:
				for child in node.Children:
					Child1.Region = MergeRegion(Child1.Region, child.Region)
					Child1.Children.append(child)
					child.father = Child1
				node.Children = []
				break
			if Next[1] == 1:
				child = node.Children[Next[0]]
				Child2.Region = MergeRegion(Child2.Region, child.Region)
				child.father = Child2
				Child2.Children.append(child)
			else:
				child = node.Children[Next[0]]
				Child1.Region = MergeRegion(Child1.Region, child.Region)
				child.father = Child1
				Child1.Children.append(child)
		node.father.Children.remove(node)
		node.father.Children.append(Child1)
		node.father.Children.append(Child2)
		node.father.Region = MergeRegion(node.father.Region, Child1.Region)
		node.father.Region = MergeRegion(node.father.Region, Child2.Region)

	pass

def PickNext(node, Child1, Child2):
	WhichChild = 0
	Index = 0
	MaxDiffArea = 0
	for i in range(len(node.Children)):
		Temp1 = IncreasedRegion(MergeRegion(Child1.Region, node.Children[i].Region), Child1.Region)
		Temp2 = IncreasedRegion(MergeRegion(Child2.Region, node.Children[i].Region), Child2.Region)
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
			if RegionArea(MergeRegion(node.Children[i], node.Children[j])) - RegionArea(node.Children[i]) - RegionArea(node.Children[j]) > MaxArea:
				Index1 = i
				Index2 = j
				MaxArea = RegionArea(MergeRegion(node.Children[i], node.Children[j])) - RegionArea(node.Children[i]) - RegionArea(node.Children[j])
	return [Index1, Index2]
	pass

def AdjustTree(node):
	while node != None:
		if len(node.Children) > node.MaxKey:
			# Do something
			SplitNode(node)
		else:
			if node.father != None:
				node.father.Region = MergeRegion(node.father.Region, node.Region)
		node = node.father
	pass


def Insert(root, node):
	NodeToInsert = ChooseLeaf(root, node)
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
		Distance += Region[key] * Region[key]
	return Distance**0.5
	pass

def MinList(Region):
	TempList = []
	for i in range(NumDimension):
		key = str(i) + 'min'
		TempList.append(Region[key])
	return TempList
	pass

def Dominate(element):
	answer = True
	elementList = MinList(element.Region)
	for point in SkylinePoints:
		pointList = MinList(point.Region)
		for i in range(NumDimension):
			if elementList[i] < pointList[i]:
				answer = False
		if answer == True:
			return answer
		answer = True
	pass

def BBS(root):
	for child in root.Children:
		heapq.heappush(Heap, (Mindist(child.Region), child))
	while True:
		try:
			element = heapq.heappop(Heap)
			if Dominate(element):
				continue
			elif len(element.Children) != 0:
				for child in element.Children:
					if !Dominate(child):
						heapq.heappush(Heap, (Mindist(child.Region),child))
			else:
				heapq.heappush(Heap, (Mindist(element.Region),element))

		except:
			print "GG"
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
	with open('../query2.txt','r') as f:
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
	with open('../sample2.txt','r') as f:
		for Object in f:
			Object = map(int, Object.strip().split())
			Object2 = [Object[i] for i in Dimension]
			i = 0
			while i < NumDimension:
				DefaultDict[DefaultKeys[i]] = Object2[i]
				DefaultDict[DefaultKeys[i+1]] = Object2[i]
				i += 1
			Root = Insert(Root, node(Region = DefaultDict, index = Object[0]))
		BBS(Root)
