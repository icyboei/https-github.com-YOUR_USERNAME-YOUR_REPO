#!/usr/bin/env python3
"""
Simple CLI Task Manager (todo.py)
A lightweight command-line tool to manage your daily tasks.
"""

import argparse
import json
import os
import sys
from datetime import datetime

DEFAULT_FILE = "tasks.json"

PRIORITIES = ["Low", "Medium", "High"]


def load_tasks(filepath=DEFAULT_FILE):
    """Load tasks from a JSON file."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Warning: Could not read {filepath} ({e}). Starting with empty list.")
        return []


def save_tasks(tasks, filepath=DEFAULT_FILE):
    """Save tasks to a JSON file."""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
    except IOError as e:
        print(f"Error saving tasks to {filepath}: {e}", file=sys.stderr)


def add_task(tasks, title, category="General", priority="Medium", filepath=DEFAULT_FILE):
    """Add a new task to the task list."""
    if not title.strip():
        print("Error: Task title cannot be empty.", file=sys.stderr)
        return False
    
    priority = priority.capitalize()
    if priority not in PRIORITIES:
        priority = "Medium"

    task = {
        "id": max([t["id"] for t in tasks], default=0) + 1,
        "title": title.strip(),
        "category": category.strip(),
        "priority": priority,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(task)
    save_tasks(tasks, filepath)
    print(f"[+] Added task #{task['id']}: '{task['title']}' [{task['priority']}] ({task['category']})")
    return True


def list_tasks(tasks, status_filter="all", category_filter=None):
    """Display tasks with filtering options."""
    if not tasks:
        print("No tasks found.")
        return

    filtered = tasks
    if status_filter == "pending":
        filtered = [t for t in filtered if not t["completed"]]
    elif status_filter == "completed":
        filtered = [t for t in filtered if t["completed"]]

    if category_filter:
        filtered = [t for t in filtered if t["category"].lower() == category_filter.lower()]

    if not filtered:
        print(f"No tasks matching criteria (status: {status_filter}, category: {category_filter or 'any'}).")
        return

    print("\n" + "=" * 65)
    print(f"{'ID':<4} {'Status':<10} {'Priority':<10} {'Category':<12} {'Title'}")
    print("=" * 65)

    for t in filtered:
        status_str = "[X] Done" if t["completed"] else "[ ] Pending"
        print(f"{t['id']:<4} {status_str:<10} {t['priority']:<10} {t['category']:<12} {t['title']}")
    
    print("=" * 65)

    total = len(tasks)
    done_count = sum(1 for t in tasks if t["completed"])
    print(f"Total: {total} | Completed: {done_count} | Pending: {total - done_count}\n")


def complete_task(tasks, task_id, filepath=DEFAULT_FILE):
    """Mark a task as completed."""
    for t in tasks:
        if t["id"] == task_id:
            if t["completed"]:
                print(f"Task #{task_id} is already completed.")
                return False
            t["completed"] = True
            save_tasks(tasks, filepath)
            print(f"[+] Task #{task_id} ('{t['title']}') marked as completed!")
            return True
    print(f"Error: Task #{task_id} not found.", file=sys.stderr)
    return False


def delete_task(tasks, task_id, filepath=DEFAULT_FILE):
    """Delete a task by ID."""
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            removed = tasks.pop(i)
            save_tasks(tasks, filepath)
            print(f"[+] Task #{task_id} ('{removed['title']}') deleted.")
            return True
    print(f"Error: Task #{task_id} not found.", file=sys.stderr)
    return False


def search_tasks(tasks, keyword):
    """Search tasks by title or category keyword."""
    keyword_lower = keyword.lower()
    matches = [t for t in tasks if keyword_lower in t["title"].lower() or keyword_lower in t["category"].lower()]
    print(f"\n--- Search results for '{keyword}' ---")
    list_tasks(matches)


def build_parser():
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(description="Simple CLI Task Manager")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", type=str, help="Task description")
    add_parser.add_argument("-c", "--category", type=str, default="General", help="Category name")
    add_parser.add_argument("-p", "--priority", choices=["Low", "Medium", "High"], default="Medium", help="Priority level")

    # List command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("-s", "--status", choices=["all", "pending", "completed"], default="all", help="Filter by status")
    list_parser.add_argument("-c", "--category", type=str, default=None, help="Filter by category")

    # Complete command
    done_parser = subparsers.add_parser("done", help="Mark task as complete")
    done_parser.add_argument("id", type=int, help="Task ID")

    # Delete command
    del_parser = subparsers.add_parser("delete", help="Delete a task")
    del_parser.add_argument("id", type=int, help="Task ID")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search tasks")
    search_parser.add_argument("keyword", type=str, help="Keyword to search")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    tasks = load_tasks()

    if args.command == "add":
        add_task(tasks, args.title, category=args.category, priority=args.priority)
    elif args.command == "list":
        list_tasks(tasks, status_filter=args.status, category_filter=args.category)
    elif args.command == "done":
        complete_task(tasks, args.id)
    elif args.command == "delete":
        delete_task(tasks, args.id)
    elif args.command == "search":
        search_tasks(tasks, args.keyword)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
