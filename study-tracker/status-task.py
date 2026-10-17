def status_task():
  while True:
    status_name = input("Enter the name of task to change status: ").lower()
    if status_name not in tasks:
      print("Task is not inside the folder.")
      continue
    else:
      break

  while True:
    change = input("Would you like to change the task status (yes/no): ").lower()
    if change != "yes" or change != "no":
      print("Please indicate correctly. Input should be 'yes' or 'no'. ")
      continue
    else:
      break
  if change == "yes":
    if tasks[status_name][3] == "incomplete":
      tasks[status_name][3] == "completed"
    else:
      tasks[status_name][3] == "incomplete"
  print(f" Task: {view_name}. \n Status: {tasks[view_name][3]}. \n Priority: {tasks[view_name][0]}. \n Due data: {tasks[view_name][1]}. \n Description: {tasks[view_name][2]}")

