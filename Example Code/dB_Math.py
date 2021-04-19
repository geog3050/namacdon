# decibel Math Calc

import math
db = 0
ln = 0

choice = input("Type 1 to convert from decibels or 0 from linear: ")

if choice:
    db = input("Enter decibel value to convert: ")
    db = int(db)
    answer = 10**(db/10)
else:
    ln = input("Enter linear value to convert: ")
    ln = int(ln)
    answer = math.log10(ln)*10
    
print(answer)

