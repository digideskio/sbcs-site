from application import app
from flask import Flask, request, session
from flask import render_template, redirect, url_for
from flask.ext.login import login_user, login_required, current_user
from sbcswebsite.models import JobPost, NewsPost, Question, Answer, Tag, User, db, question_tag_table, job_post_tag_table, news_post_tag_table
from base64 import urlsafe_b64encode as b64encode, urlsafe_b64decode as b64decode
import requests
import os
import urlparse
import facebook
from sbcswebsite.users import admin_required
from datetime import datetime

@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/calendar")
def calendar(): 
    return render_template("calendar.html")

@app.route("/news")
def news(): 
    newsletter_list = NewsPost.query.order_by(NewsPost.id.desc()).limit(10).all() 
    tags = _tags_for_type(NewsPost, news_post_tag_table, "news_post_tag")
    return render_template("news.html", news_posts=newsletter_list, tags=tags)

@app.route("/news/tags/<tag>")
def news_post_tag(tag):
    news_posts = NewsPost.query.join(news_post_tag_table).join(Tag).filter(Tag.tag == tag).order_by(NewsPost.id.desc()).limit(10).all()
    tags = _tags_for_type(NewsPost, news_post_tag_table, "news_post_tag")
    return render_template("news.html", news_posts=news_posts, tags=tags)

def _tag_from_cols(tup, tag_route):
    id, name, frequency = tup
    tag = Tag()
    tag.id = id
    tag.tag = name
    tag.frequency = frequency
    print name
    tag.url = url_for(tag_route, tag=name)
    return tag

def _tags_for_type(table, join_table, tag_route):
    tags_with_frequency = db.session.query(Tag.id, Tag.tag, db.func.count(Tag.id)).join(join_table).join(table).group_by(Tag.id).all()
    return [_tag_from_cols(tup, tag_route) for tup in tags_with_frequency if tup[2] > 0]

def _get_tags_for_request(existing_tags = None):
    existing_tags = existing_tags or []
    request_tags = request.form.get("tags").split(",")
    db_tags = Tag.query.filter(Tag.tag.in_(request_tags)).all()
    old_tags = db_tags + existing_tags
    old_tag_words = set([tag.tag for tag in old_tags])
    new_tags = [Tag(tag=tag) for tag in request_tags if tag not in old_tag_words]
    return old_tags + new_tags

