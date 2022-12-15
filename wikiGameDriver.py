from search import *
import time
from bidirectionalBFS import *

startTime = time.time()
startPage = "Artificial intelligence"
destPage = "Husky"
print("Searching for path between", startPage, "and", destPage)

# doesnt work
# startPage = "Everything Everywhere All at Once"
# destPage = "Royal Corps of Eritrean Colonial Troops"

print("Starting a BFS search")
finalPath  = wikiGameBFS(startPage, destPage)
timeTaken = round(time.time()-startTime, 1)
print("The found shortest path between", startPage, "and", destPage, "is: ")
print(finalPath)
print("It took", timeTaken, "seconds")

print("Starting a Astar search")
finalPath = wikiGameAStar(startPage, destPage, numberOfSameCategoriesHeuristic)
timeTaken = round(time.time()-startTime, 1)
print("The found shortest path between", startPage, "and", destPage, "is: ")
print(finalPath)
print("It took", timeTaken, "seconds")

print("Starting a biBFS search")
finalPath  = wikiGameBidirectionalBFS(startPage, destPage)
timeTaken = round(time.time()-startTime, 1)
print("The found shortest path between", startPage, "and", destPage, "is: ")
print(finalPath)
print("It took", timeTaken, "seconds")