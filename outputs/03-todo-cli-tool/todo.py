#!/usr/bin/env python3
import json
import os
import sys
from datetime import datetime
from typing import List, Dict

class TodoManager:
    def __init__(self, filename: str = "todos.json"):
        self.filename = filename
        self.todos = self.load_todos()

    def load_todos(self) -> List[Dict]:
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_todos(self):
        with open(self.filename, 'w') as f:
            json.dump(self.todos, f, indent=2)

    def add_task(self, description: str):
        task = {
            "id": len(self.todos) + 1,
            "description": description,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        self.todos.append(task)
        self.save_todos()
        print(f"✅ Added task: {description}")

    def list_tasks(self):
        if not self.todos:
            print("📝 No tasks found!")
            return

        print("\n📋 Your Tasks:")
        print("-" * 50)
        for task in self.todos:
            status = "✅" if task["completed"] else "⏳"
            print(f"{status} [{task['id']}] {task['description']}")
        print()

    def complete_task(self, task_id: int):
        for task in self.todos:
            if task["id"] == task_id:
                task["completed"] = True
                task["completed_at"] = datetime.now().isoformat()
                self.save_todos()
                print(f"🎉 Completed task: {task['description']}")
                return
        print(f"❌ Task with ID {task_id} not found!")

    def delete_task(self, task_id: int):
        for i, task in enumerate(self.todos):
            if task["id"] == task_id:
                deleted_task = self.todos.pop(i)
                self.save_todos()
                print(f"🗑️ Deleted task: {deleted_task['description']}")
                return
        print(f"❌ Task with ID {task_id} not found!")

def show_help():
    print("""
📝 Todo CLI Tool

Usage:
    python todo.py add "Task description"    - Add a new task
    python todo.py list                      - List all tasks
    python todo.py complete <id>             - Mark task as completed
    python todo.py delete <id>               - Delete a task
    python todo.py help                      - Show this help message

Examples:
    python todo.py add "Buy groceries"
    python todo.py complete 1
    python todo.py delete 2
    """)

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    todo_manager = TodoManager()
    command = sys.argv[1].lower()

    if command == "add":
        if len(sys.argv) < 3:
            print("❌ Please provide a task description!")
            return
        description = " ".join(sys.argv[2:])
        todo_manager.add_task(description)

    elif command == "list":
        todo_manager.list_tasks()

    elif command == "complete":
        if len(sys.argv) < 3:
            print("❌ Please provide a task ID!")
            return
        try:
            task_id = int(sys.argv[2])
            todo_manager.complete_task(task_id)
        except ValueError:
            print("❌ Task ID must be a number!")

    elif command == "delete":
        if len(sys.argv) < 3:
            print("❌ Please provide a task ID!")
            return
        try:
            task_id = int(sys.argv[2])
            todo_manager.delete_task(task_id)
        except ValueError:
            print("❌ Task ID must be a number!")

    elif command == "help":
        show_help()

    else:
        print(f"❌ Unknown command: {command}")
        show_help()

if __name__ == "__main__":
    main()