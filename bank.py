#Task Discription:
#This project is a simple text-based banking system mplemented in Python. 
#It allows users to perform basic banking operations such as deposit, withdrawal, 
#and balance inquiry. The system reads account information from an input file, 
#where each account is identified by a unique ID and a balance. Users can 
#interact with the system by depositing money, withdrawing funds, and checking 
#their balance. Input validation is implemented to ensure that all amounts are 
#valid and positive. The system also allows changes to be saved back to the file, 
#ensuring that accounts information is persistent.


# I chose a dictionary because it provides efficient key-value mapping, where the key is 
# a unique account ID and the value is the account balance. Dictionaries are mutable, 
# which makes it easy to update balances when deposits or withdrawals occur.
accounts = {}
# using 'with' so that the file automatically will be closed
try:
  with open("input.txt", "r") as file: 
     for line in file:
        try:
          account_number, account_balance = line.split(' ')
          accounts[account_number] = float(account_balance)
        except ValueError: 
           print(f"Invalid data in line: {line}. Please check account ID and balance format.")

except FileNotFoundError: 
   print("Error: File was not found")
except Exception as e:
   print(f"An unexpected error occured: {e}")

# Deposits a specified amount into the account.
def deposit(name, amount):
   if name in accounts:
      if amount > 0:
        accounts[name] += amount
      else:
        print("The amount should be positive")
   else:
      print(f"This account: {name} does not exist in our System")
      
# Withdraws a specified amount from the account.
def withdraw(name, amount):
   if name in accounts:
     if amount > 0: 
       if accounts[name] >= amount:
         accounts[name] -= amount
       else:
         print(f"This account: {name} does not have this amount")
     else:
        print("The amount shoud be positive")
   else:
      print(f"This account: {name} does not exist in our System")

# Displays the balance of the specified account.
def balance(name):
   if name in accounts:
      print(f"The balance of {name} is {accounts[name]}")
   else:
      print(f"This account: {name} does not exist in our System")

# Saves updated account data back to the file.
def saveChanges():
   try:
      with open("input.txt", "w") as file:
         for account_number, account_balance in accounts.items():
            file.write(f"{account_number} {account_balance}\n")
         print("Accounts have been updated sucessfully.")
   except Exception as e:
      print(f"An error occured while writing on the file: {e}")
      

  
#testing
# Test Case 1: Deposit money into an existing account and check balance.
deposit("323E2", 500)
balance("323E2")

# Test Case 2: Withdraw money from an existing account and check balance.
withdraw("367Z3", 200)
balance("367Z3")

# Test Case 3: Withdraw more money than the available balance.
withdraw("321S2", 500.0)
balance("321S2")

# Test Case 4: Attempt to deposit into a non-existing account.
deposit("999XYZ", 100)

# Test Case 5: Check balance of an existing account.
balance("874A8")
#Save changes to the file
saveChanges()
