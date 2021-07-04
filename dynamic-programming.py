"""
Student ID: 31190863

This module consists of functions best_schedule and best_itinerary for FIT2004 Assignment 2 and 
several helper functions.
This module is structured in a way the main functions are displayed first followed by their helper 
functions (if any).
"""

# Task 1
def best_schedule(weekly_income, competitions):
    """ 
    This function takes in a list of income earned by a trainer working, and a list of competitions 
    and calculates the maximum he/she can earn from a combination of working and competing. To keep
    track of the maximum attainable each week, use a memory array, salary. salary[i] will contain
    the optimal income after considering incomes and winnings from week 0 to week i. The final item 
    in the list will contain the maximum income attainable after considering all week incomes and 
    competitions.
    :input: weekly_income(list of income from trainer work where weekly_income[i] is earned on week 
            i), competitions(list of tuples where each tuple consists of integers representing 
            starting week and ending week of competition as well as winnings earned from competing
            in that order)
            A is length of weekly_income; B is length of competitions; N = A+B
    :output: maximum profit attainable from working as a trainer and competing (final element in 
             salary)
    :time complexity: best & worst: O(N) because the nested for loops run in N time regardless of 
                      input
                      Calculation: O(A) + O(B) + O(A+B) = O(A+B) = O(N)
    :aux space complexity: O(N) because weekly_comp takes O(A+B) space and salary takes O(A) space
                           to store optimal income; potential_income takes O(B) space;
                           end_time, start_time, comp, current_max, prev_max_income store single 
                           values
                           Calculation: O(A+B) + O(A) + O(B) + O(1) = O(A+B) = O(N)
    :space complexity: input takes O(N) space
                       Calculation: O(N) + aux space = O(N) + O(N) = O(N)
    """
    # start with a base case of income = 0 (consider this week -1)
    salary = [0]
    # group competitions by end times 
    # weekly_comp[i][2] consists of competitions ending in week i
    weekly_comp = [[] for _ in range(len(weekly_income))] # runs in O(A) time
    for comp in competitions: # runs in O(B) time
        end_time = comp[1]
        if end_time > len(weekly_income)-1:
            continue
        weekly_comp[end_time].append(comp)
    # loop runs in O(A+B) = O(N) time
    for i in range(len(weekly_income)): # runs in O(A) time
        current_max = salary[-1] 
        comps = weekly_comp[i] # competitions ending at that week
        if len(comps) > 0: # if there are competitions, we need to consider them
            # income if work in week i
            potential_income = current_max+weekly_income[i]
            for comp in comps: # runs in O(B) time
                start_time = comp[0]
                end_time = comp[1]
                winnings = comp[2]
                # get optimal income before start week of the competition
                # since there is an extra element in salary (base case), no need to access 
                # start_time-1, just start_time
                prev_max_income = salary[start_time]
                # save new total if competing gives a higher income
                if winnings+prev_max_income > potential_income:
                    potential_income = winnings+prev_max_income
            # add highest income earned from working or attending competitionsthat week
            salary.append(potential_income) 
        # if no competiton ends that week, optimal is to work that week
        else:
            salary.append(current_max+weekly_income[i])
    return salary[-1]

# Task 2
def best_itinerary(profit, quarantine_time, home):
    """ 
    This function calculates the maximum profit a salesperson who is starting in a city, home, on 
    day 0, can make given the time constraint of quarantine which varies according to the city and
    travelling (1 day). The profit is calculated backward from the last to the first day where the
    the day after the last day is the base case in which the salesperson earns 0 regardless of the 
    city he/she is in. Note that "transit" in this function and helper functions refer to salesperson
    passing by a city which allows them to skip quarantine in that city.
    :input: profit(matrix of values where profit[b][c] means the profit that can be earned in day b 
            in city c) of length d (also the number of days) with each nested list being length n
            (also the number of cities), 
            quarantine_time(list of days needed to quarantine in each city) of length n , home(an 
            integer indicating the start city of the salesperson)   
    :output: an integer representing the maximum profit possible for a salesperson starting in city 
             n where n is home on day 0
    :time complexity: best & worst: O(nd) because operations in the for loops (transit_cities, 
                      travel_left, travel_right and max) take constant time
                      Calculation: O(d) + O((nd)*1) = O(nd)
    :aux space complexity: O(nd) where d is the number of days and n is the number of cities because 
                           a memory matrix, memo of size nd is used to store the optimal profits at 
                           each day in each city;
                           transit, right_city, left_city and remain_in store single values
                           Calculation: O(nd) + O(1) = O(nd)
    :space complexity: O(nd) since input profit takes n*d space
                       Calculation: O(nd) + aux space = O(nd) + O(nd) = O(nd)
    """
    # initialise and create a memory list of size profit but with an extra nested 
    # list appended at the end (serves as the base case)
    memo = []
    for _ in range(len(profit)+1): # runs in O(d) time
        memo.append([0]*len(quarantine_time))
    # loop through from the last day up
    for i in range(len(memo)-2, -1, -1): # runs in O(d) time
        for j in range(len(memo[i])): # runs in O(n) time
            # find the best profit when salesperson transit cities
            transit = transit_cities(i, j, quarantine_time, memo, profit) # runs in O(1) time
            if j < len(quarantine_time)-1: # can travel right if it is not the rightmost city
                right_city = travel_right(i, j, quarantine_time, memo) # runs in O(1) time
            if j > 0: # can travel left if it is not the leftmost city
                left_city = travel_left(i, j, quarantine_time, memo) # runs in O(1) time
            # calculate profit if salesperson did not travel and worked in the current city
            remain_in = memo[i+1][j]+profit[i][j]
            # calculate profit if salesperson did travel
            if j == 0:
                # look to the right city only to find highest profit
                memo[i][j] = max([right_city, transit, remain_in]) # runs in O(1) time
            elif j == len(quarantine_time)-1:
                # look to the left city only to find highest profit  
                memo[i][j] = max([left_city, transit, remain_in]) # runs in O(1) time
            else:
                # look to the right and left city to find highest profit
                memo[i][j] = max([left_city, right_city, transit, remain_in]) # runs in O(1) time
    return memo[0][home]

# helper function for best_itinerary
def travel_left(i, j, quarantine_time, memo):
    """ 
    This function finds the total profit attainable when the salesperson decides to travel to 
    city j-1 on day i. The first day the salesperson is able to work in city j-1 if he/she is 
    in city j on day i is:
        first day = i + quarantine time in city j-1 + travel time
    :input: i(day), j(city), quarantine_time(list of days needed to quarantine in each city of 
            length n), 
            memo(memory containing of profit from "the future" to be reused of length d)
    :output: total profit including first day salesperson can work in city j-1 or -1 if
             indices are not valid (ie exceeding the days or cities in memo)
    :time complexity: best & worst: O(1) because all elements are accessed by their indices
    :aux space complexity: O(1) because new_i and val hold single values
    :space complexity: O(nd) due to the memo matrix
                       Calculation: O(nd) + aux space = O(nd)
    """
    # make sure indices is valid when called by valid_transit
    if i >= len(memo)-1 or j <= 0:
        return -1
    # first day able to work in city on the left (including quarantine and travel time)
    new_i = i + quarantine_time[j-1] + 1
    # if the new_i exceeds the number of days then do not consider it
    if (new_i) >= len(memo):
        return -1
    val = memo[new_i][j-1]
    return val

# helper function for best_itinerary
def travel_right(i, j, quarantine_time, memo):
    """ 
    This function finds the total profit attainable when the salesperson decides to travel to 
    city j+1 on day i. The first day the salesperson is able to work in city j-1 if he/she is 
    in city j on day i is:
        first day = i + quarantine time in city j+1 + travel time
    :input: i(day), j(city), quarantine_time(list of days needed to quarantine in each city of 
            length n), 
            memo(memory containing of profit from "the future" to be reused of length d)
    :output: total profit including first day salesperson can work in city j+1 or -1 if
             indices are not valid (ie exceeding the days or cities in memo)
    :time complexity: best & worst: O(1) because all elements are accessed by their indices
    :aux space complexity: O(1) because new_i and val hold single values
    :space complexity: O(nd) due to the memo matrix
                       Calculation: O(nd) + aux space = O(nd)
    """
    # make sure indices is valid when called by valid_transit
    if i >= len(memo)-1 or j >= len(quarantine_time)-1:
        return -1
    # first day able to work in city on the right (including quarantine and travel time)
    new_i = i + quarantine_time[j+1] + 1
    # if the new_i exceeds the number of days then do not consider it
    if (new_i) >= len(memo):
        return -1
    val = memo[new_i][j+1]
    return val

# helper function for best_itinerary
def transit_cities(i, j, quarantine_time, memo, base_profit):
    """
    This function finds the maximum total profit attainable if the salesperson were to transit 
    one or more cities in which quarantine is not needed in the transit city. Possible transit 
    routes are to the cities on the left and right except when salesperson is in the leftmost 
    or rightmost city in which there is only one route. A valid transit can occur when the value 
    in memo[i+1][j+1] must be larger than the current memo[i][j] value and the value in 
    memo[i+1][j+1] must come from another city other than j+1. Transitting one city only consists 
    of a day of travel which is why the value at the current position is compared to the ones 
    in the left and right city on day i+1
    :input: i(day), j(city), quarantine_time(list of days needed to quarantine in each city of 
            length n), 
            memo(memory containing of profit from "the future" to be reused of length d),
            base_profit(list of profit earned in each city on each day)
    :output: maximum total profit if salesperson were to transit cities - if no transit results 
             in a larger profit, function returns -1
    :time complexity: best & worst: O(1) because valid_transit and accessing elements by indices 
                      runs in constant time
                      Calculation: O(1) + O(1) = O(1)
    :aux space complexity: O(1) because valid_transit uses O(1) and max_profit, profit store a 
                           single values
    :space complexity: O(nd) due to the memo matrix
                       Calculation: O(nd) + aux space = O(nd)
    """
    max_profit = -1
    # salesperson is not in the rightmost city
    if j < len(quarantine_time)-1:
        # compare current value and one in potential transit city 
        if memo[i+1][j+1] > memo[i][j]:
            # check if value is part of a valid transit
            profit = base_profit[i+1][j+1]
            if valid_transit(i+1, j+1, quarantine_time, memo, profit): # runs in O(1) time
                if memo[i+1][j+1] > max_profit:
                    max_profit = memo[i+1][j+1]
    # salesperson is not in the leftmost city
    if j > 0:
        # compare current value and one in potential transit city
        if memo[i+1][j-1] > memo[i][j]:
            # check if value is part of a valid transit
            profit = base_profit[i+1][j-1]
            if valid_transit(i+1, j-1, quarantine_time, memo, profit): # runs in O(1) time
                if memo[i+1][j-1] > max_profit:
                    max_profit = memo[i+1][j-1]   
    return max_profit

# helper function for best_itinerary
def valid_transit(i, j, quarantine_time, memo, profit):
    """
    This function checks whether the value at memo[i][j] comes from a valid transit or can be 
    part of a valid transit. A valid transit fulfils one of two conditions:
        1. Value at memo[i][j] is the value from having worked in an adjacent city after travel 
           and quarantine
        2. Value at memo[i][j] is the value taken from another valid transit in city j+1 or j-1 
           on day i+1
    To check for 1, the function calls travel_left and/or travel_right and compares with memo[i][j].
    To check for 2, the function checks if the value in memo[i][j] is from working in city j or 
    part of a valid transit
    :input: i(day), j(city), quarantine_time(list of days needed to quarantine in each city of length n), 
            memo(memory containing of profit from "the future" to be reused of length d), 
            profit(value of profit made on day i in city j)
            Note: memo[i][j] is the optimal profit on the first day of a potential transit
            For example, to get optimal profit for memo[3][4], transit_cities calls this function
            with values i=4 and j=5 to check if memo[4][5] can be or is part of a valid transit. 
    :output: true if transitting cities, travelling to and quarantining in the final city gives
             the salesperson the maximum profit; false otherwise
    :time complexity: best & worst: O(1) because travel_left, travel_right and accessing elements is 
                      done in constant time
                      Calculation: O(1) + O(1) = O(1) 
    :aux space complexity: O(1) because valid, right_city, left_city and transit store only single 
                           values
    :space complexity: O(nd) due to the memo matrix
                       Calculation: O(nd) + aux space = O(nd)
    Note: variable transit is a boolean to ensure that value came from a valid set of transits ending 
          in a city if multiple transits are needed;
          memo[i][j] != memo[i+1][j]+profit is to check whether the value memo[i][j]
          came from working in that city (for a valid transit, this should be true)
    """
    valid = False
    left_city = travel_left(i, j, quarantine_time, memo) # runs in O(1) time
    right_city = travel_right(i, j, quarantine_time, memo) # runs in O(1) time
    # salesperson is not in the rightmost city
    if j >= 1 and j <= len(quarantine_time)-2:
        transit = memo[i+1][j+1] == memo[i][j] and memo[i][j] != memo[i+1][j]+profit
        if left_city == memo[i][j] or right_city == memo[i][j] or transit:
            valid = True
    # salesperson is not in the leftmost city
    if j >= 0 and j <= len(quarantine_time)-1:
        transit = memo[i+1][j-1] == memo[i][j] and memo[i][j] != memo[i+1][j]+profit
        if left_city == memo[i][j] or right_city == memo[i][j] or transit:
            valid = True
    return valid