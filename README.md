# Data Engineering Coding Challenge

## Introduction
Given two files, "actual.txt" and "predicted.txt", we want to compute the average price differences for each slide window and print the result in a file called "comparison.txt". The length of the slide window is given in the file "window.txt". In the consideration of memory, we don't read the files in a time, but read them line by line. 

## Structure of the code
The code is composed of six functions: window_length(window), error(actual, predicted), update_error(error_info, pop, append),process(string), find_the_first_time(actual, predicted) and average_difference(actual, predicted, window, output).

### window_length(window)
- read the content of "window.txt" file.
- return the length for the slide window.

### error(actual, predicted)
actual: dictionary, keys: stock ID, values: price.
- it records the stock IDs and corresponding price in "actual.txt" file for certain time period.

predicted: dictionary, keys: stock ID, values: price
- it records the stock IDs and corresponding price in "predicted.txt" file for certain time period.

This function computes the total price differences for all common stock IDs in both actual and in predicted. It returns [num, error_sum].
num: int, denote the number of common stock IDs in both actual and predicted.
error_sum: float, denote the total price differences of all the common stock IDs.

### update_error(error_info, pop, append)
error_info: [num, error_sum], 
num: int, denote the number of stock IDs in the slide window period.
error_sum: float, denote the total price differences in the slide window period.

pop: [num, error_sum], num denoted the number of stock IDs for the time period that will be removed from the slide window, error_sum is the corresponding total price differences in that time period. It is the previously added element in the slide window and will be popped out.

append: [num, error_sum], num denoted the number of stock IDs for the time period that will be added to the slide window, error_sum is the corresponding total price differences. It is the newly-added element in the slide window.

### process(string)
string: the line that read from files. This function process the line in the file to a list. The first element of the list is the time, the second element is the stock ID, the third element is the price.

### find_the_first_time(actual, predicted)
actual: the "actual.txt" file.

predicted: file "predicted.txt" file.

This function is to find the starting time.

### average_difference(actual, predicted, window, output)
- open files
- initialize the slide window, no_data is used to record the number of consecutive time that there is no common stock IDs for actual and predicted.
- read the files line by line, for fixed time, load the data into the dictionaries recording the stock IDs and prices in "actual.txt" and "predicted.txt".
- compute the number of common stock IDs and total differences for this time period, record it as error_info.
- keep track of the number of consecutive time that do not have data.
- add error_info to the slide window. Pop out the previously added error_info and update the total price differenced in the slide window.
- write the average difference in the output file.
  - if the number of non-data time is more than the length of the slide window, print "NA".
  - if there is no data, print "0.00".
  - otherwise, calculate the average difference and print it.





