from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# In-memory storage for comments
comments = []

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
    <h2>comments</h2>

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
                method: 'PUT',
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

# API route – get all comments
@app.route("/comments", methods=["GET"])
def get_comments():
    return jsonify(comments)

# API route – add a comment
@app.route("/comments", methods=["POST"])
def add_comment():
    data = request.get_json()
    comment = data.get("comment")
    if comment:
        comments.append(comment)
        return jsonify({"message": "Comment added"}), 201
    return jsonify({"error": "No comment provided"}), 400

# API route – edit/update a comment
@app.route("/comments/<int:index>", methods=["PUT"])
def update_comment(index):
    if 0 <= index < len(comments):
        data = request.get_json()
        comment = data.get("comment")
        if comment:
            comments[index] = comment
            return jsonify({"message": "Comment updated"})
        return jsonify({"error": "No comment provided"}), 400
    return jsonify({"error": "Invalid index"}), 404

# API route –delete a comment
@app.route("/comments/<int:index>", methods=["DELETE"])
def delete_comment(index):
    if 0 <= index < len(comments):
        removed = comments.pop(index)
        return jsonify({"message": f"Comment '{removed}' deleted"})
    return jsonify({"error": "Invalid index"}), 404

if __name__ == "__main__":
    app.run(debug=True)
