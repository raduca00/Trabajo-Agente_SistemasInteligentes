from memory import MemoryManager
from planner import StudyPlanner
from inputs import TaskInputProvider

class SmartStudyAgent:
    def __init__(self, memory_file="tasks_memory.json"):
        self.memory = MemoryManager(memory_file)
        self.planner = StudyPlanner()
        self.input_provider = TaskInputProvider()
        self.tasks = self.memory.load_tasks()
        print(f"🤖 SmartStudy Agent: Environment initialized. Loaded {len(self.tasks)} task(s) from persistent memory. 🤖")

    def add_manual_tasks(self):
        new_tasks = self.input_provider.get_manual_tasks()
        if new_tasks:
            self.tasks.extend(new_tasks)
            self.memory.save_tasks(self.tasks)
            print(f"State updated & saved to disk! Total tasks in memory: {len(self.tasks)}")

    def view_tasks(self):
        if not self.tasks:
            print("\nTask memory is currently empty.")
            return
        print("\n--- Current Tasks in Persistent Memory ---")
        for i, t in enumerate(self.tasks, 1):
            print(f"  {i}. {t['name']} | Due in: {t['days_to_deadline']} days | Required workload: {t['estimated_hours']}h")

    def create_schedule(self):
        if not self.tasks:
            print("\nNo tasks found in the agent's memory. Please add some tasks first!")
            return

        while True:
            print("Expected Schema: <float>DailyHours |  Example: 2 or 3.5 (hours per day)")
            hours_input = input("📅 How many hours do you have available per day to study?: ").strip()
            try:
                available_hours_per_day = float(hours_input)
                if available_hours_per_day <= 0:
                    print("⚠️ Available hours must be greater than zero.")
                    continue
                break
            except ValueError:
                print("⚠️ Input parsing error. Please enter a valid number.")

        print(f"\n📅 --- STUDY SCHEDULE GENERATED ({available_hours_per_day}h/day) ---")
        schedule_plan = self.planner.generate_schedule(self.tasks, available_hours_per_day)
        self.memory.save_tasks(self.tasks)
        
        for day_name, today_time_slots in schedule_plan:
            if today_time_slots:
                print(f"  • {day_name}: {', '.join(today_time_slots)}")
            else:
                print(f"  • {day_name}: ☕ Free day or no pending tasks left!")

    def wipe_memory(self):
        self.tasks = []
        self.memory.clear_memory()
        print("\nMemory wiped successfully (RAM and JSON disk file cleared).")
