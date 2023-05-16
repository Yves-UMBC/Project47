import mysql.connector
import tkinter as tk
from tkinter import filedialog
import pandas as pd


connection = mysql.connector.connect(host='crime.cttsnysgbtbv.us-east-1.rds.amazonaws.com',
                                     database='crime.db',
                                     user='admin',
                                     password='password')

# implementing the database described in the Crime.SQL file
# This code implements a GUI pop-up of the users filesystem
# the expected result is for the user to pick the crime_data
# excel file from open baltimore.

"""
THERE IS A BUG IN WHICH PANDAS WILL NOT RECOGNIZE THE EXCEL FILE

this can be remedied by copying the excel file to the 
"""

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

Crime_data = pd.read_excel(file_path)
null_data = pd.read_excel(file_path).notnull()

print("Crime data captured")

for i in range(1000):
    use = True
    dateTim = Crime_data.loc[i, "CrimeDateTime"]
    if(dateTim[:4] != "2023"):
        use = False

    ####crimeCode####
    if(null_data.loc[i,"CrimeCode"] == False):
        crimeCode = None
    else:
        crimeCode = Crime_data.loc[i, "CrimeCode"]
    ####location####
    if (null_data.loc[i,"Location"] == False):
        location = None
    else:
        location = Crime_data.loc[i,"Location"]
    ####description####
    if (null_data.loc[i,"Description"] == False):
        description = None
    else:
        description = Crime_data.loc[i, "Description"]
    ####Weapon####
    if (null_data.loc[i, "Weapon"] == False):
        weapon = None
    else:
        weapon = Crime_data.loc[i, "Weapon"]
    ####neighborhood####
    if (null_data.loc[i,"Neighborhood"] == False):
        neighborhood = None
    else:
        neighborhood = Crime_data.loc[i,"Neighborhood"]

    if (null_data.loc[i,"Latitude"] == False):
        use = False;
    else:
        latitude = Crime_data.loc[i,"Latitude"]
        if(int(latitude) == 0):
            use = False

    if (null_data.loc[i,"Longitude"] == False):
        use = False;
    else:
        longitude = Crime_data.loc[i,"Longitude"]
        if(int(longitude) == 0):
            use = False
    if(use):
        insert = """INSERT INTO crime
                              (crimecode, description, dateTime, weapon, location, latitude, longitude, neighborhood) 
                               VALUES 
                              (%s,%s,%s,%s,%s,%s,%s,%s)"""
        cursor = connection.cursor()
        data_tuple = (crimeCode,description,dateTim,weapon,location,float(latitude),float(longitude),neighborhood)
        cursor.execute(insert, data_tuple)
        connection.commit()
        print("inserted")

root.destroy()


# First enter neighborhood data
# First enter neighborhood data
print("New prompt opening")
root = tk.Tk()
root.withdraw()
neighborhood_window = tk.Toplevel(root)
neighborhood_window.withdraw()
file_path = filedialog.askopenfilename()
Neighborhood_data = pd.read_excel(file_path)
neighborhood_window.destroy()  # Close the neighborhood window

# Then enter the HFAI data
hfai_window = tk.Toplevel(root)
hfai_window.withdraw()
file_path = filedialog.askopenfilename()
hfai_data = pd.read_excel(file_path)
hfai_window.destroy()  # Close the HFAI window


for j in range(len(hfai_data)):
    raw_string = (hfai_data.loc[j, "CSA2010"])
    raw_string = raw_string.split('/')
    for n in raw_string:
        neighborhood_name = n.strip().lower()
        print(neighborhood_name)
        for i in range(len(Neighborhood_data)):
            reg_neighborhood_name = Neighborhood_data.loc[i, "CSA2010"]
            reg_neighborhood_name = reg_neighborhood_name.split("/")

            for l in reg_neighborhood_name:
                print(neighborhood_name + "  ---  " +l.strip().lower())
                if l.strip().lower() == neighborhood_name:
                    hfai = hfai_data.loc[j, "hfai15"]
                    median_income = Neighborhood_data.loc[i,"mhhi21"]
                    insert = """INSERT INTO neighborhood
                                             (hfai, median_income, name) 
                                              VALUES 
                                             (%s,%s,%s)"""
                    cursor = connection.cursor()
                    data_tuple = (float(hfai), float(median_income), neighborhood_name)
                    cursor.execute(insert, data_tuple)
                    connection.commit()
                    break;




file_path = filedialog.askopenfilename()
















