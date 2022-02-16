A programming blog made with Flask!

The project's main goal is to build a simple API 
with some basic user interface functions. Apply
best practices on app's stucture.

As secondary goals is to aply best practices in code, 
work with JWT tokens, create a clean, neat web app.

Blog main functionality:

User endpoints:

- /register/ (for new user registration)

Takes a JSON payload with username, email 
and password. Checks if name or email are 
on the database.

- /user/name or id (retrieve user data)

Get the data searching by id or username.
If doesn't exist, return error in JSON format.

- /user/name or id (update user)

Recieve data in JSON payload and update
an existing user. If the user not exist, 
return error in JSON format.

- /user/name or id (delete user)

Delete a user by id or by name.

Post endpoints:

- /post/ (new post)

Receive JSON payload for a new post.
Needs the user id.

- /post/id (for deleteting a post)

Takes an id of post as an argument,
find it (if exists) and delete it.

- /post/user name or id (find the posts of user)

Takes as an argument, either user name or id
and return all the post by this user, if any.

- /post/post_id (update a post)

Takes the id of a post as an argument
and update it. Need to have a "title" and
a "body" fields in JSON payload.