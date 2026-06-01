from flask import Flask, jsonify, request
from flask_cors import CORS


def get_next_id():
    if len(POSTS) == 0:
        return 1
    return max(post["id"] for post in POSTS) + 1


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
    title = data.get("title").strip()
    content = data.get("content").strip()

    if title is None or title == "":
        return jsonify({"message": "Please provide a title."}), 400
    if content is None or content == "":
        return jsonify({"message": "Please provide a content."}), 400

    post = {"id": get_next_id(), "title": title, "content": content}
    POSTS.append(post)
    return jsonify(post), 201


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    for post in POSTS:
        if post["id"] == id:
            POSTS.remove(post)
            return jsonify({"message": f"Post with id={id} successfully deleted"}), 200

    return jsonify({"message": f"Post with id={id} not found."}), 404


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update_post(id):
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


@app.route("/api/search", methods=["GET"])
def search_posts():
    title = request.args.get('title', '').strip().lower()
    content = request.args.get('content', '').strip().lower()
    filtered_posts = []
    for post in POSTS:
        if title != "" and title in post["title"].lower():
            filtered_posts.append(post)

        if (content != ""
                and content in post["content"].lower()
                and post not in filtered_posts): # don't add double
            filtered_posts.append(post)

    return jsonify(filtered_posts), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
