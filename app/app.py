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
    
    @staticmethod
    def get_user(user_id):
        # Get user from the database
        cursor.execute("SELECT * FROM user WHERE userID = %s", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(user_data[0], user_data[1])  # Create a User object
        return None

    def create_post(self, content, location_id, tagged_friends):
        # Create a new post

        location = Location.get_location(location_id)
        post = Post(content, location, self)
        
        # Save tagged friends to the database
        for friend_id in tagged_friends:
            cursor.execute("INSERT INTO posttaggedfriends (postID, userID) VALUES (%s, %s)", (post.postID, friend_id))

        db_connection.commit()
        return post
    


    @staticmethod
    def viewpost():
        cursor.execute("SELECT * FROM post ORDER BY timestamp DESC")
        posts = cursor.fetchall()
        return jsonify({"posts": posts})
    
    @staticmethod
    def views_post_user_id(user):
        cursor.execute("SELECT * FROM post WHERE user_id = %s", (user.user_id,))
        user_posts = cursor.fetchall()
        return jsonify({"user_posts": user_posts})
    
    @staticmethod
    def viewPostsByLocation(location):
        # Get Location from get location function
            cursor.execute("SELECT * FROM post WHERE locationID = %s", (location.locationID,))
            location_posts = cursor.fetchall()
            return jsonify({"location_posts": location_posts})


class Post:
    post_id_counter = 1

    def __init__(self, content, location, user):
        self.postID = Post.post_id_counter
        Post.post_id_counter += 1
        self.content = content
        self.timestamp = datetime.now()
        self.location = location
        self.user = user

        # Save the post to the database
        cursor.execute("INSERT INTO post (content, timestamp, locationID, user_id) VALUES (%s, %s, %s, %s)",
                       (self.content, self.timestamp, self.location.locationID, self.user.user_id))
        db_connection.commit()

        


class Location:
    def __init__(self, location_id, name):
        self.locationID = location_id
        self.name = name
        
    @staticmethod
    def get_location(location_id):
        cursor.execute("SELECT * FROM location WHERE locationID = %s", (location_id,))
        location = cursor.fetchone()
        if location:
            return Location(location[0], location[1])
        else:
            return None
        
@app.route('/post', methods=['POST']    )
def create_post():
    data = request.json
    user = User.get_user(data['user_id'])
    if user:
        user.create_post(data['content'], data['location_id'], data['tagged_friends'])
        return jsonify({"message": "Post created successfully"})
    else:
        return jsonify({"error": "User not found."})

# REST API route to view all posts by the most recent time
@app.route('/view', methods=['GET'])
def view_all_posts():
    post = User.viewpost()
    return post


# REST API route to view all posts by a specific user
@app.route('/view/user/<int:user_id>', methods=['GET'])
def view_posts_by_user(user_id):
    user = User.get_user(user_id)
    if user:
        post = user.views_post_user_id(user)
        return post
    else:
        return jsonify({"error": "User not found."})
    

# REST API route to view all posts from a specific location
@app.route('/view/location/<int:location_id>', methods=['GET'])
def view_posts_by_location(location_id):
    location = Location.get_location(location_id)
    if location:
        post = User.viewPostsByLocation(location)
        return post
    else:
        return jsonify({"error": "Location not found."})
if __name__ == '__main__':
    app.run(debug=True)