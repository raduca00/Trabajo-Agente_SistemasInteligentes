from agent import SmartStudyAgent

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
            agent.add_manual_tasks()
        elif choice == "2":
            agent.view_tasks()
            input("\n Press Enter to return to the menu...")
        elif choice == "3":
            agent.create_schedule()
            input("\n Press Enter to return to the menu...")
        elif choice == "4":
            agent.wipe_memory()
            input("\n Press Enter to return to the menu...")
        elif choice == "5":
            print("\n Goodbye! Persistent memory is safely stored on disk. Shutting down.")
            break
        else:
            print("\n Invalid option. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    start_interface()
