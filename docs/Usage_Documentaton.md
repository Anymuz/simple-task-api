
# Example GraphQL Operations
These operations can be run for testing at `http://localhost:8000/task-api` once the server is running.

## Object Types (`@strawberry.type`)
The GraphQL schema types used in the task management API are documented below

### `TaskType`
Represents a single task object returned by most queries and mutations.
```graphql
type TaskType {
  id: Int!
  title: String!
  completed: Boolean!
  createdAt: String
  updatedAt: String
}
```

### `TaskStats`
Returned by the `taskStats` query to show total task counts.
```graphql
type TaskStats {
  total: Int!
  completed: Int!
  pending: Int!
}
```

## Query Operations (`@strawberry.field`)
This section gives details on the set of query operations available with this API.

### Query: `tasks(input?)`
**Returns a list of all tasks. Optional filtering by search string or completion status.**
```graphql
query {
  tasks {
    idtasks
    title
    completed
    createdAt
    updatedAt
  }
}
```

**Filter by search term**
```graphql
query {
  tasks(input: { search: "git" }) {
    id
    title
    completed
  }
}
```

**Filter by completed status**
```graphql
query {
  tasks(input: { completed: false }) {
    id
    title
    completed
  }
}
```

**Filter by both search and completed**
```graphql
query {
  tasks(input: { search: "readme", completed: true }) {
    id
    title
    completed
  }
}
```

### Query: `task(input)`
**Get a specific task by ID**
```graphql
query {
  task(input: { id: 1 }) {
    id
    title
    completed
    createdAt
    updatedAt
  }
}
```

### Query: `taskStats`
**Get task summary stats**
```graphql
query {
  taskStats {
    total
    completed
    pending
  }
}
```

## Mutation Operations (`@strawberry.mutation`)
This section gives details on the set of mutation operations available with this API.

### Mutation: `addTask(input)`
**Create a new task**
```graphql
mutation {
  addTask(input: { title: "Commit  to git" }) {
    id
    title
    completed
    createdAt
  }
}
```

### Mutation: `toggleTask(input)`
**Toggle completion status**
```graphql
mutation {
  toggleTask(input: { id: 1 }) {
    id
    title
    completed
    updatedAt
  }
}
```

### Mutation: `deleteTask(input)`
**Delete a task by ID**
```graphql
mutation {
  deleteTask(input: { id: 1 }) {
    id
    title
  }
}
```

### Mutation: `updateTask(input)`
**Update a task's title**
```graphql
mutation {
  updateTask(input: { id: 2, newTitle: "Update readme" }) {
    id
    title
    updatedAt
  }
}
```

## Input Types Used in GraphQL API (`@strawberry.input`)
This section outlines the custom input types used in the GraphQL operations defined in the task management API.

### `NewTaskInput`
Used in: `add_task` mutation
```graphql
input NewTaskInput {
  title: String!
}
```

### `UpdateTaskInput`
Used in: `update_task` mutation
```graphql
input UpdateTaskInput {
  id: Int!
  new_title: String!
}
```

### `TaskIdInput`
Used in: `task`, `toggle_task`, and `delete_task` operations
```graphql
input TaskIdInput {
  id: Int!
}
```

### `TaskListInput`
Used in: `tasks` query for filtering task results
```graphql
input TaskListInput {
  search: String
  completed: Boolean
}
```

## Error Handling
ID mismatchhes in mutations and queries that use `taskIDInput` will return `null` if the ID provided doesn't match a task. In the `updateTask` mutatuiion, empty or whitespace-only `newTitle` inputs will raise the error below
```json
{
  "errors": [
    {
      "message": "Task title cannot be empty."
    }
  ]
}
```