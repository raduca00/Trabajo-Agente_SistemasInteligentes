import json
import os
from datetime import datetime

class MemoryManager:
    def __init__(self, memory_file="tasks_memory.json"):
        self.memory_file = memory_file

    def load_tasks(self):
        """Loads tasks from the local JSON file and recalculates remaining days dynamically."""
        if not os.path.exists(self.memory_file):
            return []

        try:
            with open(self.memory_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                now = datetime.now()
                
                for task in data:
                    if isinstance(task.get("deadline_date"), str):
                        deadline = datetime.fromisoformat(task["deadline_date"])
                        task["deadline_date"] = deadline
                        
                        remaining_days = (deadline - now).days
                        task["days_to_deadline"] = max(0, remaining_days)
                        
                self.save_tasks(data)
                return data
                
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Warning: Could not read memory file ({e}). Starting with empty memory.")
            return []

    def save_tasks(self, tasks):
        """Saves current RAM tasks into the local JSON file."""
        serializable_tasks = []
        for task in tasks:
            task_copy = task.copy()
            if isinstance(task_copy.get("deadline_date"), datetime):
                task_copy["deadline_date"] = task_copy["deadline_date"].isoformat()
            serializable_tasks.append(task_copy)

        try:
            with open(self.memory_file, "w", encoding="utf-8") as file:
                json.dump(serializable_tasks, file, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"❌ Error saving to persistent memory: {e}")

    def clear_memory(self):
        self.save_tasks([])
