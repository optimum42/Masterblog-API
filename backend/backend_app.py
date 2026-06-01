from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def get_next_id():
    """ Returns the next available post id """
    if len(POSTS) == 0:
        return 1
    return max(post["id"] for post in POSTS) + 1


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    Returns a list of all posts
    optional query params can control the sorting:
    sort=title: sorted by title
    sort=content: sorted by content
    direction=asc sort in ascending order
    direction=desc sort in descending order
    """
    sort = request.args.get('sort', '').strip().lower()
    direction = request.args.get('direction', '').strip().lower()
    if sort == "":
        return jsonify(POSTS), 200

    if sort not in ["title", "content"]:
        message = "Please provide 'title' or 'content' as a sorting parameter."
        return jsonify({"message": message}), 400

    if direction != "" and direction not in ["asc", "desc"]:
        message = "Please provide 'asc' or 'desc' as a direction parameter."
        return jsonify({"message": message}), 400

    sorted_posts = sorted(POSTS, key=lambda x: x[sort],
                               reverse=direction == "desc")
    return jsonify(sorted_posts), 200


@app.route('/api/posts', methods=['POST'])
def add_post():
    """ Adds a new post to the list of posts """
    data = request.get_json()
    title = data.get("title").strip()
    content = data.get("content").strip()

    if title is None or title == "":
        return jsonify({"message": "Please provide a title."}), 400
    if content is None or content == "":
        return jsonify({"message": "Please provide a content."}), 400

    post = {"id": get_next_id(), "title": title, "content": content}
    POSTS.append(post)
    return jsonify(post), 201


@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """
    Deletes a post from the list of posts and returns a success message
    If post id is not found, returns a 404 status and a message
    """
    for post in POSTS:
        if post["id"] == post_id:
            POSTS.remove(post)
            return jsonify({"message": f"Post with id={post_id} successfully deleted"}), 200

    return jsonify({"message": f"Post with id={post_id} not found."}), 404


@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    """
    Updates a post from the list of posts
    Returns the updated post if post id exists
    If post id is not found, returns a 404 status and a message
    """
    for post in POSTS:
        if post["id"] == post_id:
            data = request.get_json()
            post["title"] = data.get("title") or post.get("title")
            post["content"] = data.get("content") or post.get("content")
            return jsonify(post), 200

    return jsonify({"message": f"Post with id={post_id} not found."}), 404



@app.route("/api/search", methods=["GET"])
def search_posts():
    """
    Returns a filtered list of all posts where query params
    title and/or content matches the appropriate fields in the posts
    """
    title = request.args.get('title', '').strip().lower()
    content = request.args.get('content', '').strip().lower()
    filtered_posts = [
        post for post in POSTS
        if ((not title) or (title in post["title"].lower())) and
           ((not content) or (content in post["content"].lower()))
    ]
    return jsonify(filtered_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
