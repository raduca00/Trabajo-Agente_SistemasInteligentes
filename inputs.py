import json
from datetime import datetime, timedelta
import ollama

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

            task = self.create_task_dict(name, days_to_deadline, estimated_hours)
            new_tasks.append(task)
            print(f"✅ Task '{name}' captured!")
            
        return new_tasks

    def get_tasks_from_llm(self, model_name="qwen2.5:3b"):
        """Level 3: Extract tasks using local Ollama with an explicit 7-day calendar reference."""
        new_tasks = []
        print(f"\n🧠 --- Mode: Natural Language Input (Powered by {model_name}) ---")
        print("💡 Describe your tasks naturally (Type 'exit' to stop).")
        print("   Example: 'Tengo examen de Redes en 4 días y necesito estudiar 6 horas'")

        while True:
            user_text = input("\n🗣️ Tell me what you have to do: ").strip()
            if user_text.lower() == 'exit':
                print("🚪 Exiting natural language mode.")
                break
            if not user_text:
                continue

            now = datetime.now()
            # Build a mini 7-day calendar so the small LLM doesn't have to do date math
            calendar_ref = "\n".join([
                f"- In {i} day(s) ({(now + timedelta(days=i)).strftime('%A')}): {(now + timedelta(days=i)).strftime('%Y-%m-%d')}"
                for i in range(8)
            ])

            system_prompt = f"""
            You are a strict academic task extractor.
            Reference calendar starting today:
            {calendar_ref}

            Rules:
            1. Extract each task, exam, or assignment mentioned by the user.
            2. If the user says "en X días" or "in X days", 'days_to_deadline' MUST be that exact number X.
            3. If the user mentions a weekday (e.g., "el lunes", "Friday"), look up the matching day in the reference calendar above.
            4. 'estimated_hours' is the study time needed (default to 2.0 if not mentioned).

            Respond ONLY with valid JSON using this exact structure:
            {{
                "tasks": [
                    {{
                        "name": "string",
                        "days_to_deadline": int,
                        "estimated_hours": float
                    }}
                ]
            }}
            """

            print("⏳ Thinking... Parsing natural language with local LLM...")
            try:
                response = ollama.chat(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_text}
                    ],
                    format="json",
                    options={"temperature": 0.0}  # 0.0 forces deterministic, strict extraction
                )

                raw_content = response["message"]["content"]
                parsed_data = json.loads(raw_content)
                extracted_tasks = parsed_data.get("tasks", [])

                if not extracted_tasks:
                    print("⚠️ The agent couldn't detect any clear tasks in that sentence. Try being more specific.")
                    continue

                for item in extracted_tasks:
                    name = str(item.get("name", "Unnamed Task")).strip()
                    days_to_deadline = max(0, int(item.get("days_to_deadline", 1)))
                    estimated_hours = max(0.5, float(item.get("estimated_hours", 2.0)))

                    task = self.create_task_dict(name, days_to_deadline, estimated_hours)
                    new_tasks.append(task)
                    print(f"  ➕ Extracted: '{name}' | Due in: {days_to_deadline}d | Workload: {estimated_hours}h")

            except json.JSONDecodeError:
                print("⚠️ Error: The LLM returned an invalid JSON format. Please try phrasing it again.")
            except Exception as e:
                print(f"❌ Connection error with Ollama: {e}")
                print("💡 Make sure Ollama is running in the background.")

        return new_tasks


    # --- HOOKS PARA FUTURAS MEJORAS ---
    def get_tasks_from_url(self, url):
        """Future Extension: Scrape official university schedule from URL."""
        raise NotImplementedError("URL Scraper module pending.")
