
# coding: utf-8

# In[75]:

data_list = ["dank","lulz","wow","amaze"]
print(data_list)
print(data_list[0])
print(data_list[2])
print ("")


# In[51]:


# can also append stuff to existing list 

for i in range(3):
    data_list[i]=data_list[i]+"666"
print (data_list)

# no need to have all data types same 

mix = ["dank",[666,69],1]
print (mix) 


# In[56]:

#accessing elements in the list
squares=[1,4,9,16,25,36]
print(squares)
print(squares[1:3])
print(squares[:])
print(squares[-2])    


# In[55]:

#looping through the list elements 
for value in squares:
    print("Element:",value)

print("")
    
#looping through the list elements and indices using enumerate 
for ind,value in enumerate(squares):
    print("Element:",ind, "-->",value)


# In[57]:

#dictionaries are denoted by curly braces , with items seperated by commas 
capitals = {'United States':'Washington DC','India':'New Delhi', 'Bangladesh':'Dhaka'}
#similar to lists , values here are accessed with a square bracket notation , but here , we will use a key 
#very important to understand the concept of key value pairs 
capitals['India']

# add an item 
capitals['Spain']='Madrid'

print(capitals)

print("")
#if you want to see if a key value exists or not , 
print('India' in capitals) #gives you a true / false value as output 


# In[36]:

#now say you want to create another dictionary with more capitals 
morecapitals = {'Germany':'Berlin','UK':'London','France':'Paris','Netherlands':'Amstredam'}
morecapitals


# In[37]:

#update capitals and add morecapitals to it 
capitals.update(morecapitals)
capitals
# delete items using del and identifying them by their key 


# In[46]:

# looping in dictionaries 
# method 1 , just mention the key 
for key in capitals :
    print(key,capitals[key])

print("")    
    
# method 2 , be more explicit 

for key in capitals.keys():
    print (key)   # if you want only keys 

print ("")

for key in capitals.values():
    print(key) # if you want only values 

print("")

for key,value in capitals.items():
    print(key,"->",value)


# In[47]:

#comprehensions - more intuitive , easier to manipulate 


# In[49]:

squares = []  # create an empty list 
for i in range(10): 
    squares.append(i**2)
print(squares)
print("")


# In[58]:

# you also have the option of mentioning a condition inline . pretty neat . 

# go through first thirty numbers , choose the ones where % 3 == 0 and then square them
squares2 = [i**2 for i in range(30) if i%3 == 0] 
print(squares2)


# In[67]:

# now use this in a dict 
squares2_dict = {i: i**2 for i in range(30) if i%3 == 0}
print(squares2_dict)
print("")

for key in squares2_dict:
    print(key)


# In[74]:

# we are going to use capitals again 
capitals_bycapital = {capitals[key]: key for key in capitals}
print (capitals_bycapital)


# In[84]:

'''generator expressions -  we use this concept when you want to perform some kind of operations on the comprehension. 
Here , we will be getting the sum of the squares of numbers'''

# normally , we would do it like this 
print(sum([i**2 for i in range(10)]))

print("")

# we can do the same thing using a python generator 
# this would look very similar to the one above , just omit the brackets 
print(sum(i**2 for i in range(10)))

# the second method is way more efficient , can be used to save memory and time


# In[ ]:



