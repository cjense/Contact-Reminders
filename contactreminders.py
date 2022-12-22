import csv
from datetime import datetime, timedelta

class Contact:
    def __init__(self, fullname, firstname, lastname, type, frequency, lastcontacted, reachout, nickname=''):
        self.fullname = fullname
        self.firstname = firstname
        self.lastname = lastname
        self.nickname = nickname
        self.type = type
        self.frequency = int(frequency)
        self.lastcontacted = datetime.strptime(lastcontacted, "%Y-%m-%d").date()
        self.reachout = self.lastcontacted + timedelta(days=self.frequency)

    def __str__(self):
        if self.nickname and self.type == 'family':
            return f"{self.nickname} is a {self.type} member and should be contacted every {self.frequency} days. Last contacted on {self.lastcontacted} and next contact should be on {self.reachout}."
        elif self.nickname and self.type == 'friend':
            return f"{self.nickname} is a {self.type} and should be contacted every {self.frequency} days. Last contacted on {self.lastcontacted} and next contact should be on {self.reachout}."
        elif not self.nickname and self.type == 'family':
            return f"{self.fullname} is a {self.type} member and should be contacted every {self.frequency} days. Last contacted on {self.lastcontacted} and next contact should be on {self.reachout}."
        elif not self.nickname and self.type == 'friend':
            return f"{self.fullname} is a {self.type} and should be contacted every {self.frequency} days. Last contacted on {self.lastcontacted} and next contact should be on {self.reachout}."
        elif self.type == 'network':
            return f"{self.fullname} is in your {self.type} and should be contacted every {self.frequency} days. Last contacted on {self.lastcontacted} and next contact should be on {self.reachout}."
        else:
            return f"{self.fullname} is a {self.type} and should be contacted every {self.frequency} days. Last contacted on {self.lastcontacted} and next contact should be on {self.reachout}."

## Read a CSV file and return a list of Contact objects

def readcsv(csvfile):
    contacts = []

    with open(csvfile, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for contact in reader:
            contacts.append(Contact(contact[0], contact[1], contact[2], contact[3], contact[4], contact[5], contact[6], contact[7]))

    return contacts

## Write a list of Contact objects to a CSV file

def updatecsv(csvin, csvout):
    contacts = readcsv(csvin)

    with open(csvout, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for contact in contacts:
            writer.writerow([contact.fullname, contact.firstname, contact.lastname, contact.type, contact.frequency, contact.lastcontacted, contact.reachout, contact.nickname])

## Iterate through contacts, if today's date is greater than or equal to the reachout date, print the contact
def contactlist():
    contacts = readcsv("contacts.csv")

    for contact in contacts:
        if datetime.today().date() >= contact.reachout:
            print(contact)

contactlist()
# updatecsv("contacts.csv", "contacts.csv")