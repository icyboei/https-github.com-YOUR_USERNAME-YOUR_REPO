# CLI Task Manager (todo.py)

A simple, fast, and feature-rich Python CLI application to manage daily tasks.

## Features
- **Add Tasks**: Set priority (Low, Medium, High) and custom categories.
- **List Tasks**: Filter by status (`all`, `pending`, `completed`) or category.
- **Mark Complete**: Easily mark tasks as finished.
- **Delete Tasks**: Remove tasks by ID.
- **Search**: Search tasks by title or category keyword.
- **Persistent Storage**: Saves tasks locally to `tasks.json`.

## Usage

```bash
# Add a task
python todo.py add "Finish project documentation" -p High -c Work

# List pending tasks
python todo.py list -s pending

# Mark task #1 as complete
python todo.py done 1

# Delete task #1
python todo.py delete 1

# Search tasks
python todo.py search "documentation"
```

## Running Tests

```bash
python -m unittest test_todo.py
```
