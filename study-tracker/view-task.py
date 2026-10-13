def view_task():
  print(tasks)

  while True:
    view_name = input("Enter the name of the task to view: ").lower()
    if view_name not in tasks:
      print("Task is not inside the folder.")
      continue
    else:
      break
  
  print(f" Task: {view_name}. \n Priority: {tasks[view_name][0]}. \n Due data: {tasks[view_name][1]}. \n Description: {tasks[view_name][2]}")
