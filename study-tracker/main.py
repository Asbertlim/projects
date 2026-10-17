tasks = {}

print("=================================================")
print("           Welcome Learner                      ")
print("=================================================")

print("")
print(" 1. Add Task\n 2. Delete Task\n 3. View Task\n 4. Check Task Status")

while True:
  choice = input("What would you like to do today: ")
  if choice == "1":
    add_task()
  elif choice == "2":
    del_task()
  elif choice == "3":
    view_task()
  elif choice == "4":
    status_task()
  else:
    print("Incorrect input. Please try again.")
    continue

  end = input("Would you like to end here (yes/no): ").lower()
  if end == "yes":
    print("Thank you for visiting. See you soon.")
    break
  elif end == "no":
    continue
  else:
    print("Incorrect input.")
    continue
