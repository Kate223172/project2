from flask import Flask, render_template, request
import random
import string
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def randomizer():
    result = None
    min_val = max_val = 0
    password_length = 8
    items_text = ""
    selected_item = None
    start_date = end_date = datetime.now().date().isoformat()
    random_date = None

    if request.method == "POST":
        action = request.form.get("action")

        if action == "number":
            min_val = float(request.form.get("min", 0))
            max_val = float(request.form.get("max", 100))
            result = random.uniform(min_val, max_val) if request.form.get("float") else random.randint(int(min_val),
                                                                                                       int(max_val))

        elif action == "password":
            password_length = int(request.form.get("length", 8))
            chars = string.ascii_letters + string.digits + string.punctuation
            result = ''.join(random.choice(chars) for _ in range(password_length))

        elif action == "item":
            items_text = request.form.get("items", "")
            items_list = [item.strip() for item in items_text.split(",") if item.strip()]
            if items_list:
                selected_item = random.choice(items_list)

        elif action == "date":
            start_date = request.form.get("start_date", datetime.now().date().isoformat())
            end_date = request.form.get("end_date", datetime.now().date().isoformat())
            start = datetime.strptime(start_date, "%Y-%m-%d").date()
            end = datetime.strptime(end_date, "%Y-%m-%d").date()
            delta = (end - start).days
            random_days = random.randint(0, delta)
            random_date_obj = start + timedelta(days=random_days)
            month_names = {
                1: "января", 2: "февраля", 3: "марта", 4: "апреля",
                5: "мая", 6: "июня", 7: "июля", 8: "августа",
                9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
            }
            random_date = f"{random_date_obj.day} {month_names[random_date_obj.month]} {random_date_obj.year}"

    return render_template(
        "randomizer.html",
        result=result,
        min_val=min_val,
        max_val=max_val,
        password_length=password_length,
        items_text=items_text,
        selected_item=selected_item,
        start_date=start_date,
        end_date=end_date,
        random_date=random_date
    )


if __name__ == "__main__":
    app.run(debug=True)
