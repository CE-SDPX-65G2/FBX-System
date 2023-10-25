from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASS')
DB_DATABASE = os.getenv('DB_NAME')

print(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE)

app = Flask(__name__)

# Define MySQL connection parameters
mysql_config = {
    'host': DB_HOST,
    'user': DB_USER,
    'password': DB_PASSWORD,
    'database': DB_DATABASE,
}

# Initialize a MySQL connection
db_connection = mysql.connector.connect(**mysql_config)
cursor = db_connection.cursor()

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.posts = []
        self.friends = set()  # Store friends as a set of user IDs
    
    @staticmethod
    def get_user(user_id):
        # Get user from the database
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data[0], user_data[1])  # Create a User object
        return None
        

    def addFriend(self, friend):
        self.friends.add(friend.user_id)

    def createPost(self, content, location, tagged_friends):
        post = Post(content, location, self, tagged_friends)
        return post

class Post:
    post_id_counter = 1

    def __init__(self, content, location, user, tagged_friends):
        self.postID = Post.post_id_counter
        Post.post_id_counter += 1
        self.content = content
        self.timestamp = datetime.now()
        self.location = location
        self.user = user
        self.taggedFriends = tagged_friends  # List of user IDs

        # Save the post to the database
        cursor.execute("INSERT INTO posts (content, timestamp, location_id, user_id) VALUES (%s, %s, %s, %s)",
                       (self.content, self.timestamp, self.location.locationID, self.user.user_id))
        db_connection.commit()

class Location:
    def __init__(self, location_id, name):
        self.locationID = location_id
        self.name = name
        

    @staticmethod
    def get_location(location_id):
        cursor.execute("SELECT * FROM locations WHERE location_id = %s", (location_id,))
        location = cursor.fetchone()
        if location:
            return Location(location[0], location[1])
        else:
            return None
        
# REST API route to create a new post with tagged friends
@app.route('/post', methods=['POST'])
def create_post():
    data = request.get_json()
    user_id = data['user_id']
    content = data['content']
    location_id = data['location_id']
    tagged_friends = data.get('tagged_friends', [])

    # Retrieve user and location information from the database
    user = User.get_user(user_id)
    location = Location.get_location(location_id)

    if user and location:
        tagged_friends = [User.get_user(friend_id) for friend_id in tagged_friends]
        post = user.createPost(content, location, tagged_friends)
        return jsonify({"message": "Post created successfully", "postID": post.postID})
    else:
        return jsonify({"error": "User or location not found."})

# REST API route to view all posts by the most recent time
@app.route('/view', methods=['GET'])
def view_all_posts():
    cursor.execute("SELECT * FROM posts ORDER BY timestamp DESC")
    posts = cursor.fetchall()
    return jsonify({"posts": posts})


# REST API route to view all posts by a specific user
@app.route('/view/user/<int:user_id>', methods=['GET'])
def view_posts_by_user(user_id):
    cursor.execute("SELECT * FROM posts WHERE user_id = %s", (user_id,))
    user_posts = cursor.fetchall()
    return jsonify({"user_posts": user_posts})

# REST API route to view all posts from a specific location
@app.route('/view/location/<int:location_id>', methods=['GET'])
def view_posts_by_location(location_id):
    # Get Location from get location function
    location = Location.get_location(location_id)
    if location:
    # GET post from database1
        cursor.execute("SELECT * FROM posts WHERE location_id = %s", (location_id,))
        location_posts = cursor.fetchall()
        return jsonify({"location_posts": location_posts})
    else:
        return jsonify({"error": "Location not found."})

if __name__ == '__main__':
    app.run(debug=True)