# QT-interface
### Creating a QT interface for a populated database in Python

# Description:
## The first tab provides a choice: a list of vacancies and directories (dictionaries) in which the data is stored that cannot be changed. 
![image](https://github.com/Rextek7/QT-interface/assets/113045888/f8681287-c6b3-437d-9932-a15ac67cfb48)

### When selecting "list of vacancies" we go to a new tab which contains a list of vacancies and a brief description of each vacancy. 
![image](https://github.com/Rextek7/QT-interface/assets/113045888/ee275ab3-65d3-47de-841a-282660e7e177)

### For each vacancy we can open a new tab that stores more detailed data about the vacancy as well as mini tabs that show the presence of this vacancy in other tables/directories.
![image](https://github.com/Rextek7/QT-interface/assets/113045888/dc4d10cb-b291-4fb6-9ca1-bc57ae59cfd5)

## By selecting "directories" a new tab opens with all directories, description of each item and their id
![image](https://github.com/Rextek7/QT-interface/assets/113045888/bc12f2d9-58e0-474a-b25e-cbb75774ae9a)


# HR_1.mwb
### Database model

# HR_DATABASE.sql
### The file contains the script of the filled database (data randomly generated)

# SQL.txt 
### Several sql queries to the database to check its correctness

# config.txt
### The file contains data that must be updated to connect to the database

# qt_interface.py
### This file contains qt interface code with pymysql library connection
### For the file to work correctly, you need to change QtGui.QIcon(r'C:\Users\Rextek\Desktop\NIPIGAZ\177 nipigaz-logo') to the logo you want to use.
