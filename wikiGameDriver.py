import search
import time

startTime = time.time()
startPage = "Everything Everywhere All at Once"
destPage = "Nihilism"
finalPath  = search.wikiGameDFS(startPage, destPage)
timeTaken = round(time.time()-startTime, 1)

print("The found shortest path between", startPage, "and", destPage, "is: ")
print(finalPath)
print("It took", timeTaken, "seconds")