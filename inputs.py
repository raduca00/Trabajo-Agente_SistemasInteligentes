from datetime import datetime, timedelta

class TaskInputProvider:
    @staticmethod
    def create_task_dict(name, days_to_deadline, estimated_hours):
        """Standardizes any task regardless of its origin (Manual, LLM, or Web URL)."""
        deadline_date = datetime.now() + timedelta(days=days_to_deadline)
        return {
            "name": name,
            "days_to_deadline": days_to_deadline,
            "deadline_date": deadline_date,
            "estimated_hours": estimated_hours,
            "priority": 0.0
        }

    def get_manual_tasks(self):
        new_tasks = []
        print("\n📥 --- Mode: Input Tasks (Type 'exit' in the task name to stop) ---")
        
        while True:
            print("💡 Expected Schema: <string>TaskName  |  Example: 'SIS2 Assignment' or 'Networking Exam'")
            name = input("📝 Enter Task Name: ").strip()
            if name.lower() == 'exit':
                print("🚪 Exiting task insertion mode.")
                break
            if not name:
                print("⚠️ Task name cannot be empty. Please match the requested schema.")
                continue

            while True:
                print(f"💡 Expected Schema: <int>DaysLeft     |  Example: 5 (if due in 5 days)")
                days_input = input(f"📅 Days left until '{name}' is due: ").strip()
                if days_input.lower() == 'exit': return new_tasks
                try:
                    days_to_deadline = int(days_input)
                    if days_to_deadline < 0:
                        print("⚠️ Days remaining cannot be negative.")
                        continue
                    break
                except ValueError:
                    print("⚠️ Input parsing error. Please enter a valid integer matching the schema.")

            while True:
                print(f"Expected Schema: <float>Hours     |  Example: 4 or 6.5 (hours of total study required)")
                hours_input = input(f"Estimated hours required for '{name}': ").strip()
                if hours_input.lower() == 'exit': return new_tasks
                try:
                    estimated_hours = float(hours_input)
                    if estimated_hours <= 0:
                        print("⚠️ Estimated workload must be greater than zero.")
                        continue
                    break
                except ValueError:
                    print("⚠️ Input parsing error. Please enter a valid number matching the schema.")

            task = self.create_task_dict(name, days_to_deadline, hours_input and estimated_hours)
            new_tasks.append(task)
            print(f"Task '{name}' captured!")
            
        return new_tasks

    # --- HOOKS PARA FUTURAS MEJORAS ---
    def get_tasks_from_llm(self):
        """Future Level 3: Extract tasks using local Ollama."""
        raise NotImplementedError("Ollama module pending.")

    def get_tasks_from_url(self, url):
        """Future Extension: Scrape official university schedule from URL."""
        raise NotImplementedError("URL Scraper module pending.")
