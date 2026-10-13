def del_task():
  del_name = input("Enter the name of the task to be removed: ").lower()
  del tasks[del_name]
  
