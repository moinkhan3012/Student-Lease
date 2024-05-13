# Flask Server Deployment on EC2
## Prerequisites

- An AWS account
- Basic knowledge of Linux commands
- SSH access to your EC2 instance

## 1. Setting Up Your EC2 Instance

### Launch the Instance

1. Log in to your AWS Management Console and go to the EC2 Dashboard.
2. Click **Launch Instances**.
3. Select an Amazon Machine Image (AMI), such as Ubuntu Server 20.04 LTS.
4. Choose an instance type, e.g., `t2.medium`.
5. Configure the instance details, storage, and tags as needed.
6. Set up a security group to allow traffic on port 80 (HTTP), port 22 (SSH) and port 8000 for flask server .
7. Launch the instance with a key pair.

### Connect to Your Instance

- Connect using SSH:
  ```bash
  ssh -i /path/to/your-key.pem ubuntu@your-instance-public-dns
  ```

## 2. Installing Dependencies

### System Updates and Package Installation

```bash
sudo apt-get update
sudo apt-get install python3-pip python3-dev nginx git -y
```

### Virtual Environment Setup

```bash
sudo pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```

## 3. Deploy Your Flask Application

### Clone Your Repository

```bash
git clone https://yourrepository.com/flask-server.git
cd flask-server
```

### Install Python Packages

Ensure you have a `requirements.txt` file in your project directory with all necessary packages listed.

```bash
pip install -r requirements.txt
```


### Configuration Files

Ensure your `.env` file and other necessary configuration files are set correctly.

- **Example `.env` file**:
  ```plaintext
    ES_HOST=https://your_elasticsearch_host
    ES_CA_CERT="path_to_your_elasticsearch_certificate"
    ES_USERNAME=your_elasticsearch_username
    ES_PASSWORD="your_elasticsearch_password"
    ES_INDEX=your_elasticsearch_index
    BUCKET_NAME="your_s3_bucket_name"
    BUCKET_KEY="your_s3_bucket_key"
    AWS_ACCESS_KEY="your_aws_access_key"
    AWS_SECRET_KEY="your_aws_secret_key"
  ```
- `BUCKET_NAME` contains your `pipeline.pkl` file on the S3 bucket, and `BUCKET_KEY` holds the path to the `pipeline.pkl` in S3 bucket.
## 4. Set Up Gunicorn

Create a Gunicorn systemd service file to keep your app running.

```bash
sudo nano /etc/systemd/system/flaskserver.service
```

- Paste the Gunicorn configuration into the file, save, and exit.
```
[Unit]
Description=Gunicorn instance for a Flask Server app
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/flask-server
ExecStart=/home/ubuntu/flask-server/venv/bin/gunicorn -b localhost:8000 app:app
Restart=always
[Install]
WantedBy=multi-user.target
```

### Start and Enable the Gunicorn Service

```bash
sudo systemctl start flaskserver
sudo systemctl enable flaskserver
```

## 5. Configure Nginx as a Reverse Proxy

- Replace `your_server_ip_or_domain` in the Nginx config with your EC2 instance's IP or domain.

```bash
sudo nano /etc/nginx/sites-available/default
```

- Paste the Nginx configuration into the file, save, and close.
```
  server {
    listen 80;
    server_name your_server_ip_or_domain;

    location / {
        proxy_pass http://localhost:5000;  # Forward requests to Gunicorn
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Restart Nginx

```bash
sudo systemctl restart nginx
```

## 6. Verify Deployment

Visit your EC2 instance's public IP address in a web browser:

```
http://your-instance-public-ip
```

Your Flask application should now be running, served through Nginx and Gunicorn.

---
