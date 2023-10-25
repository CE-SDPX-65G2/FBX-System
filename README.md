# FBX-System
FBX-System 

## User Stories for an FBX System
- As a user, I want to post, so that my post is publicly read.
- As a user, I want to tag my friends, so that the post is also on my friends wall.
- As a user, I want to tag a location, so that the post has a location.
- As a user, I want to view all posts by recently time.
- As a user, I want to view all posts from a specific user.
- As a user, I want to view all posts by a location.

### Write a Class Diagram
### Write Sequence Diagrams
### Write APIs for this system
  (Following the Classes and Objects from the design)
  /post   						(with json input and save into **DB**)
  /view   						(return all posts)
  /view/user/{user_id}   			(return all posts from a user_id)
  /view/location/{location_id}   	(return all posts from a location_id)

