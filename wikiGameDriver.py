import search
import time

startTime = time.time()
startPage = "Everything Everywhere All at Once"
destPage = "Nihilism"
print("Searching for path between", startPage, "and", destPage)

# print("Starting a BFS search")
# finalPath  = search.wikiGameDFS(startPage, destPage)
# timeTaken = round(time.time()-startTime, 1)
# print("The found shortest path between", startPage, "and", destPage, "is: ")
# print(finalPath)
# print("It took", timeTaken, "seconds")

print("Starting a BFS search")
print(search.wikiGameAStar(startPage, destPage, search.numberOfSameCategoriesHeuristic))
timeTaken = round(time.time()-startTime, 1)
print("The found shortest path between", startPage, "and", destPage, "is: ")
# print(finalPath)
print("It took", timeTaken, "seconds")
