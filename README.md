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
![class_diagram](https://github.com/CE-SDPX-65G2/FBX-System/assets/77483621/dfc8571a-9aa8-4453-9d63-681365d2130b)

### Write Sequence Diagrams
![Seq](https://github.com/CE-SDPX-65G2/FBX-System/assets/77483621/2db9289a-88fe-4c73-9e44-c2305e129aa7)

### Write APIs for this system
  (Following the Classes and Objects from the design)
  /post   						(with json input and save into **DB**)
  /view   						(return all posts)
  /view/user/{user_id}   			(return all posts from a user_id)
  /view/location/{location_id}   	(return all posts from a location_id)

