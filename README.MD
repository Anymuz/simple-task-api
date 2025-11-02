# Task Management API (GraphQL) 

*A simple task list API built with **FastAPI**, **Strawberry GraphQL**, **SQLAlchemy**, and **SQLite**.*

## Overview
This GraphQL API provides CRUD functionality for managing a list of tasks. Users can:

* Add, toggle status and delete tasks.
* Query sngle tasks by ID or filter them by title.

Bonus features include:
* A mutation to update task title
* A query to retrieve task completion statistics
* Added optional search argumment to query only completed/inncomplete tasks

The system uses:
* **FastAPI** as the web server
* **Strawberry GraphQL** for schema definition
* **SQLAlchemy** as ORM (backed by **SQLite**)

## Tech Stack
* **Python 3.11**
* **FastAPI** - web framework to mount and serve GraphQL endpoint
* **Strawberry GraphQL** - defines the schema and handles query/mutation resolution
* **SQLAlchemy** - ORM layer for SQLite
* **SQLite** - persistent storage backend (via file-based DB)

## Setup Instructions
Clone this repo or download and unzip into directory on system and ensure installation of Python 3.10+ beforehand.

### Environment & Installation
This project requires the following libraries:
- `fastapi`
- `strawberry-graphql[fastapi]`
- `sqlalchemy`
- `aiosqlite`
- `uvicorn`
They are listed in requirements.txt so that using python virtual environment (venv) and pip allows for quick and easy environment set up. Depending on system of choice use the following commands in the terminal.

#### Unix/macOS (bash/zsh)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Windows CMD
```cmd
python -m venv .venv
.venv\Scripts\Activate
pip install -r requirements.txt
```

#### Windows PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

  If you encounter a PowerShell execution policy error, run:
  >
  > ```powershell
  > Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  > ```

### Run the App
Start the server, `taskData.db` will be created with first mutation.
```bash
uvicorn app.main:app --reload
```

GraphQL endpoint available at: [http://localhost:8000/task-api](http://localhost:8000/task-api)

## Project Structure
This project will have thefollowing file structure:
```
app/
├── __init__.py
├── main.py         # FastAPI server + schema mount
├── database.py     # SQLAlchemy DB engine + session
├── models.py       # SQLAlchemy Task model
├── schema.py       # GraphQL schema + resolvers
.gitignore            
requirements.txt
README.md
```

**NOTE:** `taskData.db` included in .gitignore is created automatically.

## GraphQL API Structure
The following queries are implemented.

### Queries
| Name | Input Arguments  | Returns | Description |
| --- | --- | --- | --- |
| `tasks` | `TaskListInput(search?: str, completed?: bool) or None` | `List[TaskType]` | Returns all tasks optionally filtered by title, returns empty list if none |
| `task` | `TaskIDInput(ID: int!)` | `TaskType or Null` | Returns a single task base on given ID or null if no task has that ID |
| `taskStats` | --- | `TaskStatsType` | Type contains count of total, complete and incomplete tasks |

### Mutationss
| Name | Input Arguents | Returns | Description  |
| --- | --- | --- | --- |
| `addTask` | `NewTaskInput(title: str!)` | `TaskType` | Creates a new task with given title |
| `toggleTask` | `TaskIDInput(ID: int!)` | `TaskType or Null` | Swaps value completed and returns task or null |
| `deleteTask` | `TaskIDInput(ID: int!)` | `TaskType or Null` | Removes task with given ID and returns task  or null |
| `updateTask` | `UpdateTaskInput(id: int!, title: str!)` | `TaskType or null` | Updates a task's title and returns task or null |

## Usage guide for Queries & Mutations (TODO: Produce usage examples guide)
The API has aformentioned query and mutation operations to use, for a full set of detailed examples and optional input combinations, refer to the [Task API Usage Guide](./USAGE.md).

## Design Aspects
* All queries and mutations will use a pre-define input type.
* DateTime fields use `Optional` in the GraphQL task type to ensure that nullable fields or optional filters  don't raise errors. This is because the feilds fror `created_at` and `updated_at` are set on update to the database not during API request.
* All the search filters for `tasks` are optonal, the query can be called without any input provided. 
* For `tasks` query the use of `List[TaskType]` will always return an array even if empty, to match GraphQL design best practices.
* `taskStats` query and `updateTask` are introduced as two **bonus operations**.
* An optional search parameter `completed` filters completed tasks from non completed tasks, added as a parameter of 'tasks' query as to meet within spec allowance of 2 additional operations.

## Handling Complex Error Scenarios
The base GraphQL schema has simple operations that assume minimal failure paths or error cases. Below are some proposals for improving the robustness of this simple API:

TODO:(discuss here)

## License

MIT (You may fork and build on this template)

## Author Notes

This README and the associated implementation were created for submission to a take-home technical assessment. While designed to meet a precise spec, the project may be expanded into a task manager boilerplate or learning scaffold in future forks.

For purpose of defending this as being an independent work, all implementation decisions are shown to be understood and deliberate by using comments, this `README`, and commit history to provide further insight.