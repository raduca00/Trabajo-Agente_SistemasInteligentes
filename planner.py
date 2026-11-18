from datetime import datetime, timedelta

class StudyPlanner:
    def calculate_priorities(self, tasks):
        if not tasks:
            return tasks
        print("\nThinking... Evaluating task priorities...")
        for task in tasks:
            days = max(task["days_to_deadline"], 0.5) 
            task["priority"] = task["estimated_hours"] / days
        
        tasks.sort(key=lambda x: x["priority"], reverse=True)
        return tasks

    def generate_schedule(self, tasks, available_hours_per_day):
        prioritized_tasks = self.calculate_priorities(tasks)
        current_date = datetime.now()
        pending_tasks = [t.copy() for t in prioritized_tasks]
        schedule_plan = []

        for i in range(5):
            schedule_date = current_date + timedelta(days=i)
            day_name = schedule_date.strftime('%A')
            
            remaining_hours_today = available_hours_per_day
            today_time_slots = []
            
            for task in pending_tasks:
                if remaining_hours_today <= 0:
                    break
                if task["estimated_hours"] > 0:
                    allocated_hours = min(task["estimated_hours"], remaining_hours_today)
                    task["estimated_hours"] -= allocated_hours
                    remaining_hours_today -= allocated_hours
                    today_time_slots.append(f"{task['name']} ({allocated_hours}h)")
            
            schedule_plan.append((day_name, today_time_slots))
            
        return schedule_plan
