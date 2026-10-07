from datetime import datetime, timedelta

class SmartStudyAgent:
    def __init__(self):
        # Component 4: Volatile working memory (list in RAM execution)
        self.tasks = []
        print("🤖 SmartStudy Agent: Volatile environment successfully initialized.")

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
                print(f"💡 Expected Schema: <float>Hours     |  Example: 4 or 6.5 (hours of total study required)")
                hours_input = input(f"⏳ Estimated hours required for '{name}': ").strip()
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
            
            # Appends tasks sequentially to maintain previous data state in memory (RAM)
            self.tasks.append(task)
            print(f"✅ State updated! Total tasks registered in volatile memory: {len(self.tasks)}")

    # Component 2: Prioritizer (Rule-Based Reasoning Engine)
    def calculate_priorities(self):
        if not self.tasks:
            return
        print("\n🧠 Thinking... Evaluating task priorities...")
        for task in self.tasks:
            # Agentic rule: Less time remaining combined with higher workload increases urgency.
            # Avoid division by zero if the deadline is today (0 days remaining)
            days = max(task["days_to_deadline"], 0.5) 
            task["priority"] = task["estimated_hours"] / days
        
        # Sort tasks dynamically from highest to lowest urgency
        self.tasks.sort(key=lambda x: x["priority"], reverse=True)

    # Component 3: Scheduler (Decision-Making System)
    def generate_schedule(self):
        if not self.tasks:
            print("\n ⚠️ No tasks found in the agent's memory. Please add some tasks first!")
            return

        while True:
            print("💡 Expected Schema: <float>DailyHours |  Example: 2 or 3.5 (hours per day)")
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
            print("\n📭 Task memory is currently empty.")
            return
        print("\n📋 --- Current Tasks in Volatile Memory ---")
        for i, t in enumerate(self.tasks, 1):
            print(f"  {i}. {t['name']} | Due in: {t['days_to_deadline']} days | Required workload: {t['estimated_hours']}h")

    def clear_tasks(self):
        self.tasks = []
        print("\n 🗑️ Volatile memory cleared successfully. All tasks have been wiped from execution.")

# --- MAIN INTERACTIVE INTERFACE LOOP (CLI) ---
def start_interface():
    agent = SmartStudyAgent()
    
    while True:
        print("\n========================================")
        print("🤖 SMARTSTUDY AGENT MAIN MENU")
        print("========================================")
        print("1. 📥 Input tasks manually (with Schema Guide)")
        print("2. 📋 View current tasks in memory")
        print("3. 📅 Generate study schedule")
        print("4. 🗑️ Clear task memory")
        print("5. ❌ Exit program")
        print("========================================")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == "1":
            agent.menu_input_tasks()
        elif choice == "2":
            agent.list_tasks()
        elif choice == "3":
            agent.generate_schedule()
        elif choice == "4":
            agent.clear_tasks()
        elif choice == "5":
            print("\n👋 Goodbye! Freeing agent workspace... Shutting down.")
            break
        else:
            print("\n ⚠️ Invalid option. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    start_interface()
