# EcoChallenge

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd EcoChallenge
   ```

2. **Create a virtual environment (recommended):**
   ```sh
   python -m venv .venv
   # On Windows (PowerShell):
   .venv\Scripts\Activate
   # On Windows (cmd):
   .venv\Scripts\activate.bat
   # On Unix/Mac:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```

5. **Load initial data (optional):**
   ```sh
   python manage.py loaddata myapp/fixtures/initial_data.json
   ```

6. **Create a superuser (for admin access):**
   ```sh
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

8. **Access the app:**
   - Home: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

---

## Notes
- Make sure you have Python 3.8+ installed.
- All dependencies (including Pillow for image uploads) are listed in `requirements.txt`.
- For any issues, ensure your virtual environment is activated and dependencies are installed.

---

## Troubleshooting

### Pillow/ImageField Error
If you see an error like:
```
myapp.Reward.image: (fields.E210) Cannot use ImageField because Pillow is not installed.
```
This means Pillow is not installed **inside your virtual environment**.

**Solution:**
1. Activate your virtual environment:
   - On Windows (PowerShell):
     ```powershell
     .venv\Scripts\Activate
     ```
   - On Windows (cmd):
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - On Unix/Mac:
     ```sh
     source .venv/bin/activate
     ```
2. Install Pillow:
   ```sh
   pip install Pillow
   ```
3. Run your server again:
   ```sh
   python manage.py runserver
   ```

**Note:** Installing Pillow globally (outside the virtual environment) will not fix this error. Always activate your virtual environment before installing dependencies or running the server. 