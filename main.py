import json
import os
from datetime import datetime, timedelta

class SmartStudyAgent:
    def __init__(self, memory_file="tasks_memory.json"):
        # Component 4: Persistent working memory (RAM + JSON file on disk)
        self.memory_file = memory_file
        self.tasks = []
        self.load_tasks()
        print(f"🤖 SmartStudy Agent: Environment initialized. Loaded {len(self.tasks)} task(s) from persistent memory. 🤖")

    # --- PERSISTENT MEMORY METHODS (LEVEL 2) ---
    def load_tasks(self):
        """Loads tasks from the local JSON file and recalculates remaining days dynamically."""
        if not os.path.exists(self.memory_file):
            self.tasks = []
            return

        try:
            with open(self.memory_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                now = datetime.now()
                
                for task in data:
                    if isinstance(task.get("deadline_date"), str):
                        deadline = datetime.fromisoformat(task["deadline_date"])
                        task["deadline_date"] = deadline
                        
                        # Recalculate days left comparing deadline against current clock
                        remaining_days = (deadline - now).days
                        # Prevent negative days if the deadline already passed (sets to 0 = due today/overdue)
                        task["days_to_deadline"] = max(0, remaining_days)
                        
                self.tasks = data
                # Save the updated days back to the JSON file
                self.save_tasks()
                
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Warning: Could not read memory file ({e}). Starting with empty memory.")
            self.tasks = []


    def save_tasks(self):
        """Saves current RAM tasks into the local JSON file."""
        serializable_tasks = []
        for task in self.tasks:
            task_copy = task.copy()
            # Convert Python datetime objects to ISO strings so JSON can store them
            if isinstance(task_copy.get("deadline_date"), datetime):
                task_copy["deadline_date"] = task_copy["deadline_date"].isoformat()
            serializable_tasks.append(task_copy)

        try:
            with open(self.memory_file, "w", encoding="utf-8") as file:
                json.dump(serializable_tasks, file, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"❌ Error saving to persistent memory: {e}")

    # Component 1: Task Analyzer & Manual Input Interface (With Expected Schemas)
    def menu_input_tasks(self):
        print("\n📥 --- Mode: Input Tasks (Type 'exit' in the task name to stop) ---")
        
        while True:
            # 1. Schema Guidance for Task Name
            print("💡 Expected Schema: <string>TaskName  |  Example: 'SIS2 Assignment' or 'Networking Exam'")
            name = input("📝 Enter Task Name: ").strip()
            if name.lower() == 'exit':
                print("🚪 Exiting task insertion mode.")
                break
                
            if not name:
                print("⚠️ Task name cannot be empty. Please match the requested schema.")
                continue

            # 2. Schema Guidance for Days Remaining
            while True:
                print(f"💡 Expected Schema: <int>DaysLeft     |  Example: 5 (if due in 5 days)")
                days_input = input(f"📅 Days left until '{name}' is due: ").strip()
                if days_input.lower() == 'exit': return
                try:
                    days_to_deadline = int(days_input)
                    if days_to_deadline < 0:
                        print("⚠️ Days remaining cannot be negative.")
                        continue
                    break
                except ValueError:
                    print("⚠️ Input parsing error. Please enter a valid integer matching the schema.")

            # 3. Schema Guidance for Estimated Workload Hours
            while True:
                print(f"Expected Schema: <float>Hours     |  Example: 4 or 6.5 (hours of total study required)")
                hours_input = input(f"Estimated hours required for '{name}': ").strip()
                if hours_input.lower() == 'exit': return
                try:
                    estimated_hours = float(hours_input)
                    if estimated_hours <= 0:
                        print("⚠️ Estimated workload must be greater than zero.")
                        continue
                    break
                except ValueError:
                    print("⚠️ Input parsing error. Please enter a valid number matching the schema.")

            # Constructing the structural task data object
            deadline_date = datetime.now() + timedelta(days=days_to_deadline)
            task = {
                "name": name,
                "days_to_deadline": days_to_deadline,
                "deadline_date": deadline_date,
                "estimated_hours": estimated_hours,
                "priority": 0.0
            }
            
            # Appends tasks sequentially and syncs with JSON persistent memory
            self.tasks.append(task)
            self.save_tasks()
            print(f"State updated & saved to disk! Total tasks in memory: {len(self.tasks)}")

    # Component 2: Prioritizer (Rule-Based Reasoning Engine)
    def calculate_priorities(self):
        if not self.tasks:
            return
        print("\nThinking... Evaluating task priorities...")
        for task in self.tasks:
            # Agentic rule: Less time remaining combined with higher workload increases urgency.
            # Avoid division by zero if the deadline is today (0 days remaining)
            days = max(task["days_to_deadline"], 0.5) 
            task["priority"] = task["estimated_hours"] / days
        
        # Sort tasks dynamically from highest to lowest urgency
        self.tasks.sort(key=lambda x: x["priority"], reverse=True)
        # Update JSON order so priorities stay persisted
        self.save_tasks()

    # Component 3: Scheduler (Decision-Making System)
    def generate_schedule(self):
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
        self.calculate_priorities()
        
        current_date = datetime.now()
        pending_tasks = [t.copy() for t in self.tasks]
        
        # Generates a workload distribution plan for the next 5 days
        for i in range(5):
            schedule_date = current_date + timedelta(days=i)
            day_name = schedule_date.strftime('%A')
            
            remaining_hours_today = available_hours_per_day
            today_time_slots = []
            
            for task in pending_tasks:
                if remaining_hours_today <= 0:
                    break
                
                if task["estimated_hours"] > 0:
                    # The agent dynamically decides how much time to allocate for this specific task today
                    allocated_hours = min(task["estimated_hours"], remaining_hours_today)
                    task["estimated_hours"] -= allocated_hours
                    remaining_hours_today -= allocated_hours
                    today_time_slots.append(f"{task['name']} ({allocated_hours}h)")
            
            if today_time_slots:
                print(f"  • {day_name}: {', '.join(today_time_slots)}")
            else:
                print(f"  • {day_name}: ☕ Free day or no pending tasks left!")

    # Memory Management Helper Functions
    def list_tasks(self):
        if not self.tasks:
            print("\nTask memory is currently empty.")
            return
        print("\n--- Current Tasks in Persistent Memory ---")
        for i, t in enumerate(self.tasks, 1):
            print(f"  {i}. {t['name']} | Due in: {t['days_to_deadline']} days | Required workload: {t['estimated_hours']}h")

    def clear_tasks(self):
        """Wipes both RAM execution memory and the persistent JSON file."""
        self.tasks = []
        self.save_tasks()
        print("\nMemory wiped successfully (RAM and JSON disk file cleared).")

# --- MAIN INTERACTIVE INTERFACE LOOP (CLI) ---
def start_interface():
    agent = SmartStudyAgent()
    
    while True:
        print("\n========================================")
        print("SMARTSTUDY AGENT MAIN MENU")
        print("========================================")
        print("1. 📥 Input tasks manually (with Schema Guide)")
        print("2. 📋 View current tasks in memory")
        print("3. 📅 Generate study schedule")
        print("4. 🗑️ Clear task memory (RAM + JSON)")
        print("5. ❌ Exit program")
        print("========================================")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == "1":
            agent.menu_input_tasks()
        elif choice == "2":
            agent.list_tasks()
            input("\n Press Enter to return to the menu...")
        elif choice == "3":
            agent.generate_schedule()
            input("\n Press Enter to return to the menu...")
        elif choice == "4":
            agent.clear_tasks()
            input("\n Press Enter to return to the menu...")
        elif choice == "5":
            print("\n Goodbye! Persistent memory is safely stored on disk. Shutting down.")
            break
        else:
            print("\n Invalid option. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    start_interface()
