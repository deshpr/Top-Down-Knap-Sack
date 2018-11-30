
def backtrack_algorithm(memoized_results, item_count, capacity, all_values, all_weights, picked_items):
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

    if item_count == 0:
        return picked_items

    if all_weights[item_count - 1] > capacity:
        cost_after_item_is_picked = 0
    else:
        # If the item was picked.
        costNow = memoized_results[item_count][capacity]    
        capacity_before_if_item_was_picked = capacity - all_weights[item_count - 1] # this item's weight, with -1 for indexing.
        cost_before_if_item_was_picked = memoized_results[item_count - 1][capacity_before_if_item_was_picked]
        cost_after_item_is_picked = cost_before_if_item_was_picked + all_values[item_count - 1]

    # If Item was not picked
    cost_before_if_item_was_not_picked = memoized_results[item_count - 1][capacity]
    
    if(cost_after_item_is_picked > cost_before_if_item_was_not_picked):
        # this item was picked.
        picked_items.append(item_count) # this in a way is also an index here.
        picked_items = backtrack_algorithm(memoized_results, item_count - 1, capacity_before_if_item_was_picked, all_values, all_weights, picked_items)
    else:
        # nothing was picked.        
        picked_items = backtrack_algorithm(memoized_results, item_count - 1, capacity, all_values, all_weights, picked_items)    
    return picked_items



def knapsack_top_down_dp(all_values, all_weights, W):
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

    if len(all_weights) != len(all_values):
        raise Exception('Invalid. The count of the weights and values do not match')

    total_item_count = len(all_values)

    # Total rows = # of items
    # Total columns = # possible weight.
        
    print("Matrix dimensions:{} X {}".format(len(all_weights) + 1, W + 1))
    memoized_results = get_memoizing_matrix(len(all_weights) + 1, W + 1)
    optimal_cost = knapsack(all_values, all_weights, memoized_results, len(all_weights), W)
    print("Optimal cost = {}".format(optimal_cost))
    print("Final matrix")
    print_matrix(memoized_results)
    picked_items = []
    picked_items = backtrack_algorithm(memoized_results, total_item_count, W, all_values, all_weights, picked_items)
    picked_items = list(reversed(picked_items))
    picked_items = [el - 1 for el in picked_items]
    return optimal_cost, picked_items


def knapsack(all_values, all_weights, memoized_results, n, C):
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

    if(memoized_results[n][C] != -1):
        return memoized_results[n][C]

#    print("Weight of this item= {}".format(allWeights[n - 1]))
    
    remaining_weight = C - all_weights[n-1]
#    print("Remaining weight = {}".format(remainingWeight))
#    print("Making the take the recursive call")

    if(remaining_weight < 0):
        consider_item = 0
        memoized_results[n][C] = 0
    else:
        consider_item = all_values[n - 1] + knapsack(all_values, all_weights, memoized_results, n-1, remaining_weight)

#    print("making the do not take recursive call")
    do_not_consider_item = knapsack(all_values, all_weights, memoized_results, n-1, C)
    
    memoized_results[n][C] = max(consider_item, do_not_consider_item)

    # The capacity of the bag is the same, we just take the next item.   
#    print("Chose between {} and {}".format(considerItem, doNotConsiderItem))
#    print("initialize {},{} to {}".format(n,C,memoizedResults[n][C]))

    return memoized_results[n][C]


def get_memoizing_matrix(rows, columns):
    """Creates the matrix (list of lists)  that can be used to store the answers to recursive calls made by the top-down dynamic programming
        approach for knapsack.

        Args:
            rows (int): The number of rows that the matrix can have.
            columns (int): The number of columns that the matrix can have.

        Returns:
            list[list]: A 2-d matrix, represented as a list of lists that has the indicated rows and columns.
    """

    matrix = [[0 for column in range(columns)]for row in range(rows)]
    for row_position in range(len(matrix)):
        for column_position in range(len(matrix[row_position])):
            matrix[row_position][column_position] = 0 if row_position == 0 or column_position == 0 else -1
    return matrix

def print_matrix(matrix):
    """Prints the matrix. Used for debugging.

        Args:
            Matrix (list[list]): A matrix (represented as a list of lists).

    """

    print("\n\n")
    for row_position in range(len(matrix)):
        to_print = ""
        for column_position in range(len(matrix[row_position])):
            to_print = to_print + "      " +  str(matrix[row_position][column_position])
        print(to_print)
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

    values = [1, 1, 1, 5]
    weights = [4, 7, 8, 10]
    W = 13

    weights = [23, 21, 29, 44, 53, 38, 63, 85, 89, 82]
    values =  [92, 57, 49, 68, 60, 43, 67, 84, 87, 72]
    W = 165

    weights = [31,10,20,19,4,3,6]
    values =  [70,20,39,37,7,5,10]
    W = 50

    weights = [25,35,45,5,25,3,2,2]
    values =  [350,400,450,20,70,8,5,5]
    W = 104

    weights = [12,7,11,8,9]
    values =  [24,13,23,15,16]
    W = 26

    
    weights = [56,59,80,64,75,17]
    values =  [50,50,64,46,50,5]
    W = 190

    weights = [41,50,49,59,55,57,60]
    values =  [442,525,511,593,546,564,617]
    W = 170

#    weights = [382745,799601,909247,729069,467902,44328,34610,698150,823460,903959,853665,551830,610856,670702,488960,951111,323046,446298,931161,31385,496951,264724,224916,169684]
#    values =  [ 825594,1677009,1676628,1523970,943972,97426,69666,1296457,1679693,1902996,1844992,1049289,1252836,1319836,953277,2067538,675367,853655,1826027,65731,901489,577243,466257,369261]
#    W = 6404180


    print("Here are the indices of the items that are selected")
    optimal_cost, indices = knapsack_top_down_dp(values, weights, W)
    print("Optimal cost = {}".format(optimal_cost))
    print("Indices = {}".format(indices))

main()



