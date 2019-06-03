# Logs Analysis
The objective of the Logs Analysis Project is to create a reporting tool that prints out reports
based on the data in the database.
This reporting tool use the psycopg2 module to connect to the database.

## How do you run this tool?

### 1. Setup: Configure VM & Database
**Step 1:** Download and install [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org).
We’ll need these tools to setup and manage the Virtual Machine (VM).
I used version 2.2.4 of Vagrant and version 5.2.18 of VirtualBox (please stick with the version mentioned
because I faced issues on newer and older versions).

**Step 2:** Download the VM configuration
from the [Downloads folder](Project1/Downloads). If you faced any problems go to
[Udacity Notes](https://github.com/udacity/fullstack-nanodegree-vm).
The configuration file  specifies the arrangement of resources
(processors, memory, disks, network adapters, etc) assigned to a virtual machine.

**Step 3:**  Download the database dump
from the [downloads folder](Project1/Downloads).
Then, copy the database dump `newsdata.sql` to the `vagrant/` (one of the folders you downloaded in step 2).

**Step 4:**  Download the python scripts from the current folder.
Then, copy them to the `vagrant/`.

**Step 5:** Open the terminal. Then, run the following commands:
```
# Install & Configure VM
cd /path/to/vagrant
vagrant up

# Log into machine
vagrant ssh

# Log into PostgreSQL interactive terminal
cd /vagrant
psql

# Create news database
CREATE DATABASE news;

# Log out of Psql
<Ctrl + D>

# Populate database using dump in shared folder
psql -d news -f newsdata.sql

# Log out of machine
# <Ctrl + D>

# Destroy machine once done
vagrant destroy
```
Note: If this is the first time you're running `vagrant up` command,
you need to wait a while after running the command.

### 2. Views I've used
**Step 1:** Drop if any of them already exists.
```
DROP VIEW IF EXISTS top3_paths;
DROP VIEW IF EXISTS top4_authors;
DROP VIEW IF EXISTS not_ok_req;
DROP VIEW IF EXISTS all_req;
```

**Step 2:** Create the four used views.
```
-- view for the most accessed article paths
CREATE VIEW top3_paths AS
    SELECT SUBSTRING(path, 10) AS log_slug, COUNT(*) AS view_count
        FROM log
        GROUP BY path
        ORDER BY view_count DESC
        LIMIT 3 OFFSET 1;
```

```
-- view for the most popular authors filter them by their articles view count
CREATE VIEW top4_authors AS
    SELECT articles.author, COUNT(log.id) AS view_count
        FROM articles, log
        WHERE SUBSTRING(log.path, 10) = articles.slug
        GROUP BY articles.author
        ORDER BY view_count DESC
        LIMIT 4;
```

```
-- view for grouping failed request per day
CREATE VIEW not_ok_req AS
    SELECT DATE(time) AS day, CAST(COUNT(*) AS FLOAT) AS request_count
        FROM log
        WHERE status != '200 OK'
        GROUP BY day
        ORDER BY request_count DESC;
```

```
-- view for grouping all of the coming requests per day
CREATE VIEW all_req AS
    SELECT DATE(time) AS day, CAST(COUNT(*) AS FLOAT) AS request_count
        FROM log
        GROUP BY day
        ORDER BY request_count DESC;
```

### 3. Run the Reporting Tool
Open the terminal. Then, run the following commands:
```
# Launch & Login to machine
cd /path/to/vagrant
vagrant up
vagrant ssh

# Open shared folder
cd /vagrant

# Run the program
python3 reportingTool.py
```

## Reporting tool will answer the following questions:

**(1) What are the most popular three articles of all time? Which articles have been accessed the most?
Present this information as a sorted list with the most popular article at the top.**
Example:
- "Princess Shellfish Marries Prince Handsome" — 1201 views
- "Baltimore Ravens Defeat Rhode Island Shoggoths" — 915 views
- "Political Scandal Ends In Political Scandal" — 553 views

**(2) Who are the most popular article authors of all time?
That is, when you sum up all of the articles each author has written,
which authors get the most page views? Present this as a sorted list with the most popular author at the top.***
Example:
- Ursula La Multa — 2304 views
- Rudolf von Treppenwitz — 1985 views
- Markoff Chaney — 1723 views
- Anonymous Contributor — 1023 views

**(3) On which days did more than 1% of requests lead to errors? The log table includes
a column status that indicates the HTTP status code that the news site sent to the user's browser.**
Example:
- July 29, 2016 — 2.5% errors
