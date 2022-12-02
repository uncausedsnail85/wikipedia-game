import wikipedia
import sys
from queue import Queue
import time

# returns a list of page titles, the path
def wikiGameDFS(initialPageTitle, destinationPageTitle):

    # if source and destination are the same
    if initialPageTitle == destinationPageTitle:
        return [initialPageTitle]

    # start timer
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
        print("elapsed time: ", round(time.time()-start, 1))

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
        print("curr_node: ", curr_node)

        # Get links in page as successors
        try:
            succList = wikipedia.page(curr_node[0], auto_suggest=False).links
        except Exception as e:
            print("e")

        # add each link into queue
        # And check if link is already in explored set to
        for succ in succList:
            if (succ not in explored):
                succNodePath = curr_node[1].copy()
                succNodePath.append(succ)
                succNode = (succ, succNodePath)
                frontier.put(succNode)