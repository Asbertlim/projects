def save_task():
  with open("tasks.json", "w") as f:
    json.dump(tasks, f, indent=4)
    
  print("Tasks successfully saved!")
