
# ![Resonance2 Logo](static/images/resonance2.png)

# Resonate

Welcome to the **Resonate**!  
This project provides a stylish matchmaking web app with rich profile interactions and a modern UI for people with eye conditions.

---

## Features

- User authentication and profile management
- Interactive match cards with new match badges  
- Profile popups with photo, bio, audio message, and action buttons  
- Responsive and modern design with animations and gradients  
- REST API integration for profiles and matching actions
- Ideal for people with eye conditions

---

## Getting Started

Follow the instructions below to set up the project locally.

### Prerequisites

- Python 3.8+  
- [pip](https://pip.pypa.io/en/stable/installation/)  
- Virtual environment tool (optional but recommended)

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Patricenko/resonate.git
cd resonate
```

2. **Create and activate a virtual environment (optional but recommended):**

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install required Python packages:**

```bash
pip install -r requirements.txt
```

> If you don't have a `requirements.txt`, you can install Django and Pillow directly:

```bash
pip install django pillow
```

4. **Apply database migrations:**

```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser (optional, for admin access):**

```bash
python manage.py createsuperuser
```

6. **Run the development server:**

```bash
python manage.py runserver
```

7. **Open your browser and go to:**  
```
http://127.0.0.1:8000/
```

---

## Additional Notes

  For it to appear in this README on GitHub, you may want to copy it to the root or a docs folder or upload it to GitHub separately and link it with an absolute URL.  
- Make sure your Django static files are properly configured to serve static assets in development and production.
- For profile images and audio playback, ensure your media files are properly configured and served.
- To stop the server, press `Ctrl+C` in your terminal.

---

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/Patricenko/dinter/issues).

---

## License

This project is licensed under the MIT License.

---

_Enjoy building your matchmaking app with Resonate!_
