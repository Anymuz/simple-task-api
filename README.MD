# Task Management API (GraphQL) 

*A simple task list API built with **FastAPI**, **Strawberry GraphQL**, **SQLAlchemy**, and **SQLite**.*

## Overview
This GraphQL API provides CRUD functionality for managing a list of tasks. Users can:

* Add, toggle status and delete tasks.
* Query single tasks by ID or filter them by title.

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
Start the server, `taskData.db` will be created with first launch. Launching with `--reload` allows changes to  take immediate effect, recommended for dev/staging but no so much in a production scenario.

```bash
uvicorn app.main:app --reload
```

GraphQL endpoint available at: [http://localhost:8000/task-api](http://localhost:8000/task-api) will provide a playground so requests dont need to be scripted or made by external tools.

## Project Structure
This is the inital directory structure with each files purpose described.
```
.
├── app/
│   ├── __init__.py   -> Treat directory as package
│   ├── main.py       -> FastAPI server + schema mount
│   ├── database.py   -> SQLAlchemy DB engine + session
│   ├── models.py     -> SQLAlchemy Task model
│   └── schema.py     -> GraphQL schema + resolvers
├── docs/
│   ├── Complex_Error_Handling.md   -> Deeper analysis of error handling beyond spec
│   ├── Security_Considerations.md  -> Security vulnerabilities and mitigation ideas
│   └── Usage_Documentation.md      -> Full GraphQL usage reference and testing inputs
├── .gitignore         -> Standard exclusions e.g database file, /venv etc          
├── requirements.txt   -> For the dependencies used in the virtual environment
└── README.md          -> This document
```
*Generated using [tree.nathanfriend.com](https://tree.nathanfriend.com)*

**NOTE:** `taskData.db` is included in .gitignore, when the file is missing a fresh one is created automatically when server is first launched.

## GraphQL API Structure
The following operatons are implemented as requested with 2 additional operations and one enhancement for filterng  the  `tasks` query by includiing an optional completed boolean arguement to filter with.

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

## Usage guide for Queries & Mutations
The API has aformentioned query and mutation operations to use, for a full set of inputs, types, operations with examples showing input combinations that would be exepected to be  included in 'for devs' API docs, refer to the [Usage Documentation](docs/Usage_Documentaton.md).

## Design Aspects
* All queries and mutations use a pre-define input type as requested.
* DateTime fields use `Optional` in the GraphQL task type to ensure that nullable fields or optional filters don't raise errors. This is because the feilds fro `created_at` and `updated_at` are set on update to the database not during API request.
* All the search filters for `tasks` are optonal, the query can be called without any input provided. 
* For `tasks` query the use of `List[TaskType]` will always return an array even if empty, to match GraphQL design best practices.
* `taskStats` query and `updateTask` are introduced as two **bonus operations**.
* An optional search parameter `completed` filters completed tasks from non completed tasks, added as a parameter of pre-required `tasks` query as to meet within spec allowance of 2 additional operations.

## Handling Complex Error Scenarios
This API handles basic errors gracefully and predictably. Queries and mutations follow GraphQL best practices by returning `null` when an object is not found (e.g. querying a non-existent task ID). All inputs are validated via Strawberry input types, ensuring correct types and required fields. All of which were requested as part of the task spec.

The base GraphQL schema instructed to be made has simple operations that assume minimal failure paths or error cases. In larger or production-grade implementations, error handling would extend beyond basic validation. Examples include:

- **Concurrent updates or database conflicts:** Transactions could be wrapped with SQLAlchemy session rollbacks to maintain integrity if two users modify the same task simultaneously.
- **Request throttling:** Implementing a rate limiter (e.g. using FastAPI middleware) would protect against excessive requests or Denial of Service attempts.
- **Data corruption recovery:** Periodic backups or transactional journaling could allow restoring state after unexpected server shutdowns.
- **Partial failure handling:** In multi-step mutations, compensating actions could roll back prior steps if a later operation fails.
- **User accountability:** Logs or audit trails could be implemented to trace the origin of invalid or destructive mutations.

These concepts are outside the current specification but demonstrate how the existing API structure can evolve into a more fault-tolerant system.

This section is very brief to keep the README as concise and well presented as can be while being informative. For a more comprehensive dive and discussion of edge cases, future-proofing, and advanced error-handling considerations, see [Complex_Error_Handling.md](docs/Complex_Error_Handling.md).

Additionally, although not part of the task, a discussion into the scalability and security factors that would be considered in a real-world back-end scenario are included as an additonal demonstration of concepts. If there is interest in further reading into this area,  please see [Security_Considerations.md](docs/Security_Considerations.md)

## License

MIT License (Public may fork and build on this template)

## Author Notes

This README and the associated implementation were created for submission to a take-home technical assessment. While designed to meet a precise spec, the project may be expanded into a task manager boilerplate or learning scaffold in future forks for other projects.

For purpose of defending this as being an independent work, all implementation decisions are shown to be understood and deliberate by using comments, this `README`, and commit history to provide further insight into the journey in building this simple API.

Special thanks to the back-end team at [Lush](https://lush.pinpointhq.com/) who gave me this chance to not only show what I can do but also presented an enjoyable oportunity to learn some valuable insight and skills.