from flask import render_template


def administracion():
    return render_template(
        "user/moduloadministrativo.html",
        #username=user["username"],
    )