import random
import constant
import route
from route import RouteSet
from route import RouteDetail

"""
Route Crossover Example
Parent 1: [R1,R2,R3,R4,R5,R6,R7,R8,R9,R10]
Paretn 2: [r1,r2,r3,r4,r5,r6,r7,r8,r9,r10]

Child 1:  [R1,R2,R3,R4,r5,r6,r7,r8,R9,R10]
Child 2:  [r1,r2,r3,r4,R5,R6,R7,R8,r9,r10]
"""
def shuffle_route_crossover(routeSetList: list[RouteSet]):
    # Using Fisher–Yates shuffle method
    for i in range(len(routeSetList) - 1, 0, -1):
        swap_idx = random.randint(0, i-1)
        #array[i], array[swap_idx] = array[swap_idx], array[i]
        if i != swap_idx:
            shuffle_swap_element(routeSetList[i].routeDetailList, routeSetList[swap_idx].routeDetailList)

def shuffle_swap_element(array1: list, array2: list):
    elementNum = random.randint(1,10)
    elementIndex = random.randint(0,len(array1) - elementNum)
    for i in range(0, len(array1)):
        if i >= elementIndex and elementNum > 0:
            array1[i], array2[i] = array2[i], array1[i]
            elementNum -= 1
    

"""
Random 4 mutation operators for the genetic algorithm:

(1) Insert mutation
(2) Remove mutation
(3) Swap mutation
(4) Transfer mutation
"""
def random_transform(routeSet: RouteSet):
    
    method = random.choices([1,2,3,4], [0.4,0.4,0.1,0.1])
    match method[0]:
        case 1:
            #print('Insert mutation')
            random_insert_node(routeSet.routeDetailList)
        case 2:
            #print('Remove mutation')
            random_remove_node(routeSet.routeDetailList)
        case 3:
            #print('Swap mutation')
            swap_node(routeSet.routeDetailList)
        case 4:
            #print('Transfer mutation')
            transfer_node(routeSet.routeDetailList)


"""
(1) Insert mutation
Example:
Before mutation [1,18,15,8,12,7,25]
After mutation  [1,18,15,8,'10',12,7,25]
"""
def random_insert_node(routeDetailList: list[RouteDetail]):
    for routeDetail in routeDetailList:
        route = routeDetail.route
        # random pick node without start and last two node
        insertIndex = random.randint(1,len(route)-2)
        newNode = random.choice([node for node in constant.STOP_NODE if node not in route])
        route[insertIndex:insertIndex] = [newNode]

"""
(2) Remove mutation
Example:
Before mutation [1,18,15,'8',12,7,25]
After mutation  [1,18,15,12,7,25]
"""
def random_remove_node(routeDetailList: list[RouteDetail]):
    for routeDetail in routeDetailList:
        route = routeDetail.route
        
        # random pick node without start and last two node
        removeNode = random.choice(route[1:len(route)-2])

        # check node must use more than once
        count = 0
        for routeDetail in routeDetailList:
            if removeNode in routeDetail.route:
                count += 1
            
        if count > 1:
            route.remove(removeNode)

"""
(3) Swap mutation
Example:
Before mutation
Route i [1,18,15,'8',12,7,25]
Route j [9,7,"6",5,13,24]

After mutation
Route i [1,18,15,"6",12,7,25]
Route j [9,7,'8',5,13,24]
"""
def swap_node(routeDetailList: list[RouteDetail]):
    # Using Fisher–Yates shuffle method
    for i in range(len(routeDetailList) - 1, 0, -1):
        swap_idx = random.randint(0, i-1)
        #array[i], array[swap_idx] = array[swap_idx], array[i]
        if i != swap_idx:
            # random pick node without start and end node
            while True:
                nodeIndex1 = random.randint(1,len(routeDetailList[i].route)-2)
                nodeIndex2 = random.randint(1,len(routeDetailList[swap_idx].route)-2)
                if routeDetailList[i].route[nodeIndex1] not in routeDetailList[swap_idx].route:
                    routeDetailList[i].route[nodeIndex1], routeDetailList[swap_idx].route[nodeIndex2] = routeDetailList[swap_idx].route[nodeIndex2], routeDetailList[i].route[nodeIndex1]
                    break

"""
(4) Transfer mutation
Example:
Before mutation
Route i [1,18,15,'6',12,7,25]
Route j [9,7,8,5,13,24]

After mutation
Route i [1,18,15,12,7,25]
Route j [9,7,8,'6',5,13,24]
"""
def transfer_node(routeDetailList:list[RouteDetail]):
    # Using Fisher–Yates shuffle method
    for i in range(len(routeDetailList) - 1, 0, -1):
        swap_idx = random.randint(0, i)
        #array[i], array[swap_idx] = array[swap_idx], array[i]
        if i != swap_idx:
            while True:
                # random pick node without start and end node
                if len(routeDetailList[i].route) > len(routeDetailList[swap_idx].route):
                    nodeIndex = random.randint(1,len(routeDetailList[swap_idx].route)-2)
                else:
                    nodeIndex = random.randint(1,len(routeDetailList[i].route)-2)
                
                transferNode = routeDetailList[i].route[nodeIndex]
                if transferNode not in routeDetailList[swap_idx].route[nodeIndex:nodeIndex]:
                    routeDetailList[swap_idx].route[nodeIndex:nodeIndex] = [transferNode]
                    routeDetailList[i].route.remove(transferNode)
                    break

def validation_duplicate_node(routeDetailList: list[RouteDetail]) -> bool:
    for routeDetail in routeDetailList:
        for node in routeDetail.route:
            if routeDetail.route.count(node) > 1:
                return False
    return True


def binary_genetic(routeDetailList: list):
    for routeDetail in routeDetailList:
        route = list(routeDetail.route)
        # exclude fisrt digit & last digit, ramdomly choose 3 digit=1, other=0
        maxFalseCount = random.randint(1, len(route)-6)
        for i in range (1, len(route)-3):
            if maxFalseCount == 0:
                break

            randomNum = random.randrange(10)
            if randomNum > 5:
                routeDetail.route.remove(route[i])
                maxFalseCount -= 1

def gen_binary_map(routeSetList: list[RouteSet]) -> list[RouteSet]:
    binaryMap = []
    for i in range(0, len(routeSetList)):
        binRouteList = []
        for j in range(0, len(routeSetList[i].routeDetailList)):
            binRoute = []
            routes = routeSetList[i].routeDetailList[j].route
            # exclude fisrt digit & last two digit, ramdomly choose 3 digit=1, other=0
            for k in range(0,len(routes)):
                if k == 0 or k >= len(routes)-2:
                    binRoute.append(1)
                else:
                    binRoute.append(0)
            
            maxTrueCount = 3
            for k in range(1, len(binRoute)-3):
                if maxTrueCount == 0:
                    binRoute[k] = 0
                else:
                    randomNum = random.randrange(10)
                    if randomNum > 5:
                        binRoute[k] = 1
                        maxTrueCount -= 1
            
            # if middle stop = 1 < 3, change to 1 by sequence
            if maxTrueCount > 0:
                for k in range(1, len(binRoute)-3):
                    if maxTrueCount == 0:
                        break
                    
                    if binRoute[k] != 1:
                        binRoute[k] = 1
                        maxTrueCount -= 1
            binRouteList.append(route.RouteDetail(binRoute))
        binaryMap.append(route.RouteSet(binRouteList))
    return binaryMap

def binery_to_stop(routeSetList: list[RouteSet], binerySetList: list[RouteSet]):
    if len(routeSetList) != len(binerySetList):
        raise Exception("route set content not match")
    
    for i in range(0,len(routeSetList)):
        for j in range(0, len(routeSetList[i].routeDetailList)):
            newRoute = []
            for k in range(0, len(routeSetList[i].routeDetailList[j].route)):
                oldStop = routeSetList[i].routeDetailList[j].route[k]
                bineryStop = binerySetList[i].routeDetailList[j].route[k]
                if bineryStop != 0:
                    newRoute.append(oldStop)
            routeSetList[i].routeDetailList[j].route = newRoute

if __name__ == "__main__":
    print("transformer.py")

