import wikipedia
import sys
from queue import Queue, PriorityQueue
import time

def wikiGameBidirectionalBFS(initialPageTitle, destinationPageTitle):
    # if source and destination are the same
    if initialPageTitle == destinationPageTitle:
        return [initialPageTitle]

    # start timer, ideally should be commented out
    start = time.time()

    # search node of a BFS graph
    initialNode = (initialPageTitle, [initialPageTitle])
    dstNode = (destinationPageTitle, [destinationPageTitle])

    # Init queues for BFS, keeping track of next in line
    srcFrontier = Queue(maxsize=0)
    srcFrontier.put(initialNode)
    dstFrontier = Queue(maxsize=0)
    dstFrontier.put(dstNode)

    # The history queue is keeping track of what is in the queue but also the history
    # it is essentially frontier union explored set
    srcFrontierHistory = Queue(maxsize=0)
    srcFrontierHistory.put(initialNode)
    dstFrontierHistory = Queue(maxsize=0)
    dstFrontierHistory.put(dstNode)

    # explored sets
    srcExplored = [] #List of titles (string)
    dstExplored = []

    # loop while any queue is not empty or destination page is reached

    while(srcFrontier.empty() is False and dstFrontier.empty() is False):
        print("elapsed time: ", round(time.time()-start, 1))

        # explore source frontier
        if srcFrontier.empty() is False:

            curr_node = srcFrontier.get()

            # If a link has been explored before, continue.
            # This happens when a link is added multiple times to the
            # queue by different pages.
            if (curr_node[0] not in srcExplored):

                # Explore the link by adding to explored set
                srcExplored.append(curr_node[0])
                # print("src_curr_node: ", curr_node)


                inDstQueue = False
                # Looping thorugh dst queue to find if curr_node in dstQueueHistory
                for node in dstFrontierHistory.queue:
                    if node[0] == curr_node[0]:
                        inDstQueue = True
                # print("inDstQueue", inDstQueue)
                # If link is dest, or its in dest frontier history, return the solution
                # we use the history because if its been explored or will be explored, 
                # we've found a path
                if (curr_node[0] == destinationPageTitle) or inDstQueue:
                    while dstFrontierHistory.empty() is False:
                        dstNode = dstFrontierHistory.get()
                        if dstNode[0] == curr_node[0]:
                            print("init dstNode[1]", dstNode[1])
                            dstNode[1].pop() # remove the node in common
                            dstNode[1].reverse() # reverse dst queue direction
                            return curr_node[1] + dstNode[1] # need to take this out?

                # Otherwise get links in page as successors
                try:
                    succList = wikipedia.page(curr_node[0], auto_suggest=False).links
                except Exception as e:
                    print(e)

                # add each link into queue
                # And check if link is already in explored set to
                for succ in succList:
                    if (succ not in srcExplored):
                        succNodePath = curr_node[1].copy()
                        succNodePath.append(succ)
                        succNode = (succ, succNodePath)
                        srcFrontier.put(succNode)
                        srcFrontierHistory.put(succNode)

        ###### Backwards BFS #####
        if dstFrontier.empty() is False:
            curr_node = dstFrontier.get()

            # If a link has been explored before, continue.
            # This happens when a link is added multiple times to the
            # queue by different pages.
            if (curr_node[0] not in dstExplored):

                # Explore the link by adding to explored set
                dstExplored.append(curr_node[0])

                # Test if link is destination
                # print("dest_curr_node: ", curr_node)

                # if link is in src queue
                inSrcQueue = False                
                for node in srcFrontierHistory.queue:
                    if node[0] == curr_node[0]:
                        inSrcQueue = True
                # print("inSrcQueue:", inSrcQueue)
                if inSrcQueue is True:
                    while srcFrontierHistory.empty() is False:
                        srcNode = srcFrontierHistory.get()
                        if srcNode[0] == curr_node[0]:
                            # print("srcNode[1]", srcNode[1], "| curr_node[1]", curr_node[1])
                            curr_node[1].pop()
                            curr_node[1].reverse()
                            return srcNode[1] + curr_node[1]

                # Get links in page as successors
                try:
                    succList = wikipedia.page(curr_node[0], auto_suggest=False).links
                except Exception as e:
                    print(e)

                # add each link into queue
                # And check if link is already in explored set to
                for succ in succList:
                    if (succ not in dstExplored):
                        succNodePath = curr_node[1].copy()
                        succNodePath.append(succ)
                        succNode = (succ, succNodePath)
                        dstFrontier.put(succNode)
                        dstFrontierHistory.put(succNode)
                        
    # if both queue empty
    return None