import sys
import collections

actual = sys.argv[2] 
predicted = sys.argv[3]
window = sys.argv[1]
output = sys.argv[4]

def window_length(window):
    """this function reads window.txt to get the length of the slide window"""
    try:
        f = open(window, 'r')
    except:
        print("Cannot open window file")
    window_length = f.readline()
    if not window_length:
        raise ValueError("window file is empty")
    try:
        window_length = int(window_length)
        if window_length <= 0:
            raise ValueError
    except ValueError:
        print("window length is not an integer greater than 0")

    f.close()
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
    s[2] = float(s[2])
        
    s[0] = int(s[0])

    return s

def find_the_first_time(actual, predicted):
    try:
        actual = open(actual, 'r')
    except:
        print("Cannot open window file")
    try:
        predicted = open(predicted, 'r')
    except:
        print("Cannot open window file")
    x = actual.readline()
    y = predicted.readline()
    try:
        if not x and not y:
            raise ValueError
    except ValueError:
        print("actual file and predicted file are empty")
    line_1 = process(x)
    line_2 = process(y)
    if not x:
        time = line_2[0]
    elif not y:
        time = line_1[0]
    else:
        time = min(line_1[0], line_2[0])
    actual.close()
    predicted.close()
    return time



def average_difference(actual, predicted, window, output):
    """This function reads the files line by line and writes the average difference to the output file"""
    first_time = find_the_first_time(actual, predicted)
    try:
        actual = open(actual, 'r')
    except:
        print("Cannot open window file")
    try:
        predicted = open(predicted, 'r')
    except:
        print("Cannot open window file")
    try:
        output = open(output,"w")
    except:
        print("Cannot open window file")
    
    # no_data records the number of consecutive time that do not records"
    length = window_length(window)
    slide_window = collections.deque([[0,0] for i in range(length)], length)
    error_sum = [0,0]
    
 
    # stop_1 and stop_2 records if searching for certain time ends
    time = first_time
    stop_1 = False
    stop_2 = False
    
    # read file line by line then record the stock ID and prices for certain time
    while True:
        actual_dic = {}
        if not stop_1:
            x = actual.readline()
        stop_1 = False
        while(stop_1 == False):
            if not x:
                break
            line = process(x)
            if line[0] != time:
                stop_1 = True
                break
            actual_dic[line[1]] = line[2]
            x = actual.readline()     

        predicted_dic = {}
        if not stop_2:
            y = predicted.readline()
        stop_2 = False
        while(stop_2 == False):
            if not y:
                break
            line = process(y)
            if line[0] != time:
                stop_2 = True
                break
            predicted_dic[line[1]] = line[2]
            y = predicted.readline()     
        
        
        # compute the total differences during this time period
        error_info = error(actual_dic, predicted_dic)
        

        pop = slide_window.popleft()
        error_sum = update_error(error_sum, pop, error_info)
        slide_window.append(error_info)
        
        # write the average differences in the output file
        if time-first_time+1 >= length:
            start_time = time - length + 1
            
            # If there is no data, write "NA"
            if error_sum[0] == 0:
                output.write(str(start_time) + '|' + str(time) + '|' + 'NA' + '\n')

            if error_sum[0] != 0:   
                average = error_sum[1] / error_sum[0]
                average = "%.2f" % average
                output.write(str(start_time) + '|' + str(time) + '|' + average + '\n')

        time += 1
    
        if not x and not y:
            break
       

    actual.close()
    predicted.close()
    output.close()


if __name__ == "__main__":
    average_difference(actual, predicted, window, output)



        


