import constant
from djikstra import DijsktraImpl
import route

#routeTable = []
dijsktraImpl = DijsktraImpl()
EDGES = constant.EdgesTable()

def check_single_route(routeMap, current, destination) -> bool:
    for r in routeMap:
        if (current in r.route) & (destination in r.route):
            return True
    return False

def get_routes(routeMap, current, destination) -> list:
    routes = []
    for index, r in enumerate(routeMap):
        if (current in r.route) & (destination in r.route):
            routes.append(r)
    return routes

def get_shortest_path_travel_time(current, destination) -> float:
    travelTime = 0
    route = dijsktraImpl.get_shortest_path(str(current), str(destination))
    for i in range(route.index(str(current)), len(route)):
        if route[i] == str(destination):
            break
        t = EDGES.get_travel_time(route[i], route[i+1])
        if t is None:
            raise ValueError('Cannot get travel time from ', route[i], ' to ', route[i+1])
        travelTime += t
    EDGES.insert_travel_time(current, destination, travelTime)
    return travelTime
    
def get_average_travel_time(current, destination, routeList) -> float:
    #minTravelTime = 999.00
    headwayRatio = 0.00
    headwayTotal = 0.00
    freqAverage = 0.00
    for r in routeList:
        newtravelTime = 0
        currentRoute = r.route
        for i in range(currentRoute.index(current), len(currentRoute) - 1):
            if str(currentRoute[i]) == str(destination):
                break
            # Last travel no stopping time
            elif str(currentRoute[i+1]) == str(destination):
                t = EDGES.get_travel_time(str(currentRoute[i]), str(currentRoute[i+1]))
                if t is None:
                    t = get_shortest_path_travel_time(currentRoute[i], currentRoute[i+1])
            else: 
                t = EDGES.get_travel_time(str(currentRoute[i]), str(currentRoute[i+1]))
                if t is None:
                    t = get_shortest_path_travel_time(currentRoute[i], currentRoute[i+1])
                t += constant.STOPPING_TIME
            newtravelTime += t
        #print("travelTime", newtravelTime)

        totalTravelTime = get_total_travel_time(currentRoute)
        headway = (1 / route.get_headway(totalTravelTime, r.noOfBus))
        headwayRatio += (newtravelTime * headway)
        headwayTotal += headway
        freqAverage = (headwayRatio + 1) / headwayTotal
    return freqAverage

def get_total_travel_time(routeList) -> float:
    newtravelTime = 0
    for i in range(0, len(routeList) - 1):
        t = EDGES.get_travel_time(str(routeList[i]), str(routeList[i+1]))
        if t is None:
            t = get_shortest_path_travel_time(routeList[i], routeList[i+1])
        if (i + 1 <= len(routeList)):
            t += constant.STOPPING_TIME
        newtravelTime += t
    return newtravelTime

def get_total_average_travel_time(routeMap, current, destination) -> float:
    result = 0
    if check_single_route(routeMap, current, destination):
        # Two points are in the single route
        routeList = get_routes(routeMap, current, destination)
        result = get_average_travel_time(current, destination, routeList)
    else:
        # Two points NOT in the single route, find all optinal interchange routes
        routeList_A = get_routes(routeMap, current, "T")
        result += get_average_travel_time(current, "T", routeList_A)

        routeList_B = get_routes(routeMap, "T", destination)
        result += get_average_travel_time("T", destination, routeList_B)
        #result += DBconn.get_travel_time("T", str(destination))

    return result

def get_total_trend(routeSet: route.RouteSet) -> float:
    result = 0
    transferTotal = 0
    for fromNode in range(1,24):
        for toNode in range (24,29):
            #print("fromNode ",fromNode," toNode ", toNode)
            travelDemand = constant.get_travel_demand(str(fromNode), str(toNode))
            result += (get_total_average_travel_time(routeSet.routeDetailList, fromNode, toNode) * travelDemand)

            
            # calculate transfer total
            if check_single_route(routeSet.routeDetailList, fromNode, toNode):
                pass
            else:
                transferTotal += travelDemand
            
    routeSet.transferCount = transferTotal
    return result

def allocate_bus(routeSet: route.RouteSet) -> float:
    i = 0
    routeMap = routeSet.routeDetailList

    while i < len(routeMap):
        for j in range(i+1,len(routeMap)):
            oldTotalTrend  = get_total_trend(routeSet)

            if (routeMap[j].noOfBus - 1 > 0):
                routeMap[i].noOfBus += 1
                routeMap[j].noOfBus -= 1
                newTotalTrend = get_total_trend(routeSet)
                if (newTotalTrend < oldTotalTrend):
                    #print('1Best route ',i," +1 ",j," -1 ")
                    #i = 0
                    break
                else:
                    # Undo
                    routeMap[i].noOfBus -= 1
                    routeMap[j].noOfBus += 1

            if (routeMap[i].noOfBus - 1 > 0):
                routeMap[i].noOfBus -= 1
                routeMap[j].noOfBus += 1
                newTotalTrend = get_total_trend(routeSet)
                if (newTotalTrend < oldTotalTrend):
                    #print('2Best route ',j," +1 ",i," -1 ")
                    #i = 0
                    break
                else:
                    # Undo
                    routeMap[i].noOfBus += 1
                    routeMap[j].noOfBus -= 1
        i += 1

    return get_total_trend(routeSet)

# define main class
if __name__ == "__main__":
    print("route_calc.py")