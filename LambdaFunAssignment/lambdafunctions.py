from functools import reduce

# 1question
fruits= ['apple', 'banana', 'cherry', 'date', 'elderberry']

fruits_filter=list(filter(lambda x:len(x)>5,fruits))

print(fruits_filter)

#2nd question
numbers=[2, 4, 6, 8, 10]

numbers_double=list(map(lambda x:x*2,numbers))
product_double=reduce(lambda x,y:x*y,numbers_double)
print(product_double)