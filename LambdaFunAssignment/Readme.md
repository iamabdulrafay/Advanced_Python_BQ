# Python Lambda Functions and Functional Programming

This project demonstrates the use of Python lambda functions and functional programming techniques such as `filter`, `map`, and `reduce`. Two primary tasks are performed:

1. Filtering a list of strings to only include those with more than 5 characters.
2. Doubling each number in a list and then finding the product of the doubled numbers.

## Tasks

### Task 1: Filter Strings by Length

Given a list of strings, use the `filter` function and a lambda function to create a new list that contains only the strings with more than 5 characters.

**Input:**

```python
fruits = ['apple', 'banana', 'cherry', 'date', 'elderberry']
fruits_filter = list(filter(lambda x: len(x) > 5, fruits))
print(fruits_filter)

##Expected Output:
['banana', 'cherry', 'elderberry']


# Task 2: Double Numbers and Find Product
## Given a list of numbers, use the map function and a lambda function to double each number. Then, use the reduce function to find the product of the doubled numbers.

numbers = [2, 4, 6, 8, 10]

from functools import reduce
numbers_double = list(map(lambda x: x * 2, numbers))
product_double = reduce(lambda x, y: x * y, numbers_double)
print(product_double)

##Expected Output:
122880



