@Summary...........

# 📝 Flask To-Do App

A full-featured Flask-based web app that allows users to organize tasks by categories. This is ideal for learning CRUD operations, PostgreSQL integration, and clean UI interaction using JavaScript.

---
##Features

- ✅ Add/Edit/Delete Users
- 📂 Add/Edit/Delete Categories under each User
- 📌 Add/Edit/Delete Tasks under each Category
- 🧠 Prevents blank and duplicate entries
- 🕒 Shows timestamps for every item (user/category/task)
- ✨ UI interactivity with JavaScript (`script.js`)
- 🎨 CSS styling (`style.css`)
- ⚠️ Confirmation prompts before delete operations

##Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML5, CSS3
- **Database**: SQLite -> Updated to PostgreSQL
- **Tools**: VS Code, Git, GitHub
- **Deployment**:Render

##Installation

Clone the repository:

```bash
git clone https://github.com/sowmyabusinayani/todo-flask-app.git
cd ToDoAPP


Create a virtual environment:

python -m venv venv
venv\Scripts\activate # or venv\Scripts\activate on Windows


Install dependencies:

pip install -r requirements.txt

🚀 Run the App......

python app.py # Runs init_db() on first launch
Visit: http://127.0.0.1:5000/ in your browser.

📂 Project Structure......

ToDoAPP/
├── static/
│ ├── script.js # All frontend JavaScript
│ └── style.css # App styling
├── templates/
│ └── index.html # Jinja2 HTML template
├── app.py # Flask app logic
├── schema.sql # Database schema (DDL)
├── requirements.txt # Python dependencies
├── render.yaml # Render deployment config
└── README.md # You are here!

🌐 Live Demo
Deployed on Render

Visit: https://todo-flask-app-una5.onrender.com/

## Future Enhancements

✅ Drag-and-drop task sorting

📆 Deadline & reminders

👤 User login sessions

🔍 Search & filter tasks

🤝 Contributing
Pull requests are welcome. For major changes, open an issue first to discuss.

📜 License
MIT © 2025 Sowmya Businayani