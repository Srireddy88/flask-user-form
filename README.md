# Flask User Form App with CI/CD

## Overview
This project is a **simple Flask web application** with a form to submit user information and a SQLite database to store entries. It demonstrates **CI/CD deployment** to **AWS EC2** using **GitHub Actions**.

**Resume Bullet:**  
> Implemented CI/CD pipeline with GitHub Actions and AWS EC2, reducing deployment time from minutes to seconds.

---

## Features
- Simple frontend form (HTML + CSS)
- Flask backend handling form submissions
- SQLite database for storing user entries
- CI/CD pipeline using GitHub Actions
- Automatic deployment to EC2 and managed via **systemd**

---

## Project Structure
flask-user-form/
│
├─ app.py # Flask backend
├─ requirements.txt # Python dependencies
├─ templates/
│ ├─ index.html # Form page
│ └─ list.html # Display entries
├─ static/
│ └─ style.css # Styling
└─ venv/ # Python virtual environment
### 1. Clone the repository
```bash
git clone git@github.com:Srireddy88/flask-user-form.git
cd flask-user-form
```
### 2. Create Python virtual environment
```
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

```
### 3. Update Flask to listen externally
```
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)

```
### So currently, without Nginx:
```
http://3.91.8.117>:5000/

```
### With Nginx reverse proxy configured:
```
http://3.91.8.117

```
### 4. Create systemd service on EC2
```
sudo vim /etc/systemd/system/flask-app.service
```
```
[Unit]
Description=Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/flask-user-form
ExecStart=/home/ubuntu/flask-user-form/venv/bin/python3 /home/ubuntu/flask-user-form/app.py
Restart=always
Environment="PATH=/home/ubuntu/flask-user-form/venv/bin:/usr/bin:/bin"

[Install]
WantedBy=multi-user.target


```
###
```
sudo systemctl daemon-reload
sudo systemctl enable flask-app
sudo systemctl start flask-app
sudo systemctl status flask-app

```
### 5. Open EC2 Security Group
```
http://3.91.8.117:5000/

```
### 6. CI/CD Pipeline (GitHub Actions)

Workflow file: .github/workflows/deploy.yml

On every push to main:

Files are copied to EC2

Virtual environment is updated

Dependencies installed

Flask app restarted via systemd

### GitHub Secrets Required

EC2_HOST → EC2 public IP

EC2_SSH_KEY → Private SSH key for EC2 access

### 7. Verify Deployment
```
sudo systemctl status flask-app
journalctl -u flask-app -f

```
```
http://3.91.8.117
```
