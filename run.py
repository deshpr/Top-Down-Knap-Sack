
def backtrackAlgorithm(memoizedResults, itemCount, capacity, allValues, allWeights, picked_items):
    """Performs backtracking to return the actual list of items that were picked by the knapsack problem.

        Args:
            memoized_results(list[list]): A 2-d matrix, represented as a list of lists, that has the results of applying the knapsack algorithm top down. The number of rows in 
                this matrix are the number of items  + 1, and the number of columns are equal to the total capacity  + 1.
            itemCount (int): The total number of items at this instance.
            capacity (int): The capacity at this instance.
            all_values (list): A list of integer values representing the values of the items
            allWeights (list): A list of integer values representing the weights of the items.
            picked_items (list): A list of indices indicating the items the knapsack program has picked so far.

        Returns:
            list: The set of indices representing the items that were picked and form the optimal subset.
    """

    if itemCount == 0:
        return picked_items

    if allWeights[itemCount - 1] > capacity:
        costAfterItemIsPicked = 0
    else:
        # If the item was picked.
        costNow = memoizedResults[itemCount][capacity]    
        capacityBeforeIfItemWasPicked = capacity - allWeights[itemCount - 1] # this item's weight, with -1 for indexing.
        costBeforeIfItemWasPicked = memoizedResults[itemCount - 1][capacityBeforeIfItemWasPicked]
        costAfterItemIsPicked = costBeforeIfItemWasPicked + allValues[itemCount - 1]

    # If Item was not picked
    costBeforeIfItemWasNotPicked = memoizedResults[itemCount - 1][capacity]
    
    if(costAfterItemIsPicked > costBeforeIfItemWasNotPicked):
        # this item was picked.
        picked_items.append(itemCount) # this in a way is also an index here.
        picked_items = backtrackAlgorithm(memoizedResults, itemCount - 1, capacityBeforeIfItemWasPicked, allValues, allWeights, picked_items)
    else:
        # nothing was picked.        
        picked_items = backtrackAlgorithm(memoizedResults, itemCount - 1, capacity, allValues, allWeights, picked_items)    
    return picked_items



def knapsack_top_down_dp(allValues, allWeights, W):
    """Implements knapsack problem using the top down dynamic programming approach, calculating both the optimal cost as well as the indices of the items
        that form the optimal subset.

        Args:
            allValues (list): A list that represents the values of the all items.
            allWeights (list): A list that represents the weights of all the items.
            W (int): The total capacity of the knapsack.

        Returns:
            int: The optimal value (cost) that we can have given the input knapsack of capacity W, and the input weights and their individual values.
            list: A list of indices, representing the optimal set of items that represent the optimal subset. 
    """
    totalItemCount = len(allValues)

    # Total rows = # of items
    # Total columns = # possible weight.

    print("Matrix dimensions:{} X {}".format(len(allWeights) + 1, W + 1))
    memoizedResults = get_memoizing_matrix(len(allWeights) + 1, W + 1)
    optimal_cost = knapsack(allValues, allWeights, memoizedResults, len(allWeights), W)
    print("Optimal cost = {}".format(optimal_cost))
    print("Final matrix")
    print_matrix(memoizedResults)
    picked_items = []
    picked_items = backtrackAlgorithm(memoizedResults, totalItemCount, W, allValues, allWeights, picked_items)
    picked_items = list(reversed(picked_items))
    picked_items = [el - 1 for el in picked_items]
    return optimal_cost, picked_items


def knapsack(allValues, allWeights, memoizedResults, n, C):
    """Implement the knapsack algorith, using the top-down dynamic programming approach. 

        Args:
            allValues (list): A list that represents the values of the all items.
            allWeights (list): A list that represents the weights of all the items.
            memoizedResults (list[list]): A matrix (represented as a list of lists) that has the memoized results (and is therefore used to store
                the results of the recursion).
            n (int): The number of items present at this instance of the problem for which knapsack is called.
            C (int): The capacity of the knapsack at this instance of the problem for which knapsack is called.

        Returns:
            int: The optimal value (cost) that we can have given the n items and a knapsack of capacity C.
    """

#    print("calling for n = {}, C = {}".format(n, C))
    # A situation in the recursive tree wherein no elements are left
    # or the weight of the bag would become 0.
    if n<0 or C <= 0:
        return 0    

    if(memoizedResults[n][C] != -1):
        return memoizedResults[n][C]

#    print("Weight of this item= {}".format(allWeights[n - 1]))
    
    remainingWeight = C - allWeights[n-1]
#    print("Remaining weight = {}".format(remainingWeight))
#    print("Making the take the recursive call")

    if(remainingWeight < 0):
        considerItem = 0
        memoizedResults[n][C] = 0
    else:
        considerItem = allValues[n - 1] + knapsack(allValues, allWeights, memoizedResults, n-1, remainingWeight)

#    print("making the do not take recursive call")
    doNotConsiderItem = knapsack(allValues, allWeights, memoizedResults, n-1, C)
    
    memoizedResults[n][C] = max(considerItem, doNotConsiderItem)

    # The capacity of the bag is the same, we just take the next item.   
#    print("Chose between {} and {}".format(considerItem, doNotConsiderItem))
#    print("initialize {},{} to {}".format(n,C,memoizedResults[n][C]))

    return memoizedResults[n][C]


def get_memoizing_matrix(rows, columns):
    """Creates the matrix (list of lists)  that can be used to store the answers to recursive calls made by the top-down dynamic programming
        approach for knapsack.

        Args:
            rows (int): The number of rows that the matrix can have.
            columns (int): The number of columns that the matrix can have.

        Returns:
            list[list]: A 2-d matrix, represented as a list of lists that has the indicated rows and columns.
    """

    Matrix = [[0 for column in range(columns)]for row in range(rows)]
    for rowPosition in range(len(Matrix)):
        for columnPosition in range(len(Matrix[rowPosition])):
            Matrix[rowPosition][columnPosition] = 0 if rowPosition == 0 or columnPosition == 0 else -1
    return Matrix

def print_matrix(Matrix):
    """Prints the matrix. Used for debugging.

        Args:
            Matrix (list[list]): A matrix (represented as a list of lists).

    """

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
#    W = 8

#    values = [1,4,5,7]
#    weights = [1,3,4,5]
#    W = 7

    values = [10, 16, 8, 25]
    weights = [4, 7, 8, 10]
    W = 13

#    values = [1, 1, 1, 5]
#    weights = [4, 7, 8, 10]
#    W = 13
    

    print("Here are the indices of the items that are selected")
    optimal_cost, indices = knapsack_top_down_dp(values, weights, W)
    print("Optimal cost = {}".format(optimal_cost))
    print("Indices = {}".format(indices))

main()



