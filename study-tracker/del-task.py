def del_task():
  del_name = input("Enter the name of the task to be removed: ").lower()
  del tasks[del_name]
  save_task()
  print(f" Task: {view_name}. \n Status: {tasks[view_name][3]}. \n Priority: {tasks[view_name][0]}. \n Due data: {tasks[view_name][1]}. \n Description: {tasks[view_name][2]}")
