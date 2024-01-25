from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.tree import Tree
from flask import flash


# TODO Tree Form
@app.route("/tree/add")
def add_tree():
    if "user_id" not in session:
        return redirect("/")
    else:
        user_id = session["user_id"]
        user = User.get_by_id({"id": user_id})
        trees = Tree.get_all({"user_id": user_id})
        return render_template("create_tree.html", user=user, trees=trees)


# TODO Create Tree
@app.route("/tree/create", methods=["POST"])
def create_tree():
    if "user_id" not in session:
        return redirect("/")
    user_id = int(session["user_id"])
    data = {
        "species": request.form["species"],
        "location": request.form["location"],
        "reason": request.form["reason"],
        "date_planted": request.form["date_planted"],
        "user_id": user_id,
    }
    Tree.save(data)
    return redirect("/dashboard")


# TODO Show Tree
@app.route("/tree/show/<int:id>")
def show(id):
    data = {"id": id}
    return render_template(
        "tree_detail.html", tree=Tree.get_one(data), user=User.get_by_id(data)
    )


# TODO My Trees
@app.route("/user/account")
def user_account():
    if "user_id" not in session:
        return redirect("/")
    else:
        user_id = session["user_id"]
        user = User.get_by_id({"id": user_id})
        trees = Tree.get_all({"id": user_id})
        return render_template("user_account.html", user=user, trees=trees)


# TODO Edit Tree
@app.route("/tree/edit/<int:tree_id>")
def edit_tree(tree_id):
    if "user_id" not in session:
        return redirect("/")
    tree_data = {"id": tree_id}
    tree = Tree.get_one(tree_data)
    data = {"id": session["user_id"]}
    user = User.get_by_id(data)
    return render_template("edit_tree.html", user=user, tree=tree)


# TODO Update Tree
@app.route("/tree/update/<int:tree_id>", methods=["POST"])
def update_tree(tree_id):
    data = {
        "id": tree_id,
        "species": request.form["species"],
        "location": request.form["location"],
        "reason": request.form["reason"],
        "date_planted": request.form["date_planted"],
    }
    Tree.update(data)
    return redirect("/user/account")


# TODO Delete Tree
@app.route("/tree/delete/<int:tree_id>")
def delete_tree(tree_id):
    data = {"id": tree_id}
    Tree.delete(data)
    return redirect("/user/account")
