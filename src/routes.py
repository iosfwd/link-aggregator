from app import app
from flask import render_template, request, redirect
import users, posts, comments, starred, votes

@app.route("/")
def index():
    post_list = posts.get_posts_front_page()
    return render_template("index.html", posts=post_list, is_admin=users.is_admin());

@app.route("/newest")
def newest_page():
    post_list = posts.get_posts_by_newest()
    return render_template("index.html", posts=post_list, is_admin=users.is_admin());

@app.route("/oldest")
def oldest_page():
    post_list = posts.get_posts_by_oldest()
    return render_template("index.html", posts=post_list, is_admin=users.is_admin());

@app.route("/highest")
def highest_voted_page():
    post_list = posts.get_posts_by_most_votes()
    return render_template("index.html", posts=post_list, is_admin=users.is_admin());

@app.route("/lowest")
def lowest_voted_page():
    post_list = posts.get_posts_by_least_votes()
    return render_template("index.html", posts=post_list, is_admin=users.is_admin());

@app.route("/most")
def most_commented_page():
    post_list = posts.get_posts_by_most_comments()
    return render_template("index.html", posts=post_list, is_admin=users.is_admin());

@app.route("/least")
def least_commented_page():
    post_list = posts.get_posts_by_least_comments()
    return render_template("index.html", posts=post_list, is_admin=users.is_admin());

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="incorrect username or password")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="passwords didn't match")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="registration failed")

@app.route("/new")
def new():
    user_id = users.user_id()

    if user_id == 0:
        return render_template("error.html", message="you have to be logged in")

    return render_template("new.html")

@app.route("/page/<int:post_id>/edit", methods=["GET", "POST"])
def edit_page(post_id):
    post = posts.get_post(post_id)
    user_id = users.user_id()

    if post.user_id != user_id and not users.is_admin():
        return render_template("error.html", message="you can only edit your own posts")

    if request.method == "GET":
        return render_template("editpage.html", post=post)

    if request.method == "POST":
        title = request.form["title"]
        url = request.form["url"]
        if posts.edit_post(title, url, post_id):
            return redirect("/page/{}".format(post_id))
        else:
            return render_template("error.html", message="editing comment failed")

@app.route("/send", methods=["POST"])
def send():
    title = request.form["title"]

    if len(title) > 256:
            return render_template("error.html", message="title was over 256 characters")

    url = request.form["url"]

    if len(url) > 2048:
            return render_template("error.html", message="url was over 2048 characters")

    if posts.send(title, url):
        return redirect("/")
    else:
        return render_template("error.html", message="creating post failed")

@app.route("/upvote/<int:id>", methods=["POST"])
def upvote(id):
    if users.user_id() == 0:
        return render_template("error.html", message="you have to be logged")

    if votes.add_upvote(id):
        return redirect("/page/{}".format(id))
    else:
        return render_template("error.html", message="upvoting failed")

@app.route("/downvote/<int:id>", methods=["POST"])
def downvote(id):
    if users.user_id() == 0:
        return render_template("error.html", message="you have to be logged")

    if votes.add_downvote(id):
        return redirect("/page/{}".format(id))
    else:
        return render_template("error.html", message="downvoting failed")


@app.route("/page/<int:id>", methods=["GET", "POST"])
def page(id):
    if request.method == "GET":
        post = posts.get_post(id)
        vts = votes.get_votes_by_post(id)
        comment_list = comments.get_list(id)
        return render_template("page.html", post=post, comments=comment_list, votes=vts, is_admin=users.is_admin())

    if request.method == "POST":
        user_id = users.user_id()
        body = request.form["body"]

        if len(body) > 10000:
            return render_template("error.html", message="comment was over 10000 characters")

        if comments.send(body, user_id, id):
            return redirect("/page/{}".format(id))
        else:
            return render_template("error.html", message="sending comment failed", is_admin=users.is_admin())

@app.route("/comment/<int:comment_id>", methods=["GET", "POST"])
def comment_page(comment_id):
    if request.method == "GET":
        comment = comments.get_comment(comment_id)
        post = posts.get_post(comment.post_id)
        user = users.get_user(comment.user_id)
        return render_template("comment.html", comment=comment, post=post, user=user)

    if request.method == "POST":
        comment = comments.get_comment(comment_id)
        user_id = users.user_id()
        body = request.form["body"]

        if len(body) > 10000:
            return render_template("error.html", message="comment was over 10000 characters")

        if comments.reply(body, user_id, comment.post_id, comment_id):
            return redirect("/page/{}".format(comment.post_id))
        else:
            return render_template("error.html", message="sending comment failed")

@app.route("/comment/<int:comment_id>/edit", methods=["GET", "POST"])
def edit_comment_page(comment_id):
    comment = comments.get_comment(comment_id)
    user_id = users.user_id()

    if comment.user_id != user_id and not users.is_admin():
        return render_template("error.html", message="you can only edit your own comments")

    if request.method == "GET":
        post = posts.get_post(comment.post_id)
        return render_template("editcomment.html", comment=comment, post=post)

    if request.method == "POST":
        body = request.form["body"]

        if len(body) > 10000:
            return render_template("error.html", message="comment was over 10000 characters")

        if comments.edit_comment(body, comment_id):
            return redirect("/comment/{}".format(comment_id))
        else:
            return render_template("error.html", message="editing comment failed")

@app.route("/comment/<int:comment_id>/hide")
def hide_comment_page(comment_id):
    comment = comments.get_comment(comment_id)
    user_id = users.user_id()

    if comment.user_id != user_id and not users.is_admin():
        return render_template("error.html", message="you can only hide your own comments")

    if comments.hide_comment(comment_id):
        return redirect("/page/{}".format(comment.post_id))
    else:
        return render_template("error.html", message="hiding comment failed")

@app.route("/page/<int:post_id>/hide", methods=["GET", "POST"])
def hide_post_page(post_id):
    user_id = users.user_id()
    post = posts.get_post(post_id)

    if post.user_id != user_id and not users.is_admin():
        return render_template("error.html", message="you can only hide your own posts")

    if posts.hide_post(post_id):
        return redirect("/")
    else:
        return render_template("error.html", message="hiding posts failed")

@app.route("/starred")
def starred_page():
    user_id = users.user_id()

    if user_id == 0:
        return render_template("error.html", message="you have to be logged")

    stories = starred.get_starred_for_user(user_id)
    user = users.get_user(user_id)
    return render_template("starred.html", user=user, stories=stories)

@app.route("/star/<int:id>", methods=["POST"])
def star_page(id):
    if users.user_id() == 0:
        return render_template("error.html", message="you have to be logged")

    if starred.add_starred(id):
        return redirect("/")
    else:
        return render_template("error.html", message="starring failed")

@app.route("/profile/<int:id>")
def profile_page(id):
    user = users.get_user(id)
    if user == None:
        return render_template("error.html", message="profile not found")

    stories = posts.get_posts_by_user(id)
    return render_template("profile.html", user=user, stories=stories)

@app.route("/result")
def result():
    query = request.args["query"]
    post_list = posts.search(query)
    return render_template("result.html", posts=post_list)
