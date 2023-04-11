from app import app
from flask import render_template, request, redirect, session
import users, stories, comments, starred, votes

@app.route("/")
def index():
    pg = request.args.get('pg', default=0, type=int)
    if pg < 0:
        pg = 0
    offset = 10 * pg
    story_list = stories.get_stories_front_page(offset)

    has_next = True
    if len(story_list) <= 10:
        has_next = False

    return render_template("index.html",
                           stories=story_list,
                           is_admin=users.is_admin(),
                           pg=pg,
                           has_next=has_next,
                           ordering="");

@app.route("/newest")
def newest_page():
    pg = request.args.get('pg', default=0, type=int)
    if pg < 0:
        pg = 0

    offset = 10 * pg
    story_list = stories.get_stories_by_newest(offset)

    has_next = True
    if len(story_list) <= 10:
        has_next = False

    return render_template("index.html",
                           stories=story_list,
                           is_admin=users.is_admin(),
                           pg=pg,
                           has_next=has_next,
                           ordering="newest");

@app.route("/oldest")
def oldest_page():
    pg = request.args.get('pg', default=0, type=int)
    if pg < 0:
        pg = 0
    offset = 10 * pg
    story_list = stories.get_stories_by_oldest(offset)

    has_next = True
    if len(story_list) <= 10:
        has_next = False

    return render_template("index.html",
                           stories=story_list,
                           is_admin=users.is_admin(),
                           pg=pg,
                           has_next=has_next,
                           ordering="oldest");

@app.route("/highest")
def highest_voted_page():
    pg = request.args.get('pg', default=0, type=int)
    if pg < 0:
        pg = 0
    offset = 10 * pg
    story_list = stories.get_stories_by_most_votes(offset)

    has_next = True
    if len(story_list) <= 10:
        has_next = False

    return render_template("index.html",
                           stories=story_list,
                           is_admin=users.is_admin(),
                           pg=pg,
                           has_next=has_next,
                           ordering="highest");

@app.route("/lowest")
def lowest_voted_page():
    pg = request.args.get('pg', default=0, type=int)
    if pg < 0:
        pg = 0
    offset = 10 * pg
    story_list = stories.get_stories_by_least_votes(offset)

    has_next = True
    if len(story_list) <= 10:
        has_next = False

    return render_template("index.html",
                           stories=story_list,
                           is_admin=users.is_admin(),
                           pg=pg,
                           has_next=has_next,
                           ordering="lowest");

@app.route("/most")
def most_commented_page():
    pg = request.args.get('pg', default=0, type=int)
    if pg < 0:
        pg = 0
    offset = 10 * pg
    story_list = stories.get_stories_by_most_comments(offset)

    has_next = True
    if len(story_list) <= 10:
        has_next = False

    return render_template("index.html",
                           stories=story_list,
                           is_admin=users.is_admin(),
                           pg=pg,
                           has_next=has_next,
                           ordering="most");

@app.route("/least")
def least_commented_page():
    pg = request.args.get('pg', default=0, type=int)
    if pg < 0:
        pg = 0
    offset = 10 * pg
    story_list = stories.get_stories_by_least_comments(offset)

    has_next = True
    if len(story_list) <= 10:
        has_next = False

    return render_template("index.html",
                           stories=story_list,
                           is_admin=users.is_admin(),
                           pg=pg,
                           has_next=has_next,
                           ordering="least");

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

@app.route("/story/<int:story_id>/edit", methods=["GET", "POST"])
def edit_story(story_id):
    story = stories.get_story(story_id)
    if not story:
        return render_template("error.html", message="story doesn't exist or is hidden")

    user_id = users.user_id()

    if story.user_id != user_id and not users.is_admin():
        return render_template("error.html", message="you can only edit your own stories")

    if request.method == "GET":
        return render_template("editstory.html", story=story)

    if request.method == "POST":
        title = request.form["title"]
        if len(title) > 256:
            return render_template("error.html", message="title was over 256 characters")

        url = request.form["url"]
        if len(url) > 2048:
            return render_template("error.html", message="url was over 2048 characters")

        if stories.edit_story(title, url, story_id):
            return redirect("/story/{}".format(story_id))
        else:
            return render_template("error.html", message="editing story failed")

@app.route("/send", methods=["POST"])
def send():
    title = request.form["title"]
    if len(title) > 256:
            return render_template("error.html", message="title was over 256 characters")

    url = request.form["url"]
    if len(url) > 2048:
            return render_template("error.html", message="url was over 2048 characters")

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if stories.send(title, url):
        return redirect("/")
    else:
        return render_template("error.html", message="creating story failed")

@app.route("/upvote/<int:id>", methods=["POST"])
def upvote(id):
    if users.user_id() == 0:
        return render_template("error.html", message="you have to be logged")

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if votes.add_upvote(id):
        return redirect("/story/{}".format(id))
    else:
        return render_template("error.html", message="upvoting failed")

@app.route("/downvote/<int:id>", methods=["POST"])
def downvote(id):
    if users.user_id() == 0:
        return render_template("error.html", message="you have to be logged")

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if votes.add_downvote(id):
        return redirect("/story/{}".format(id))
    else:
        return render_template("error.html", message="downvoting failed")


@app.route("/story/<int:id>", methods=["GET", "POST"])
def story_page(id):
    story = stories.get_story(id)
    if not story:
        return render_template("error.html", message="story doesn't exist or is hidden")

    if request.method == "GET":
        comment_list = comments.get_list(id)
        return render_template("story.html", story=story, comments=comment_list, is_admin=users.is_admin())

    if request.method == "POST":
        user_id = users.user_id()
        body = request.form["body"]

        if len(body) > 10000:
            return render_template("error.html", message="comment was over 10000 characters")

        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        if comments.send(body, user_id, id):
            return redirect("/story/{}".format(id))
        else:
            return render_template("error.html", message="sending comment failed")

@app.route("/comment/<int:comment_id>", methods=["GET", "POST"])
def comment_page(comment_id):
    comment = comment.get_comment(comment_id)
    if not comment:
        return render_template("error.html", message="comment doesn't exist or is hidden")

    if request.method == "GET":
        story = stories.get_story(comment.story_id)
        user = users.get_user(comment.user_id)
        return render_template("comment.html", comment=comment, story=story, user=user)

    if request.method == "POST":
        user_id = users.user_id()
        body = request.form["body"]

        if len(body) > 10000:
            return render_template("error.html", message="comment was over 10000 characters")

        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        if comments.reply(body, user_id, comment.story_id, comment_id):
            return redirect("/story/{}".format(comment.story_id))
        else:
            return render_template("error.html", message="sending comment failed")

@app.route("/comment/<int:comment_id>/edit", methods=["GET", "POST"])
def edit_comment_page(comment_id):
    comment = comment.get_comment(comment_id)
    if not comment:
        return render_template("error.html", message="comment doesn't exist or is hidden")

    user_id = users.user_id()

    if comment.user_id != user_id and not users.is_admin():
        return render_template("error.html", message="you can only edit your own comments")

    if request.method == "GET":
        story = stories.get_story(comment.story_id)
        return render_template("editcomment.html", comment=comment, story=story)

    if request.method == "POST":
        body = request.form["body"]

        if len(body) > 10000:
            return render_template("error.html", message="comment was over 10000 characters")

        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        if comments.edit_comment(body, comment_id):
            return redirect("/comment/{}".format(comment_id))
        else:
            return render_template("error.html", message="editing comment failed")

@app.route("/comment/<int:comment_id>/hide", methods=["POST"])
def hide_comment_page(comment_id):
    comment = comments.get_comment(comment_id)
    if not comment:
        return render_template("error.html", message="comment doesn't exist or is hidden")

    user_id = users.user_id()

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if comment.user_id != user_id and not users.is_admin():
        return render_template("error.html", message="you can only hide your own comments")

    if comments.hide_comment(comment_id):
        return redirect("/story/{}".format(comment.story_id))
    else:
        return render_template("error.html", message="hiding comment failed")

@app.route("/story/<int:story_id>/hide", methods=["POST"])
def hide_story_page(story_id):
    user_id = users.user_id()
    story = stories.get_story(story_id)
    if not story:
        return render_template("error.html", message="story doesn't exist or is hidden")

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if story.user_id != user_id and not users.is_admin():
        return render_template("error.html", message="you can only hide your own stories")

    if stories.hide_story(story_id):
        return redirect("/")
    else:
        return render_template("error.html", message="hiding stories failed")

@app.route("/starred")
def starred_page():
    user_id = users.user_id()

    if user_id == 0:
        return render_template("error.html", message="you have to be logged")

    story_list = starred.get_starred_for_user(user_id)
    user = users.get_user(user_id)
    return render_template("starred.html", user=user, stories=story_list)

@app.route("/star/<int:id>", methods=["POST"])
def star_page(id):
    if users.user_id() == 0:
        return render_template("error.html", message="you have to be logged")

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if starred.add_starred(id):
        return redirect("/")
    else:
        return render_template("error.html", message="starring failed")

@app.route("/destar/<int:id>", methods=["POST"])
def destar_page(id):
    if users.user_id() == 0:
        return render_template("error.html", message="you have to be logged")

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if starred.remove_starred(id):
        return redirect("/starred")
    else:
        return render_template("error.html", message="starring failed")

@app.route("/profile/<int:id>")
def profile_page(id):
    user = users.get_user(id)
    if user == None:
        return render_template("error.html", message="profile not found")

    story_list = stories.get_stories_by_user(id)
    return render_template("profile.html", user=user, stories=story_list)

@app.route("/result")
def result():
    query = request.args["query"]
    story_list = stories.search(query)
    return render_template("result.html", stories=story_list)
