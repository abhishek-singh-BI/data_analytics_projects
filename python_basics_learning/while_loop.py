# While Loop: Execute some code WHILE some condition is true.

# Pandas not needed, just added to check package installation in the right python env
# import pandas as pd

# A while loop is an if statement but with infinite loop until the condition is met
# age = int(input("Please Enter your Age: "))

# if age <= 0:
#     print(f"{age} is less than zero. Invalid Age")
# else:
#     print(f"Age is: {age}")


# Lets convert the above in a while loop

age = int(input("Please enter your age: "))

while age <= 0:
    print("Age cannot be negative!")
    # now reassign age input so that the while loop has an exit strategy :)
    age = int(input("Please enter your age: "))
    print(f"Age is: {age}")
