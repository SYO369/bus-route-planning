from ast import Constant
import copy
from doctest import master
import route
import route_calc
import constant
import transformer
import random
import time
from operator import itemgetter, attrgetter

def gen_route_map(parentSet: list[route.RouteSet]):
    """
    Crossover different sets of route by following steps:
    1. Pair up all 20 sets
    2. Crossover routes between two sets
    
    There should be 40 sets (20 original sets and 20 new sets) for coming process
    """
    childSet = copy.deepcopy(parentSet)
    transformer.shuffle_route_crossover(childSet)
    # validate route set node is duplicate/exclude

    """
    Randomly do mutation routes in each set by one of the four methods
    1. randomly select one method for each set
    2. Probability of four method : 0.4,0.4,0.1,0.1
    3. Originm T & destination cannot be moved
    4. If there are repeat stop on same route, randomly delete one of the stop
    5. If there are stops not covered, undo and do mutation again
    """
    for c in childSet:
        transformer.random_transform(c)
    parentSet.extend(childSet)

def gen_express_route(parentSet: list[route.RouteSet]):
    """
    Generate express route for each set
    1. crossover stops of same route
    2. 20 subsets (10 original + 10 new) is formed
    """
    subSet = copy.deepcopy(parentSet)
    bineryMap = transformer.gen_binary_map(subSet)
    transformer.shuffle_route_crossover(bineryMap)
    transformer.binery_to_stop(subSet, bineryMap)
    for i in range(0,len(parentSet)):
        parentSet[i].routeDetailList.extend(subSet[i].routeDetailList)

def del_sub_route(parentSet: list[route.RouteSet]):
    for s in parentSet:
        s.routeDetailList = s.routeDetailList[:10]

if __name__ == "__main__":
    inlcudeSubset = input("Inlcude subset? (y/n) :  ")
    if inlcudeSubset != 'y' and inlcudeSubset != 'n':
        quit()
    """
    Generate 20 set route sets of routes with following rules:
    1. 10 routes for each set
    2. All routes should be formed as below: [Origin -> 9 stops -> T -> Destination]
    3. Only dedicated stops can be origin and destination
    4. No repeat stop on same routes
    5. All stops should be covered in each set
    """
    start_time = time.time()
    masterSet = []
    parentSet = []
    isKeep = False
    count = 0
    while count <= constant.MAX_LOOP_COUNT:
        if len(parentSet) > 0:
            print(".", end = '')
        else:
            for i in range(0, constant.TOTAL_ROUTE_SET):
                parentSet.append(route.RouteSet(route.random_generate_route()))
        
        gen_route_map(parentSet)
        if inlcudeSubset == "y":
            gen_express_route(parentSet)
            #del_sub_route(parentSet)
        
        for i in range(0,len(parentSet)):
            route.assign_bus(parentSet[i].routeDetailList)
            #parentSet[i].totalDemand = route_calc.get_total_trend(parentSet[i].routeDetailList)
            parentSet[i].totalDemand = route_calc.allocate_bus(parentSet[i])
        
        if isKeep:
            parentSet.extend(masterSet)
            masterSet = []

        # Sort array with ascending total travel time
        parentSet.sort(key=attrgetter('totalDemand'))

        # Find the best route set with minimum total travel time
        bestRouteSet = parentSet[0]
        masterSet.append(bestRouteSet)

        # Delete route set by calculated probability
        for s in parentSet:
            probability = s.get_probability(bestRouteSet)
            isInsert = random.choices([True, False], [probability, 1 - probability])
            if isInsert[0]:
                masterSet.append(s)
        
        # If element < 20, keep master set and re-gen parent set again
        # else pick 20 set
        if len(masterSet) < 20:
            isKeep = True
            masterSet = parentSet[::]
            parentSet = []
        else:
            isKeep = False
            parentSet = masterSet[:20]
            masterSet = []
            count = count + 1

    print("")
    parentSet[0].print()
    print("Execution time: %s s" % (time.time() - start_time))
