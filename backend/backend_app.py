from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    if title is None or title == "":
        return jsonify({"message": "Please provide a title."}), 401
    if content is None or content == "":
        return jsonify({"message": "Please provide a content."}), 401

    post = {"id": 3, "title": title, "content": content}
    POSTS.append(post)
    return jsonify(post), 201


@app.route('/api/posts/<id>', methods=['DELETE'])
def delete_post(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({"message": "Please provide an integer id."}), 401

    for post in POSTS:
        if post["id"] == id:
            POSTS.remove(post)
            return jsonify({"message": f"Post with id={id} successfully deleted"}), 200

    return jsonify({"message": f"Post with id={id} not found."}), 404


@app.route('/api/posts/<id>', methods=['PUT'])
def update_post(id):
    try:
        id = int(id)
    except ValueError:
        return jsonify({"message": "Please provide an integer id."}), 401

    post_exists = False
    for post in POSTS:
        if post["id"] == id:
            post_exists = True
            break

    if not post_exists:
        return jsonify({"message": f"Post with id={id} not found."}), 404

    data = request.get_json()
    post["title"] = data.get("title") or post.get("title")
    post["content"] = data.get("content") or post.get("content")

    return jsonify(post), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
