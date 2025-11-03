# Security Considerations
These notes accompany the GraphQL Task API submission but are not included as part of the given task scope therefore have been put into a seperate document. They are written to showcase the way cyber security knowledge can benefit backend developmment. This is intended to show how the API might be adapted for more advanced use in a real-world deployment scenario with security principles adhered to.

## Security Specific Error Handling Considerations 
Protection of the back-end data integrity and service availability would require connsiderationns of the following:

* Distinguishing between different types of updates (e.g. editing title vs. toggling completion) to avoid ambiguity in the `updated_at` field. Could be done with a second timestamp or status-specific metadata.
* Implementing soft deletes (logical deletion flag or delayed hard delete) to allow accidental deletions to be reversed.
* Periodic database backups or auto-rollback points would prevent irreversible damage from unexpected failures or corruption.
* Adding simple rate limits to prevent flooding the server with requests or accidental DoS scenarios.
* Recognising basic indicators of bot or script activity based on unusual request patterns (e.g. auto-incremental ID querying, mass deletion or toggling of tasks).

## Authentication and Multi-User Expansion
In the event this API is extended to support multiple users, the following would need to be added to ensure data confidentiality:

* A `User` table or model, with each task linked by a `user_id` field (foreign key).
* Authentication mechanism:
  - User registration with hashed passwords
  - Token or session-based login (e.g. JWT)
* Session handling:
  - Expiring unused sessions
  - Optional: Bind sessions to IP for extra hijack prevention

Tasks would only be accessible to the authenticated user, and queries will need to be filtered accordingly, user-based database schema is a common solution to this over relying on a query to correctly filter the user ID.

## API Key / Session Token Handling
With the above considerations, measures further need to protect the authentication that is required. This means the following standard security practices should along-side be implemented:
* Do not store passwords or tokens in plaintext. Always encrypt or hash securely incase of database leak.
* Avoid permanent tokens for login. Use short-lived tokens and refresh sessions periodically in event that session hi-jacking occures.
* Allow tokens to be revoked (either manually or automatically) if suspicious activity is detected.

## Potential Directions for Feature Expansion 
By handling the complex error scenarios and implementing these security measures, some of the future potential cases that can be built on this simple but scalable API include:
* Task assignment — ability to assign or share tasks with other users
* Project groups — tasks could be grouped into categories, stages or boards
* Notifications or reminders — optional email or system alert integration
* Admin moderation — in the event of public or shared usage, allow moderation or oversight by elevated users

## Front-end Safety Additions
Althought this is a back-end task, front-end development would ideally support the common goal of security and usability with measures such as:
* Ask for confirmation before deleting tasks (in a real UI situation)
* Add a task change log or audit table to track all edits or deletions

## Summary
Although not required by the specification given, the above notes demonstrate how a simple single-user task API could form the foundation of a more complex backend system with proper consideration. The intent of this additional reading document is to show awareness of the kind of architectural, security, and scaling concerns that would arise in a real product scenario.
