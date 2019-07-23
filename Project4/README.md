# Linux Server Configuration Project

## About the project
> A baseline installation of a Linux distribution on a virtual machine and prepare it to host web applications, to include installing updates, securing it from a number of attack vectors and installing/configuring web and database servers

* IP Address: [```35.159.25.27```]
* SSH Port: [default: 22]
* Host App URL: [```http://35.159.25.27```](http://35.159.25.27)


## Objectives
This project's objective is to set up a web application server—built from a baseline Linux installation—secured against a number of attack vectors and configured to serve the Item Catalog Application.

## Requirements
1. A Web Browser such as Chrome or Firefox is installed.
2. Access to a command line terminal such as bash or an SSH client such as PuTTY to remotely connect to the server.


## Usage
SSH into the Linux server as 'grader' user using the provided key.
```ssh grader@35.159.25.27 -i ~/.ssh/provided_grader_key```
Enter passphrase for provided_grader_key (Both the key and the passphrase are included in the "Notes to Reviewer" field).
The application is auto-served using supervisor package. Just go to ```http://35.159.25.27```


## Server Configuration
### 1. Create an instance in AWS Lightsail 
Go to AWS Lightsail and create a new account / sign in with your account.
Click Create instance and choose Linux/Unix, OS only Ubuntu 18.04LTS
Choose a payment plan (the cheapest plan is enough for now and it's free for first month)
Click Create button to create the instance.

### 2. Set up the AWS SSH key
Go to `account` page from your AWS account. You will find your SSH key there.
Download your SSH key, the file name will be like `LightsailDefaultPrivateKey-*.pem`
Navigate to the directory where your file is stored in your terminal.
Run `chmod 600 LightsailDefaultPrivateKey-*.pem` to restrict the file permission. 
Change name to `lightsail_key.rsa`.
Run a command `ssh -i lightsail_key.rsa ubuntu@35.159.25.27` in your terminal.

### 3. Update all packages
```sudo apt-get update```
```sudo apt-get upgrade```
```sudo apt-get dist-upgrade```
###### Enable automatic security updates
```sudo apt-get install unattended-upgrades```
```sudo dpkg-reconfigure --priority=low unattended-upgrades```

### 4. Change timezone to UTC and Fix language issues
```sudo timedatectl set-timezone UTC```
```sudo update-locale LANG=en_US.utf8 LANGUAGE=en_US.utf8 LC_ALL=en_US.utf8```

### 5. Create a new user grader and Give him sudo access
```sudo adduser grader```
```sudo nano /etc/sudoers.d/grader```
Then add the following text ```grader ALL=(ALL) ALL``` or run ```adduser grader sudo```

### 6. Setup SSH keys for grader
On your local machine terminal run ```ssh-keygen``` Then choose the path for storing public and private keys
On remote machine home as user ```grader```
```sudo su - grader```
```mkdir .ssh```
```touch .ssh/authorized_keys ```
```sudo chmod 700 .ssh```
```sudo chmod 600 .ssh/authorized_keys```
```nano .ssh/authorized_keys```
Then paste the contents of the public key created on the local machine by running
```sudo scp lightsail_key.rsa grader@35.159.25.27:~/.ssh/authorized_keys``` from your local machine. Now log out of your current session and log in using 
```ssh grader@35.159.25.27 -i ~/.ssh/provided_grader_key```

### 7. Name the server (Optional)
Run ```hostnamectl set-hostname new-server-name```.
Set that new-server-name in the host file by running ```nano /etc/hosts``` under the localhost
list past ```35.159.25.27 new-server-name```

### 8. Disallow Root Logins over SSH
Go to ```sudo nano /etc/ssh/sshd_config``` and change ```PermitRootLogin no``` and
```PasswordAuthentication no```.
After that restart the ssh service by running ```sudo systemctl restart sshd```

### 9. Set up Uncomplicated FireWall (UFW)
Configure UFW to allow only incoming request from (SSH) and (HTTP)
```sudo ufw status -- utf should be inactive```
```sudo ufw default deny incoming -- deny all incoming requests```
```sudo ufw default allow outgoing-- allow all outgoing requests```
```sudo ufw allow ssh -- allow incoming ssh request```
```sudo ufw allow http/tcp -- allow all http request```
```sudo ufw enable -- enable ufw```
```sudo ufw status -- check current status of ufw```
Go to AWS page and set up relevant ports from networking tab.

### 10. Clone or FTP or SCP the itemcatalog project
Copy the project to the server.

### 11. 3rd-Party Packages to be installed
##### 1. ```sudo apt install python3-pip```
##### 2. ```sudo apt install python3-venv```
Activate the python virtual environment by running ```~project_dir$ source venv/bin/activate``` and go on
##### 3. ```pip install -r requirements.txt --pip all of the required packages```
##### 4. Use Nginx and gunicorn to serve the project statically and dynamically
```sudo apt-get install nginx```
```pip install gunicorn```

###### Setting up Nginx and Gunicorn
    1. Running Nginx
    Run ```sudo rm /etc/nginx/sites-enables/default```
    and open ```sudo nano /etc/nginx/sites-enables/choosed-project-name``` and paste
    ```
    server {
        listen 80;
        server_name YOUR_IP_OR_DOMAIN;
    
        location /static {
            alias /home/YOUR_USER/YOUR_PROJECT/flaskblog/static;
        }
    
        location / {
            proxy_pass http://localhost:8000;
            include /etc/nginx/proxy_params;
            proxy_redirect off;
        }
    }
    ```
    after that restart nginx by running ```sudo systemctl restart nginx```
    
    2. Running Gunicorn
    Run ```gunicorn -w <INT:THE_AMOUNT_OF_WORKERS> APP_FILE:APP_VAR_NAME```

##### 5. Use Supervisor
Install it at first ```sudo apt install supervisor``` after that you have to configure supervisor by opening ```sudo nano /etc/supervisor/conf.d/CHOSEN_APP_NAME.conf```
and paste those lines 
```
[program:CHOSEN_APP_NAME]
directory=/home/YOUR_USER/YOUR_PROJECT
command=/home/YOUR_USER/YOUR_PROJECT/venv/bin/gunicorn -w <INT:THE_AMOUNT_OF_WORKERS> APP_FILE:APP_VAR_NAME
user=YOUR_USER
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/CHOSEN_APP_NAME/CHOSEN_APP_NAME.err.log
stdout_logfile=/var/log/CHOSEN_APP_NAME/CHOSEN_APP_NAME.out.log
```
and don't forget to create the last two log files by running 
```sudo mkdir -p /etc/supervisor/conf.d/CHOSEN_APP_NAME --create the directory```
```sudo touch /var/log/CHOSEN_APP_NAME/CHOSEN_APP_NAME.err.log```
```sudo touch /var/log/CHOSEN_APP_NAME/CHOSEN_APP_NAME.out.log```
finally reload the supervisor by running ```sudo supervisorctl reload```




