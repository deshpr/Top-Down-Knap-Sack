
def backtrackAlgorithm(memoizedResults, itemCount, capacity, allValues, allWeights, picked_items):
    
    if itemCount == 0:
        return

    if allWeights[itemCount - 1] > capacity:
        return

    costNow = memoizedResults[itemCount][capacity]    
    # If the item was picked.
    capacityBeforeIfItemWasPicked = capacity - allWeights[itemCount - 1] # this item's weight, with -1 for indexing.
    costBeforeIfItemWasPicked = memoizedResults[itemCount - 1][capacityBeforeIfItemWasPicked]

    # If Item was not picked
    costBeforeIfItemWasNotPicked = memoizedResults[itemCount - 1][capacity]

    if(costBeforeIfItemWasPicked > costBeforeIfItemWasNotPicked):
        # this item was picked.
        picked_items.append(itemCount) # this in a way is also an index here.
        backtrackAlgorithm(memoizedResults, itemCount - 1, capacityBeforeIfItemWasPicked, allValues, allWeights, picked_items)
    else:
        # nothing was picked.
        backtrackAlgorithm(memoizedResults, itemCount - 1, capacity, allValues, allWeights, picked_items)    

def get_items_selected(memoizedResults, totalItemCount, totalCapacity, allValues, allWeights):
    picked_items = []
    backtrackAlgorithm(memoizedResults, totalItemCount, totalCapacity, allValues, allWeights, picked_items)
    return picked_items.reverse()

def knapsack(allValues, allWeights, memoizedResults, n, C):
    print("calling for n = {}, C = {}".format(n, C))
    # A situation in the recursive tree wherein no elements are left
    # or the weight of the bag would become 0.
    if n<0 or C <=0:
        return 0    

    if(memoizedResults[n][C] != -1):
        return memoizedResults[n][C]

    print("Weight of this item= {}".format(allWeights[n - 1]))
    
    remainingWeight = C - allWeights[n-1]
    print("Remaining weight = {}".format(remainingWeight))
    print("Making the take the recursive call")

    considerItem = 0 if remainingWeight < 0 else allValues[n - 1] + knapsack(allValues, allWeights, memoizedResults, n-1, remainingWeight)

    print("making the do not take recursive call")
    doNotConsiderItem = knapsack(allValues, allWeights, memoizedResults, n-1, C)
    
    memoizedResults[n][C] = max(considerItem, doNotConsiderItem)

    # The capacity of the bag is the same, we just take the next item.   
    print("Chose between {} and {}".format(considerItem, doNotConsiderItem))
    print("initialize {},{} to {}".format(n,C,memoizedResults[n][C]))

    return memoizedResults[n][C]


def get_memoizing_matrix(rows, columns):
    Matrix = [[0 for column in range(columns)]for row in range(rows)]
    for rowPosition in range(len(Matrix)):
        for columnPosition in range(len(Matrix[rowPosition])):
            Matrix[rowPosition][columnPosition] = 0 if rowPosition == 0 or columnPosition == 0 else -1
    return Matrix

def print_matrix(Matrix):
    print("\n\n")
    for rowPosition in range(len(Matrix)):
        toPrint = ""
        for columnPosition in range(len(Matrix[rowPosition])):
            toPrint = toPrint + "      " +  str(Matrix[rowPosition][columnPosition])
        print(toPrint)
    print("\n\n")


def main():
#    values = [2,4,6,9]
#    weights = [2,2,4,5]
#   W = 8

    values = [1,4,5,7]
    weights = [1,3,4,5]
    W = 7
    # Total rows = # of items
    # Total columns = # possible weight.
    print("Matrix dimensions:{} X {}".format(len(weights) + 1, W + 1))
    memoizedResults = get_memoizing_matrix(len(weights) + 1, W + 1)
    print("Initial Matrix")
    print_matrix(memoizedResults)
    

    optimal_cost = knapsack(values, weights, memoizedResults, len(weights), W)
    print("Optimal cost = {}".format(optimal_cost))
    print("Program complete. ")

    print("Final matrix")
    print_matrix(memoizedResults)

    print("Get items selected.")
    results = get_items_selected(memoizedResults, len(weights), W, values, weights)
    print(results)

main()



