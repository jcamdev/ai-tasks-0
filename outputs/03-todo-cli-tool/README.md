# Todo CLI Tool

A simple command-line todo application written in Python.

## Features

- Add new tasks
- List all tasks
- Mark tasks as completed
- Delete tasks
- Persistent storage using JSON
- Clean command-line interface

## Usage

```bash
# Add a new task
python todo.py add "Buy groceries"

# List all tasks
python todo.py list

# Complete a task (by ID)
python todo.py complete 1

# Delete a task (by ID)
python todo.py delete 2

# Show help
python todo.py help
```

## Requirements

- Python 3.6+
- No external dependencies required

## Data Storage

Tasks are stored in a `todos.json` file in the same directory as the script.