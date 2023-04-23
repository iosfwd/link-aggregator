from db import db
from sqlalchemy import text
import users

def get_stories_front_page(offset = 0):
    sql = text("""
    SELECT id, title, url, user_id, created_at, username, vote_sum, comment_count
    FROM story_view
    ORDER BY vote_sum DESC
    LIMIT 10 OFFSET :offset
    """)
    result = db.session.execute(sql, {"offset":offset})
    return result.fetchall()

def get_stories_by_newest(offset = 0):
    sql = text("""
    SELECT id, title, url, user_id, created_at, username, vote_sum, comment_count
    FROM story_view
    ORDER BY created_at DESC
    LIMIT 10 OFFSET :offset
    """)
    result = db.session.execute(sql, {"offset":offset})
    return result.fetchall()

def get_stories_by_oldest(offset = 0):
    sql = text("""
    SELECT id, title, url, user_id, created_at, username, vote_sum, comment_count
    FROM story_view
    ORDER BY created_at ASC
    LIMIT 10 OFFSET :offset
    """)
    result = db.session.execute(sql, {"offset":offset})
    return result.fetchall()

def get_stories_by_most_votes(offset = 0):
    sql = text("""
    SELECT id, title, url, user_id, created_at, username, vote_sum, comment_count
    FROM story_view
    ORDER BY vote_sum DESC
    LIMIT 10 OFFSET :offset
    """)
    result = db.session.execute(sql, {"offset":offset})
    return result.fetchall()

def get_stories_by_least_votes(offset = 0):
    sql = text("""
    SELECT id, title, url, user_id, created_at, username, vote_sum, comment_count
    FROM story_view
    ORDER BY vote_sum ASC
    LIMIT 10 OFFSET :offset
    """)
    result = db.session.execute(sql, {"offset":offset})
    return result.fetchall()

def get_stories_by_most_comments(offset = 0):
    sql = text("""
    SELECT id, title, url, user_id, created_at, username, vote_sum, comment_count
    FROM story_view
    ORDER BY comment_count DESC
    LIMIT 10 OFFSET :offset
    """)
    result = db.session.execute(sql, {"offset":offset})
    return result.fetchall()

def get_stories_by_least_comments(offset = 0):
    sql = text("""
    SELECT id, title, url, user_id, created_at, username, vote_sum, comment_count
    FROM story_view
    ORDER BY comment_count ASC
    LIMIT 10 OFFSET :offset
    """)
    result = db.session.execute(sql, {"offset":offset})
    return result.fetchall()

def get_story(id):
    sql = text("""
    SELECT id, title, url, user_id, created_at, username, vote_sum, comment_count
    FROM story_view
    WHERE id=:id
    """)
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()

def send(title, url):
    user_id = users.user_id()
    if user_id == 0:
        return False

    sql = text("""
    INSERT INTO stories (title, url, user_id)
    VALUES (:title, :url, :user_id)
    """)
    db.session.execute(sql, {"title":title,
                             "url":url,
                             "user_id":user_id})
    db.session.commit()
    return True

def get_stories_by_user(user_id):
    sql = text("""
    SELECT id, title, url, user_id, created_at, hidden
    FROM stories
    WHERE user_id=:user_id
    """)
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def edit_story(title, url, id):
    if users.user_id() == 0:
        return False

    sql = text("""
    UPDATE stories
    SET (title, url) = (:title, :url)
    WHERE stories.id=:id
    """)
    db.session.execute(sql, {"title":title,
                             "url":url,
                             "id":id})
    db.session.commit()
    return True

def hide_story(story_id):
    if users.user_id() == 0:
        return False

    sql = text("""
    UPDATE stories
    SET hidden=TRUE
    WHERE stories.id=:story_id
    """)
    db.session.execute(sql, {"story_id":story_id})
    db.session.commit()
    return True

def search(query):
    sql = text("""
    SELECT id, title, url, user_id, created_at, username, vote_sum, comment_count
    FROM story_view
    WHERE ((title LIKE :query)
    OR (url LIKE :query))
    """)
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    return result.fetchall()
