from flask import Blueprint, redirect, render_template, request, url_for, session

from post_rules import validate_post
from repositories import posts

blueprint = Blueprint("posts", __name__)


@blueprint.before_request
def require_login():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"), code=303)


def not_found():
    return render_template(
        "error.html", status_code=404, message="게시글을 찾을 수 없습니다.",
        description="삭제되었거나 존재하지 않는 글입니다. 목록에서 다른 글을 확인해 주세요.",
    ), 404


@blueprint.get("/")
def index():
    return render_template("index.html", posts=posts.list_posts())


@blueprint.get("/board/<int:post_id>")
def detail(post_id: int):
    post = posts.find_post(post_id)
    if post is None:
        return not_found()
    return render_template("detail.html", post=post)


@blueprint.route("/board/new", methods=["GET", "POST"])
def new():
    values = {"title": "", "body": ""}
    if request.method == "POST":
        values = {"title": request.form.get("title", ""), "body": request.form.get("body", "")}
        title, body, errors = validate_post(values["title"], values["body"])
        if errors:
            return render_template("new.html", values=values, errors=errors), 400
        post = posts.create_post(title, body)
        return redirect(url_for("posts.detail", post_id=post["id"]), code=303)
    return render_template("new.html", values=values, errors={})


@blueprint.route("/board/<int:post_id>/edit", methods=["GET", "POST"])
def edit(post_id: int):
    post = posts.find_post(post_id)
    if post is None:
        return not_found()
    values = {"title": post["title"], "body": post["body"]}
    if request.method == "POST":
        values = {"title": request.form.get("title", ""), "body": request.form.get("body", "")}
        title, body, errors = validate_post(values["title"], values["body"])
        if errors:
            return render_template("edit.html", post=post, values=values, errors=errors), 400
        updated = posts.update_post(post_id, title, body)
        if updated is None:
            return not_found()
        return redirect(url_for("posts.detail", post_id=post_id), code=303)
    return render_template("edit.html", post=post, values=values, errors={})


@blueprint.route("/board/<int:post_id>/delete", methods=["GET", "POST"])
def delete(post_id: int):
    if request.method == "POST":
        deleted = posts.delete_post(post_id)
        if deleted is None:
            return not_found()
        return redirect(url_for("posts.index"), code=303)
    post = posts.find_post(post_id)
    if post is None:
        return not_found()
    return render_template("delete.html", post=post)
