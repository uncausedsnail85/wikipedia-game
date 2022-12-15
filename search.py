import wikipedia
import sys
from queue import Queue, PriorityQueue
import time

# returns a list of page titles, the path
def wikiGameBFS(initialPageTitle, destinationPageTitle):

    # if source and destination are the same
    if initialPageTitle == destinationPageTitle:
        return [initialPageTitle]

    # start timer, ideally should be commented out
    start = time.time()

    # search node of a BFS graph
    initialNode = (initialPageTitle, [initialPageTitle])
    # Init queue for BFS, keeping track of next in line
    frontier = Queue(maxsize=0)
    frontier.put(initialNode)
    # explored set
    explored = [] #List of titles (string)

    # loop forever until: queue is empty or destination page is reached
    while(True):
        # print("elapsed time: ", round(time.time()-start, 1))

        # if queue is empty, no further 
        if frontier.empty(): return None
        curr_node = frontier.get()

        # If a link has been explored before, continue.
        # This happens when a link is added multiple times to the
        # queue by different pages.
        if (curr_node[0] in explored): continue

        # Explore the link by adding to explored set
        explored.append(curr_node[0])

        # Test if link is destination
        if (curr_node[0] == destinationPageTitle): return curr_node[1]
        # print("curr_node: ", curr_node)

        # Get links in page as successors
        try:
            succList = wikipedia.page(curr_node[0], auto_suggest=False).links
        except Exception as e:
            # print(e)
            pass

        # add each link into queue
        # And check if link is already in explored set to
        for succ in succList:
            if (succ not in explored):
                succNodePath = curr_node[1].copy()
                succNodePath.append(succ)
                succNode = (succ, succNodePath)
                frontier.put(succNode)

##########################################################

# Given a page, return the distance between the category
# of the given page and the category of the dest page.
# Wikipedia organizes categories with subcategories,
# leading to an almost tree like structure (accurately
# it is a partially ordered set). By using the distance
# to the target category, we can use it as a heuristic.
def shrotestDistanceCategoriesHeuristic(pageTitle, destinationCategories):
    try:
        sourceCats = wikipedia.page(pageTitle, auto_suggest=False).categories
    except Exception as e:
        print(e)
        return sys.maxsize

    # sourceCats = wikipedia.page(pageTitle, auto_suggest=False).categories
    # print("find heuristic for Source page:", pageTitle)
    # todo: bring this call outside of the function
    # destCats = wikipedia.page(destinationTitle, auto_suggest=False).categories 
    destCats = destinationCategories.copy()
    # print("DestCats:", destCats)
    # return number of matching categories
    numberMatches = 0
    for i in sourceCats:
        for j in destCats:
            # print("j:", j)
            if i == j:                
                numberMatches =+ 1
                destCats.remove(j)
    # print("Done, number of matches:", numberMatches)
    return numberMatches

# Returns number of intersecting categories, normalized over 1.
def numberOfSameCategoriesHeuristic(pageTitle, destinationCategories):
    try:
        sourceCats = wikipedia.page(pageTitle, auto_suggest=False).categories
    except Exception as e:
        # print(e)
        return sys.maxsize
    destCats = destinationCategories.copy()
    common_len = len(set(sourceCats) & set(destCats))
    return 1 - common_len/len(destCats)

def nullHeuristic(pageTitle, destinationTitle):
    return 0 

def wikiGameAStar(initialPageTitle, destinationPageTitle, heuristic):

    # pre-fetching destination page categories
    destinationPageCategories =  wikipedia.page(destinationPageTitle, auto_suggest=False).categories 

    # source and dest are the same page
    if initialPageTitle == destinationPageTitle:
        return [initialPageTitle]

    # start timer, ideally should be commented out
    start = time.time()

    # the search node of a A* search graph
    initialNode = (initialPageTitle, [initialPageTitle])
    # Init priority queue for, keeping track of lowest heuristic
    frontier = PriorityQueue(maxsize=0)
    frontier.put((heuristic(initialNode[0], destinationPageCategories), initialNode))
    # explored set
    explored = [] #List of titles (string)

    # loop forever until: queue is empty or destination page is reached
    while(True):
        # print("elapsed time: ", round(time.time()-start, 1))

        # if queue is empty, no further 
        if frontier.empty(): return None
        frontierPop = frontier.get()
        curr_node = frontierPop[1]

        # print("curr_node: ", curr_node)
        
        # If a link has been explored before, continue.
        # This happens when a link is added multiple times to the
        # queue by different pages.
        if (curr_node[0] in explored): continue

        # Explore the link by adding to explored set
        explored.append(curr_node[0])

        # Test if link is destination
        if (curr_node[0] == destinationPageTitle): 
            return curr_node[1]

        # Get links in page as successors
        try:
            succList = wikipedia.page(curr_node[0], auto_suggest=False).links
        except Exception as e:
            # print(e)
            pass


        # add each link into queue
        # And check if link is already in explored set to
        for succ in succList:
            if (succ not in explored):
                succNodePath = curr_node[1].copy()
                succNodePath.append(succ)
                succPathCost = 1 + frontierPop[0]
                succNode = (succ, succNodePath)
                if (succNode[0] not in explored):
                    frontier.put((succPathCost + heuristic(succNode[0], destinationPageCategories), succNode))

