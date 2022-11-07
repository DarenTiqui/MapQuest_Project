#GUI that asks user to input Starting Location and Destination. Outputs the route information between the two locations

import tkinter as tk
from typing import Text
import urllib.parse
import requests
import colorama
from colorama import Fore, Style
import json


main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "CiNR7Z5oMO6ZZwaSObxXa7e8ZGUMXDd9"

#GUI
root = tk.Tk()
root.title("MapQuest Route Finder")
root.geometry("600x500")

#Label for Starting Location
label1 = tk.Label(text="Starting Location: ")
label1.grid(row=0, column=0)

#Entry for Starting Location
entry1 = tk.Entry()
entry1.grid(row=0, column=1)

#Label for Destination
label2 = tk.Label(text="Destination: ")
label2.grid(row=1, column=0)

#Entry for Destination
entry2 = tk.Entry()
entry2.grid(row=1, column=1)

#Label for Measurement System
label3 = tk.Label(text="Measurement System[(M)Metric/(I)Imperial]: ")
label3.grid(row=2, column=0)

#Entry for Measurement System
entry3 = tk.Entry()
entry3.grid(row=2, column=1)


#textbox    
text = tk.Text(root, height=20, width=80, highlightcolor = 'blue', highlightbackground='brown', fg='Navy', bg='#FFEFE7')
text.grid(row=5, column=0, columnspan=2)

#Function to get the route information
def get_route():
    
    url = main_api + urllib.parse.urlencode({"key": key, "from": entry1.get(), "to": entry2.get()})
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]
    
    if json_status == 0:
      #display route information on frame
      text.insert(tk.END, "API Status: " + str(json_status) + " = A successful route call.\n")
      text.insert(tk.END, "Directions from " + (entry1.get()) + " to " + (entry2.get()) + "\n")
      text.insert(tk.END, "Estimated Duration: " + (json_data["route"]["formattedTime"]) + "\n")
      if entry3.get().upper() == 'I':
        text.insert(tk.END, "Miles: " + str("{:.2f}".format((json_data["route"]["distance"]))) + "\n")
        #text.insert(tk.END, "Fuel Used (Gal): " + str("{:.2f}".format((json_data["route"]["fuelUsed"]))) + "\n")
      elif entry3.get().upper() == 'M':
        text.insert(tk.END, "Kilometers: " + str("{:.2f}".format((json_data["route"]["distance"])*1.61)) + "\n")
        #text.insert(tk.END, "Fuel Used (Ltr): " + str("{:.2f}".format((json_data["route"]["fuelUsed"])*3.78)) + "\n")
      text.insert(tk.END, "=============================================\n")
      z = json_data["route"]["legs"][0]["maneuvers"]
      for each in z:
        if entry3.get().upper() == 'I':
          text.insert(tk.END, "=============================================\n")
          text.insert(tk.END, "Step " + str(z.index(each)+1) + "\n")
          text.insert(tk.END, "Distance: " + str("{:.2f}".format((each["distance"]))) + " miles\n")
          text.insert(tk.END, "Direction: " + each["narrative"] + "\n")
        elif entry3.get().upper() == 'M':
          text.insert(tk.END, "=============================================\n")
          text.insert(tk.END, "Step " + str(z.index(each)+1) + "\n")
          text.insert(tk.END, "Distance: " + str("{:.2f}".format((each["distance"])*1.61)) + " kilometers\n")
          text.insert(tk.END, "Direction: " + each["narrative"] + "\n")
        if each != z[-1]:
          #Added a feature to display the time it takes before doing Maneuver
          text.insert(tk.END,"Estimated Time before Maneuver: " + (each["formattedTime"] + "\n"))
          #Added a feature to display the direction the user will face after doing Maneuver
          text.insert(tk.END,"Direction after Maneuver: " + (each["directionName"] + "\n"))

    else:
      label4 = tk.Label(text="API Status: " + str(json_status) + " = A failure occured.")
      label4.grid(row=3, column=0)




#Button to get the route information
button1 = tk.Button(text="Get Route", command=get_route)
button1.grid(row=3, column=1)

#button to clear the entries
button2 = tk.Button(text="Clear", command=lambda: entry1.delete(0, 'end') or entry2.delete(0, 'end') or entry3.delete(0, 'end') or text.delete(1.0, 'end'))
button2.grid(row=3, column=0)

root.mainloop()