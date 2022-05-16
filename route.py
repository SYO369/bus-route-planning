import constant
import random

class RouteDetail(object):
    def __init__(self, route: list, noOfBus=0):
        self.route = route
        self.noOfBus = noOfBus
    
    def print(self):
        print("route: ", self.route, " bus: ", self.noOfBus)

class RouteSet(object):
    def __init__(self, routeDetailList: list[RouteDetail], totalDemand=0, transferCount=0):
        self.routeDetailList = routeDetailList
        self.totalDemand = totalDemand
        self.transferCount = transferCount

    def get_probability(self, bestRouteSet) -> float:
        h = self.get_node_pair_count(bestRouteSet)
        L = self.get_total_node_pair(bestRouteSet)
        return (((1-0.08) * (h / L)) + 0.08) ** 0.02
    
    def get_node_pair_count(self, bestRouteSet) -> int:
        nodePairCount = 0
        for i in range (0, len(self.routeDetailList)):
            #duplicateRoute = []
            for j in range (0, len(self.routeDetailList[i].route) - 1):
                if (j >= len(bestRouteSet.routeDetailList[i].route) - 1):
                    break
                if (self.routeDetailList[i].route[j] == bestRouteSet.routeDetailList[i].route[j] and self.routeDetailList[i].route[j+1] == bestRouteSet.routeDetailList[i].route[j+1]):
                    #if (len(duplicateRoute) > 1):
                    #   duplicateRoute.pop()
                    #duplicateRoute.append(self.routeDetail[i].route[j])
                    #duplicateRoute.append(self.routeDetail[i].route[j+1])
                    nodePairCount += 1
            # For debug using
            #print(duplicateRoute)
        return nodePairCount
    
    def get_total_node_pair(self, bestRouteSet) -> int:
        count = 0
        for i in range(0, len(self.routeDetailList)):
            count += len(self.routeDetailList[i].route) - 1
        
        for i in range(0, len(bestRouteSet.routeDetailList)):
            count += len(bestRouteSet.routeDetailList[i].route) - 1

        return count
    
    def print(self):
        print("Total Demand: ", self.totalDemand)
        print("Total transfer count: ", self.transferCount)
        for route in self.routeDetailList:
            route.print()

def get_headway(totalTravelTime, numOfbus) -> float:
    return (totalTravelTime * 2) / numOfbus

#Not in use
def routeMapInit() -> list:
    routeMap = []
    routeMap.append(RouteDetail(constant.Route1.stop, constant.Route1.numOfBus))
    routeMap.append(RouteDetail(constant.Route2.stop, constant.Route2.numOfBus))
    routeMap.append(RouteDetail(constant.Route3.stop, constant.Route3.numOfBus))
    routeMap.append(RouteDetail(constant.Route4.stop, constant.Route4.numOfBus))
    routeMap.append(RouteDetail(constant.Route5.stop, constant.Route5.numOfBus))
    routeMap.append(RouteDetail(constant.Route6.stop, constant.Route6.numOfBus))
    routeMap.append(RouteDetail(constant.Route7.stop, constant.Route7.numOfBus))
    routeMap.append(RouteDetail(constant.Route8.stop, constant.Route8.numOfBus))
    routeMap.append(RouteDetail(constant.Route9.stop, constant.Route9.numOfBus))
    routeMap.append(RouteDetail(constant.Route10.stop, constant.Route10.numOfBus))
    generate_route(routeMap)
    return routeMap

def generate_route(oldList: list):
    i = 0
    extraRouteNum = 5
    extraList = []
    while i < extraRouteNum:
        newRoute:RouteDetail = random.choice(oldList)
        if newRoute.route not in extraList:
            r = set(random.sample(range(len(newRoute.route)), 1))
            result = [x for e,x in enumerate(newRoute.route) if not e in r]
            oldList.append(RouteDetail(result, newRoute.noOfBus))
        i += 1

def random_generate_route() -> list:
    startNodeList = constant.START_NODE.copy()
    stopNodeList = constant.STOP_NODE.copy()
    lastNodeList = constant.LAST_NODE.copy()
    routeMap = []
    for i in range(0,constant.VALID_ROUTE_SET):    
        route = []
        route.append(random_node(startNodeList))
        for j in range (0,constant.MIDDLE_NODE_COUNT):
            route.append(random_node(stopNodeList))
            if (len(stopNodeList) == 0):
                stopNodeList = constant.STOP_NODE.copy()
        route.append("T")
        route.append(random_node(lastNodeList))
        routeMap.append(RouteDetail(route))

        if (len(startNodeList) == 0):
            startNodeList = constant.START_NODE.copy()
        if (len(lastNodeList) == 0):
            lastNodeList = constant.LAST_NODE.copy()
    
    #assign_bus(routeMap)
    return routeMap

def random_node(nodeList: list) -> int:
    node = random.choice(nodeList)
    nodeList.remove(node)
    return node

def assign_bus(routeDetailList: list[RouteDetail]):
    busNum = constant.TOTAL_BUS_NUM
    for i in range(0, len(routeDetailList)):
        if (i == len(routeDetailList) - 1):
            routeDetailList[i].noOfBus = busNum
            break
        randomBus = random.randint(1, busNum - len(routeDetailList) + i)
        routeDetailList[i].noOfBus = randomBus
        busNum = busNum - randomBus

# define main class
if __name__ == "__main__":
    print("route.py")