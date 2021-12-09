import math

def binary_search(sorted_table, element):
   index = math.ceil(len(sorted_table) / 2)

   while element != sorted_table[index]:
      print("boo")
      if sorted_table[index] > element:
         index = math.ceil(index / 2)
      else:
         index = math.ceil(index + index / 2)

   return index

table = [1, 2, 3, 4, 5]

print(str(binary_search(table, 2)))

