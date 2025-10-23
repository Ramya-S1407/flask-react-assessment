import json
import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# JSON file to persist comments
COMMENTS_FILE = "comments.json"

# Load comments from file if exists
if os.path.exists(COMMENTS_FILE):
    with open(COMMENTS_FILE, "r") as f:
        comments = json.load(f)
else:
    comments = []

# Helper function to save comments to file
def save_comments():
    with open(COMMENTS_FILE, "w") as f:
        json.dump(comments, f)

# HTML template (inline for simplicity)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 20px auto; }
        input, button { padding: 5px; margin: 5px; }
        li { margin-bottom: 8px; }
    </style>
</head>
<body>
    <h2>Comments</h2>

    <input type="text" id="commentInput" placeholder="Add a comment">
    <button onclick="addComment()">Add</button>

    <ul id="commentList"></ul>

    <script>
        async function fetchComments() {
            const res = await fetch('/comments');
            const data = await res.json();
            const list = document.getElementById('commentList');
            list.innerHTML = '';
            data.forEach((comment, index) => {
                const li = document.createElement('li');
                li.innerHTML = `
                    ${comment} 
                    <button onclick="editComment(${index})">Edit</button>
                    <button onclick="deleteComment(${index})">Delete</button>
                `;
                list.appendChild(li);
            });
        }

        async function addComment() {
            const input = document.getElementById('commentInput');
            const text = input.value.trim();
            if (!text) return;
            await fetch('/comments', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ comment: text })
            });
            input.value = '';
            fetchComments();
        }

        async function editComment(index) {
            const newText = prompt("Edit comment:");
            if (newText === null || newText.trim() === "") return;
            await fetch('/comments/' + index, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ comment: newText })
            });
            fetchComments();
        }

        async function deleteComment(index) {
            await fetch('/comments/' + index, { method: 'DELETE' });
            fetchComments();
        }

        // Load comments on page load
        fetchComments();
    </script>
</body>
</html>
"""

# Home route – serves HTML
@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

# GET all comments
@app.route("/comments", methods=["GET"])
def get_comments():
    return jsonify(comments)

# GET single comment by index
@app.route("/comments/<int:index>", methods=["GET"])
def get_comment(index):
    if 0 <= index < len(comments):
        return jsonify({"comment": comments[index]})
    return jsonify({"error": "Invalid index"}), 404

# Add a comment
@app.route("/comments", methods=["POST"])
def add_comment():
    data = request.get_json()
    comment = data.get("comment")
    if comment:
        comments.append(comment)
        save_comments()  # save to file
        return jsonify({"message": "Comment added"}), 201
    return jsonify({"error": "No comment provided"}), 400

# Edit/update a comment
@app.route("/comments/<int:index>", methods=["PUT", "PATCH"])
def update_comment(index):
    if 0 <= index < len(comments):
        data = request.get_json()
        comment = data.get("comment")
        if comment:
            comments[index] = comment
            save_comments()  # save edits to file
            return jsonify({"message": "Comment updated"})
        return jsonify({"error": "No comment provided"}), 400
    return jsonify({"error": "Invalid index"}), 404

# Delete a comment
@app.route("/comments/<int:index>", methods=["DELETE"])
def delete_comment(index):
    if 0 <= index < len(comments):
        removed = comments.pop(index)
        save_comments()  # save after deletion
        return jsonify({"message": f"Comment '{removed}' deleted"})
    return jsonify({"error": "Invalid index"}), 404

#Added the main function
if __name__ == "__main__":
    app.run(debug=True)
