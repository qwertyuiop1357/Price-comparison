"import the files"
actual = "./input/actual.txt"
predicted = "./input/predicted.txt"
window = "./input/window.txt"
output = "./output/comparison.txt"

def window_length(window):
    """this function reads window.txt to get the length of the slide window"""
    f = open(window, 'r')
    window_length = f.readline()
    window.close()
    return int(window_length)


def error(actual, predicted):
    """this function computes the difference of values between common keys in actual and predicted.
    
    actual: dictionary, keys: stock ID, values: price
    predicted: dictionary, keys: stock ID, values: price
    num: int, number of common keys
    error_sum: float, total sum of differences for all common keys
    """
    comp = {}
    if predicted is None or actual is None:
        error_info = [0,0]
        return error_info
    
    for i in predicted:
        if i in actual:
            comp[i] = abs(actual[i] - predicted[i])
    
    num, error_sum = 0, 0
    for j in comp:
        num += 1 
        error_sum += comp[j]
        
    return [num, error_sum]


def update_error(error_info, pop, append):
    """This function updates the total error in the window
    error_info: [num, error_sum], records the total number of stock IDs
    and total differences of prices in the window
    pop: the [num, error] that is be removed from the window
    append: the [num, error_sum] that is added to the window
    """
    num = error_info[0]
    error_sum = error_info[1]
    num = num - pop[0] + append[0]
    error_sum = error_sum - pop[1] + append[1]
    update_error = [num, error_sum]
    return update_error

def process(string):
    """read the .txt file and process it to a list"""
    if not string:
        return []
    
    s = string.split("|")
    s[2] = s[2].strip()
    s[0] = int(s[0])
    s[2] = float(s[2])
    return s

import collections

def average_difference(actual, predicted, window, output):
    """This function reads the files line by line and writes the average difference to the output file"""
    actual = open(actual, 'r')
    predicted = open(predicted, 'r')
    output = open(output,"w")
    
    # no_data records the number of consecutive time that do not records"
    length = window_length(window)
    slide_window = collections.deque([[0,0] for i in range(length)], length)
    error_sum = [0,0]
    no_data = 0
 
    # stop_1 and stop_2 records if searching for certain time ends
    time = 1
    stop_1 = False
    stop_2 = False
    
    # read file line by line then record the stock ID and prices for certain time
    while True:
        hashset = {}
        if not stop_1:
            x = actual.readline()
        if not x:
            break
        stop_1 = False
        while(stop_1 == False and x):
            line = process(x)
            if line[0] != time:
                stop_1 = True
                break
            hashset[line[1]] = line[2]
            x = actual.readline()     

        hashset_2 = {}
        if not stop_2:
            y = predicted.readline()
        if not y:
            break
        stop_2 = False
        while(stop_2 == False and y):
            line = process(y)
            if line[0] != time:
                stop_2 = True
                break
            hashset_2[line[1]] = line[2]
            y = predicted.readline()     
       
        # compute the total differences during this time period
        error_info = error(hashset, hashset_2)
        
        # If no data for the whole slide window, write "NA"
        if error_info[0] == 0:
            no_data += 1
        else:
            no_data = 0
        pop = slide_window.popleft()
        error_sum = update_error(error_sum, pop, error_info)
        slide_window.append(error_info)
        
        # write the average differences in the output file
        if time >= length:
            start_time = time - length + 1
            if no_data >= length:
                output.write(str(start_time) + '|' + str(time) + '|' + 'NA' + '\n')
            
            if error_sum[0] == 0:
                average = "%.2f" % 0
                output.write(str(start_time) + '|' + str(time) + '|' + average + '\n')

            if error_sum[0] != 0:   
                average = error_sum[1] / error_sum[0]
                average = "%.2f" % average
                output.write(str(start_time) + '|' + str(time) + '|' + average + '\n')

        time += 1

    actual.close()
    predicted.close()
    output.close()

   
if __name__ == "__main__":
    average_difference(actual, predicted, window, output)



        
