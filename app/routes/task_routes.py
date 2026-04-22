from flask import Blueprint, redirect, render_template, request, url_for

from app.models import db
from app.models.task import Task

task_bp = Blueprint("task", __name__)


@task_bp.route("/")
@task_bp.route("/tasks")
def index():
    keyword = request.args.get("q", "").strip()
    status = request.args.get("status", "").strip()

    query = Task.query

    if keyword:
        query = query.filter(
            (Task.title.contains(keyword)) | (Task.description.contains(keyword))
        )

    if status == "completed":
        query = query.filter_by(completed=True)
    elif status == "incomplete":
        query = query.filter_by(completed=False)

    tasks = query.order_by(Task.created_at.desc()).all()
    return render_template("index.html", tasks=tasks, keyword=keyword, status=status)


@task_bp.route("/tasks/create", methods=["GET", "POST"])
def create_task():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        due_date = request.form.get("due_date", "").strip()

        if title:
            task = Task(title=title, description=description, due_date=due_date)
            db.session.add(task)
            db.session.commit()
            return redirect(url_for("task.index"))

    return render_template("create_task.html")


@task_bp.route("/tasks/<int:task_id>")
def task_detail(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template("task_detail.html", task=task)


@task_bp.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        due_date = request.form.get("due_date", "").strip()

        if title:
            task.title = title
            task.description = description
            task.due_date = due_date
            db.session.commit()
            return redirect(url_for("task.task_detail", task_id=task.id))

    return render_template("edit_task.html", task=task)


@task_bp.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("task.index"))


@task_bp.route("/tasks/<int:task_id>/toggle", methods=["POST"])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("task.index"))
    