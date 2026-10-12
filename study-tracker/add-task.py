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
