# Flask User Form App with CI/CD

## Overview
This project is a **simple Flask web application** with a form to submit user information and a SQLite database to store entries. It demonstrates **CI/CD deployment** to **AWS EC2** using **GitHub Actions**.

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
<img width="1920" height="1080" alt="Screenshot 2025-09-03 181134" src="https://github.com/user-attachments/assets/21fb1d2e-70f5-4f7d-b834-a76a2d7f7b9b" />
<img width="1920" height="1080" alt="Screenshot 2025-09-03 181247" src="https://github.com/user-attachments/assets/08b3e841-eeef-49e5-8494-0572168dbdab" />
<img width="1920" height="1080" alt="Screenshot 2025-09-03 181333" src="https://github.com/user-attachments/assets/3acdcc95-ca2b-4e97-8b37-57b8a403cb3c" />


### With Nginx reverse proxy configured
```
http://3.91.8.117

```
<img width="1920" height="1080" alt="Screenshot 2025-09-03 182037" src="https://github.com/user-attachments/assets/2d896e46-9476-4d9b-a1c5-4283cc42d17c" />

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
### deploy.yml
```
http://3.91.8.117
```
```
name: Deploy to EC2

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Copy files to EC2
        uses: appleboy/scp-action@v0.1.7
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ubuntu
          key: ${{ secrets.EC2_SSH_KEY }}
          source: "."
          target: "~/flask-user-form"

      - name: Deploy on EC2
        uses: appleboy/ssh-action@v0.1.10
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ubuntu
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            set -e
            cd ~/flask-user-form

            echo " Updating packages"
            sudo apt-get update -y
            sudo apt-get install -y python3-venv python3-pip

            echo "Setting up virtual environment"
            if [ ! -d "venv" ]; then
              python3 -m venv venv
            fi
            source venv/bin/activate

            echo "Upgrading pip"
            pip install --upgrade pip setuptools wheel

            echo "Installing dependencies"
            pip install -r requirements.txt

            echo "Restarting Flask app"
            sudo systemctl daemon-reload
            sudo systemctl restart flask-app
            sudo systemctl enable flask-app
```
<img width="1920" height="1080" alt="Screenshot 2025-09-03 192941" src="https://github.com/user-attachments/assets/492ce3c3-81e6-4e97-9575-34017f84056f" />
