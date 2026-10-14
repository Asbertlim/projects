def add_task():
  name = input("Enter task name: ").lower()

  while True:
    level = "123"
    priority = input("Enter level of priority from 1-3 : ")

    if not priority.isdigit():
      print("Priority level has to be a digit between 1 and 3.")
      continue

    elif priority not in level:
      print("Priority level has to be a digit between 1 and 3.")
      continue

    else:
      break

  desc = input("Enter description of task: ")

  date = input("Enter due date of task (DD-MM-YY): ")

  while True:
    status = input("Enter status of task (Completed/Incomplete): ").lower()
    if status != "completed" or status != "incomplete":
      print("Incorrect input for status.")
      continue
    else:
      break

  tasks[name] = [f"Priority: {priority}", f"Due date: {date}", f"Description: {desc}", f"Status : {status}"]
  return f" Task: {view_name}. \n Status: {tasks[view_name[3]]}. \n Priority: {tasks[view_name][0]}. \n Due data: {tasks[view_name][1]}. \n Description: {tasks[view_name][2]}"
