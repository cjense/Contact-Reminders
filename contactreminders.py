import csv, sys
from datetime import datetime, timedelta

csvfile = 'contacts.csv'

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
        self.overdue = (datetime.today().date() - self.reachout).days

    def __str__(self):
        if self.nickname and self.type == 'family':
            return f"{self.nickname} is a {self.type} member and should be contacted every {self.frequency} days. Last contacted on {self.lastcontacted} and next contact should be on {self.reachout}. You are {self.overdue} days overdue.\n"
        elif self.nickname and self.type == 'friend':
            return f"{self.nickname} is a {self.type} and should be contacted every {self.frequency} days. Last contacted on {self.lastcontacted} and next contact should be on {self.reachout}. You are {self.overdue} days overdue.\n"
        elif not self.nickname and self.type == 'family':
            return f"{self.fullname} is a {self.type} member and should be contacted every {self.frequency} days. Last contacted on {self.lastcontacted} and next contact should be on {self.reachout}. You are {self.overdue} days overdue.\n"
        elif not self.nickname and self.type == 'friend':
            return f"{self.fullname} is a {self.type} and should be contacted every {self.frequency} days. Last contacted on {self.lastcontacted} and next contact should be on {self.reachout}. You are {self.overdue} days overdue.\n"
        elif self.type == 'network':
            return f"{self.fullname} is in your {self.type} and should be contacted every {self.frequency} days. Last contacted on {self.lastcontacted} and next contact should be on {self.reachout}. You are {self.overdue} days overdue.\n"
        else:
            return f"{self.fullname} is a {self.type} and should be contacted every {self.frequency} days. Last contacted on {self.lastcontacted} and next contact should be on {self.reachout}. You are {self.overdue} days overdue.\n"


def main():
    contacts = readcsv(csvfile)

    if len(sys.argv) > 1 and sys.argv[1] == "update" and len(sys.argv) == 5:
        updatecontact(sys.argv[2], sys.argv[3], sys.argv[4])
    elif len(sys.argv) > 1 and sys.argv[1] == "update" and len(sys.argv) == 4:
        updatecontact(sys.argv[2], sys.argv[3])
    elif len(sys.argv) > 1 and sys.argv[1] == "add":
        addcontact()
    elif len(sys.argv) > 1 and sys.argv[1] == "shortlist":
        shortlist()
    elif len(sys.argv) > 1 and sys.argv[1] == "help":
        help()
    else:
        contactlist()

## Read a CSV file and return a list of Contact objects

def readcsv(csvfile):
    contacts = []

    with open(csvfile, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for contact in reader:
            contacts.append(Contact(contact[0], contact[1], contact[2], contact[3], contact[4], contact[5], contact[6], contact[7]))

    return contacts


## Write a list of Contact objects to a CSV file

def updatecsv(contactlist, csvout):
    with open(csvout, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for contact in contactlist:
            writer.writerow([contact.fullname, contact.firstname, contact.lastname, contact.type, contact.frequency, contact.lastcontacted, contact.reachout, contact.nickname])


## Iterate through contacts, if today's date is greater than or equal to the reachout date, print the contact

def contactlist():
    contacts = readcsv(csvfile)

    for contact in contacts:
        if datetime.today().date() >= contact.reachout:
            print(contact)

## Add a new contact to the CSV file

def addcontact():
    contacts = readcsv(csvfile)

    fullname = input("Enter the full name of the contact: ")
    try:
        fullname = str(fullname)
    except:
        print("Invalid name. Please try again.")
        return

    for contact in contacts:
        if fullname == contact.fullname:
            print("Contact already exists. Please try again.")
            return

    try:
        firstname = fullname.split()[0]
        lastname = fullname.split()[1]
    except:
        print("Invalid name. Please try again.")
        return

    type = input("Enter the type of contact (family, friend, or network): ")
    if type != 'family' and type != 'friend' and type != 'network':
        print("Invalid type. Please try again.")
        return

    frequency = input("Enter the frequency of contact (in days): ")
    try:
        frequency = int(frequency)
    except:
        print("Invalid frequency. Please try again.")
        return
    if frequency > 365:
        print("Invalid frequency. Please try again.")
        return

    lastcontacted = input("Enter the last contacted date (YYYY-MM-DD): ")
    try:
        lastcontacted = datetime.strptime(lastcontacted, "%Y-%m-%d").date()
    except:
        print("Invalid date. Please try again.")
        return

    reachout = lastcontacted + timedelta(days=int(frequency))
    lastcontacted = str(lastcontacted)
    nickname = input("Enter a nickname for the contact (optional): ")

    contacts.append(Contact(fullname, firstname, lastname, type, frequency, lastcontacted, reachout, nickname))
    print("Added contact: " + fullname + ". Next reachout is " + reachout.strftime("%Y-%m-%d") + ".")

    updatecsv(contacts, csvfile)


## Update the lastcontacted date and reachout date for a contact

def updatecontact(firstname, lastname, lastcontacted=datetime.today().date()):
    if type(lastcontacted) == str:
        lastcontacted = datetime.strptime(lastcontacted, "%Y-%m-%d").date()

    if type(firstname) != str or type(lastname) != str:
        print("Invalid name. Please use format firstname lastname")
        return

    contacts = readcsv(csvfile)

    for c in contacts:
        if c.fullname == firstname + " " + lastname:
            c.lastcontacted = lastcontacted
            c.reachout = datetime.today().date() + timedelta(days=c.frequency)
            print("Updated contact: " + c.fullname + ". Next reachout is " + c.reachout.strftime("%Y-%m-%d") + ".")

    updatecsv(contacts, csvfile)

def shortlist():
    contacts = readcsv(csvfile)

    for contact in contacts:
        if datetime.today().date() >= contact.reachout:
            print(contact.fullname + "\n")

def help():
    print("Usage: contacts.py [command] [arguments]\n")
    print("Commands:")
    print("add - add a new contact")
    print("update - update the last contacted date for a contact")
    print("shortlist - print a list of contacts to reach out to")
    print("help - print this help message")
    print("No arguments - print a list of contacts to reach out to\n")

if __name__ == "__main__":
    main()