# Sudoku-schoolProject
It is a 12 class practical project.It is sudoku game made in python.


# MYSQL
Got it! Let’s make this super clear and beginner-friendly. I’ll break it down step by step:

---

## **1️⃣ Install MySQL**

* **Windows/Mac:** Download MySQL from [official site](https://dev.mysql.com/downloads/installer/).
* **Linux (Ubuntu):**

```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

* After installation, check MySQL is running:

```bash
sudo systemctl status mysql
```

---

## **2️⃣ Create a database**

Log into MySQL:

```bash
mysql -u root -p
```

Enter your password.

Create a database for your project:

```sql
CREATE DATABASE rail_ticket;
USE rail_ticket;
```

---

## **3️⃣ Import the SQL dump**

If you have the `railway_dummy.sql` file:

* Open terminal in the folder with the file and run:

```bash
mysql -u root -p rail_ticket < railway_dummy.sql
```

* This will create **stations**, **trains**, and **schedule** tables with data.

Check if data is there:

```sql
USE rail_ticket;
SHOW TABLES;
SELECT * FROM stations LIMIT 5;
```

---

## **4️⃣ Connect MySQL to Python**

You need the `mysql-connector-python` package:

```bash
pip install mysql-connector-python
```

Python example to connect and fetch data:

```python
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="rail_ticket"
)

cursor = conn.cursor()

# Example: fetch first 5 stations
cursor.execute("SELECT * FROM stations LIMIT 5;")
for row in cursor.fetchall():
    print(row)

# Close connection
cursor.close()
conn.close()
```

---

## **5️⃣ Querying for trains and schedule**

Example: find all stations for a train:

```python
train_id = 1
cursor.execute("""
    SELECT s.name, sch.arrival_time, sch.departure_time
    FROM schedule sch
    JOIN stations s ON s.id = sch.station_id
    WHERE sch.train_id = %s
    ORDER BY sch.arrival_time
""", (train_id,))

for row in cursor.fetchall():
    print(row)
```

---

💡 **Tip for beginners:**

* Tables: `stations`, `trains`, `schedule`
* Relationships: `schedule` has foreign keys to `trains` and `stations`
* Use JOINs to combine tables

---

If you want, I can **replace the dummy data with real Indian Railway station codes and real-ish train routes** so your project feels realistic.

Do you want me to do that?
