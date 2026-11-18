from agent import SmartStudyAgent

def start_interface():
    agent = SmartStudyAgent()
    
    while True:
        print("\n========================================")
        print("SMARTSTUDY AGENT MAIN MENU")
        print("========================================")
        print("1. 🗣️ Input tasks with Natural Language (AI)")
        print("2. 📥 Input tasks manually (with Schema Guide)")
        print("3. 📋 View current tasks in memory")
        print("4. 📅 Generate study schedule")
        print("5. 🗑️ Clear task memory (RAM + JSON)")
        print("6. ❌ Exit program")
        print("========================================")
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice == "1":
            agent.add_llm_tasks()
        elif choice == "2":
            agent.add_manual_tasks()
        elif choice == "3":
            agent.view_tasks()
            input("\n Press Enter to return to the menu...")
        elif choice == "4":
            agent.create_schedule()
            input("\n Press Enter to return to the menu...")
        elif choice == "5":
            agent.wipe_memory()
            input("\n Press Enter to return to the menu...")
        elif choice == "6":
            print("\n Goodbye! Persistent memory is safely stored on disk. Shutting down.")
            break
        else:
            print("\n Invalid option. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    start_interface()
