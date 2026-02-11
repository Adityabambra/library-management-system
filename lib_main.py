import os
import json
from datetime import datetime, timedelta
import sys
import hashlib

class library:
    def __init__(self):
        print(" ***** WELCOME TO THE LIBRARY ***** ")

        base_path = os.path.join(os.path.expanduser("~"), "Desktop")
        folder_name = "library_data"   # avoid dot
        folder_path = os.path.join(base_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)


        self.user_details = os.path.join(folder_path, "user_data.json")
        self.books_data = os.path.join(folder_path, "books_data.json")

        initial_books = [
            "python", "sql", "numpy", "pandas", "java",
            "c++", "c", "javascript", "html", "css",
            "django", "flask", "react", "angular", "nodejs",
            "ruby", "php", "swift", "kotlin", "go"
        ]
        initial_books = [book.title() for book in initial_books]

        if not os.path.exists(self.books_data):
            b_data = {
                "books": initial_books,
                "borrowed": {},  # { "Book Name": {"borrower": key, "return_date": "dd-mm-YYYY"} }
                "ammount_collected": 0
            }
            with open(self.books_data, "w") as f:
                json.dump(b_data, f, indent=4)

        with open(self.books_data, "r") as f:
            data = json.load(f)
            self.books = sorted(data.get("books", []))
            self.b_avail = data.get("borrowed", {})  
            self.ammount = data.get("ammount_collected", 0)

        if not os.path.exists(self.user_details):
            u_data = {
                "user": [],
                "history": {},
                "donar": {}
            }
            with open(self.user_details, "w") as u:
                json.dump(u_data, u, indent=4)

        with open(self.user_details, "r") as u:
            u_data = json.load(u)
            self.users = u_data.get("user", [])
            self.history = u_data.get("history", {})
            self.donar = u_data.get("donar", {})

        self.name = None
        self.no = None
        self.pin = None
        self.key = None

    def save_udetails(self):
        data = {
            "user": self.users,
            "history": self.history,
            "donar": self.donar
        }
        with open(self.user_details, "w") as f:
            json.dump(data, f, indent=4)

    def save_bdata(self):
        data = {
            "books": sorted(self.books),
            "borrowed": self.b_avail,
            "ammount_collected": self.ammount
        }
        with open(self.books_data, "w") as f:
            json.dump(data, f, indent=4)

    # ---------- Registration ----------
    def create_id(self):
        print("  REGISTRATION FEES : ₹ 200 ")
        name = input("Enter your name : ").title()

        try:
            no = int(input("Enter your mobile number : "))
            aadhar = int(input("Enter your aadhar card number : "))
        except ValueError:
            print("Invalid mobile or aadhar number format.")
            return

        if len(str(no)) != 10 or len(str(aadhar)) != 12:
            print("Mobile number or Aadhar number is incorrect.")
            return

        for user in self.users:
            if user.get("no") == no or user.get("id") == aadhar:
                print("User with these details already exists.")
                return

        while True:
            upin = input("Create your 4 digit PIN: ")
            if len(upin) != 4 or not upin.isdigit():
                print("Enter PIN of 4 digits (numbers only).")
                continue

            cpin = input("Confirm your PIN : ")
            if cpin != upin:
                print("PINs do not match. Try again.")
                continue


            pin_hash = hashlib.sha256(upin.encode()).hexdigest()
            new_user = {"name": name, "no": no, "id": aadhar, "pin": pin_hash, "fine": 0}
            self.ammount = self.ammount + 200
            self.users.append(new_user)
            self.save_bdata()
            self.save_udetails()
            print("Registration successful!")
            return

    # ---------- Login ----------
    def login(self):
        name = input("Enter your name : ").title()
        try:
            no = int(input("Enter your mobile number : "))
        except ValueError:
            print("Invalid mobile number format.")
            return False

        upin = input("Enter your PIN : ")

        if len(str(no)) != 10 or len(upin) != 4:
            print("Please enter correct PIN or Number")
            return False

        pin_hash = hashlib.sha256(upin.encode()).hexdigest()
        found = False

        for user in self.users:
            if user.get("name") == name and user.get("no") == no and user.get("pin") == pin_hash:
                found = True
                break

        if found:
            print("Login Successful! Redirecting to the main menu...\n")
            self.name = name
            self.no = no
            self.pin = pin_hash
            self.key = f"{name}_{no}"
            return True
        else:
            for user in self.users:
                if user.get("name") == name and user.get("no") == no and user.get("pin") != pin_hash:
                    print("INCORRECT PIN.")
                    return False
            print("No user found with these name and mobile number.")
            return False

    # ---------- Change details ----------
    def change_details(self):
        if not self.name or not self.no:
            print("You must be logged in to change details.")
            return

        print("Select what you want to change ")
        print("1. Name \n2. Mobile no. \n3. Aadhar no. \n4. PIN")

        try:
            change = int(input("Enter your choice : "))
        except ValueError:
            print("Invalid input")
            return

        current_user = None
        for user in self.users:
            if user.get("name") == self.name and user.get("no") == self.no and user.get("pin") == self.pin:
                current_user = user
                break

        if not current_user:
            print("User not found. Make sure you are logged in.")
            return

        # Change name
        if change == 1:
            print("Current name:", self.name)
            new_name = input("Enter your new name : ").title()
            conf_name = input("Enter your new name AGAIN : ").title()
            if new_name == conf_name:
                print(f"Confirm you want to change your name from {self.name} to {new_name}")
                change_name = input("Enter yes/no : ").lower()
                if change_name == "yes":
                    current_user["name"] = new_name
                    # update session name and key
                    self.name = new_name
                    self.key = f"{self.name}_{self.no}"
                    self.save_udetails()
                    print("Name changed.")
                else:
                    print("Name change cancelled.")
            else:
                print("Names did not match.")

        # Change mobile number
        elif change == 2:
            print("Current mobile number:", self.no)
            try:
                new_no = int(input("Enter your new mobile number : "))
                conf_no = int(input("Enter your new mobile number AGAIN : "))
            except ValueError:
                print("Invalid mobile number format.")
                return

            if new_no == conf_no and len(str(new_no)) == 10:
                print(f"Confirm you want to change your mobile number from {self.no} to {new_no}")
                change_no = input("Enter yes/no : ").lower()
                if change_no == "yes":
                    current_user["no"] = new_no
                    self.no = new_no
                    self.key = f"{self.name}_{self.no}"
                    self.save_udetails()
                    print("Mobile number changed.")
                else:
                    print("Mobile change cancelled.")
            else:
                print("Numbers did not match or invalid length.")

        # Change aadhar
        elif change == 3:
            print("Current aadhar number:", current_user.get("id"))
            try:
                new_id = int(input("Enter your new aadhar number : "))
                conf_id = int(input("Enter your new aadhar number AGAIN : "))
            except ValueError:
                print("Invalid aadhar format.")
                return

            if new_id == conf_id and len(str(new_id)) == 12:
                print(f"Confirm you want to change your aadhar number from {current_user.get('id')} to {new_id}")
                confirm = input("Enter yes/no : ").lower()
                if confirm == "yes":
                    current_user["id"] = new_id
                    self.save_udetails()
                    print("Aadhar updated.")
                else:
                    print("Aadhar change cancelled.")
            else:
                print("Aadhar numbers did not match or invalid length.")

        # Change PIN
        elif change == 4:
            try:
                # ask the user to re-enter current id to confirm
                check_id = int(input("Enter your aadhar id to confirm: "))
            except ValueError:
                print("Invalid aadhar format.")
                return

            if check_id != current_user.get("id"):
                print("Aadhar does not match. Cannot change PIN.")
                return

            while True:
                new_pin = input("Enter your new PIN  : ")
                conf_pin = input("Enter your new PIN AGAIN : ")
                if new_pin != conf_pin:
                    print("PINs do not match. Try again.")
                    continue
                if len(new_pin) != 4 or not new_pin.isdigit():
                    print("PIN must be 4 digits.")
                    continue
                new_pin_hash = hashlib.sha256(new_pin.encode()).hexdigest()
                print(f"Confirm you want to change your PIN.")
                confirm = input("Enter yes/no : ").lower()
                if confirm == "yes":
                    current_user["pin"] = new_pin_hash
                    self.save_udetails()
                    print("PIN changed.")
                else:
                    print("PIN change cancelled.")
                break
        else:
            print("Please enter a valid input")
            return

    # ---------- Search ----------
    def search_books(self):
        query = input("Enter book name to search: ").title()
        found = [b for b in self.books if query in b.title()]
        if found:
            print("Books found:")
            for b in found:
                print(f"- {b}")
        else:
            print("No book found with this name.")

    # ---------- Borrow ----------
    def borrow_book(self):
        if not self.name:
            print("You must be logged in to borrow a book.")
            return

        entered = input("Enter your PIN : ")
        entered_hash = hashlib.sha256(entered.encode()).hexdigest()
        if entered_hash != self.pin:
            print("INCORRECT PIN. TRY AGAIN")
            return

        for user in self.users:
            if user.get("name") == self.name and user.get("no") == self.no:
                if user.get("fine", 0) > 100:
                    print(f"You have a fine pending of ₹{user.get('fine')}. Please pay the fine first to issue a book.")
                    return

        borrowed_books = [b for b, v in self.b_avail.items() if v.get("borrower") == self.key]

        if len(borrowed_books) >= 3:
            print("You have already borrowed the maximum number of books. Please return at least one book before borrowing more.")
            return

        book_name = input("Enter the name of the book you want to borrow: ").title()
        if book_name not in self.books:
            print("This book is currently not available.")
            if book_name in self.b_avail:
                due_date_str = self.b_avail[book_name].get("return_date")
                print(f"This book will be available after {due_date_str}")
            return

        try:
            days = int(input("Enter the no of days you want to issue (MAX 15 DAYS): "))
        except ValueError:
            print("Invalid input for days.")
            return

        if days > 15:
            print("Sorry! We cannot issue a book for that many days.")
            return

        issue_date = datetime.now()
        return_date = issue_date + timedelta(days=days)
        return_date_str = return_date.strftime("%d-%m-%Y")

        try:
            self.books.remove(book_name)
        except ValueError:
            print("Book not found in available list; cannot borrow.")
            return

        self.b_avail[book_name] = {"borrower": self.key, "return_date": return_date_str}
        self.history.setdefault(self.key, [])
        self.history[self.key].append({
            "book": book_name,
            "issue_date": issue_date.strftime("%d-%m-%Y"),
            "return_date": return_date_str
        })

        print(f"Book borrowed by {self.name} for {days} days. Return date: {return_date_str}")
        print("NOTE -- There is a penalty of ₹20 for each day after the return date.")

        self.save_bdata()
        self.save_udetails()

    # ---------- Return ----------
    def return_book(self):
        if not self.name:
            print("You must be logged in to return a book.")
            return

        book_name = input("Enter the book name : ").title()
        if book_name not in self.b_avail:
            print("This is not the book you issued or it's not borrowed.")
            return

        entry = self.b_avail.get(book_name)
        if not entry:
            print("This is not the book you issued.")
            return

        borrower = entry.get("borrower")
        due_date_str = entry.get("return_date")

        if borrower != self.key:
            print("This is not the book you issued.")
            return

        try:
            due_date = datetime.strptime(due_date_str, "%d-%m-%Y")
        except Exception:
            print("Stored return date format is invalid.")
            return

        today = datetime.now()

        fine = 0
        if today > due_date:
            days_late = (today - due_date).days
            fine = days_late * 20
            print(f"You are {days_late} days late. A fine of ₹20 per day applies. Total fine for late return: ₹{fine}")
        else:
            print("Book returned on time.")

        for user in self.users:
            if user.get("name") == self.name and user.get("no") == self.no:
                user["fine"] = user.get("fine", 0) + fine

        for record in self.history.get(self.key, []):
            if record.get("book") == book_name:
                record["return_date"] = today.strftime("%d-%m-%Y")
                break


        self.books.append(book_name)

        self.b_avail.pop(book_name, None)

        self.save_bdata()
        self.save_udetails()

    # ---------- Give (donate) ----------
    def give_book(self):
        if not self.name:
            print("You must be logged in to donate a book.")
            return

        book_name = input("Enter the name of the book : ").title()
        self.books.append(book_name)
        print("Book added successfully.")

        today = datetime.now()
        self.donar.setdefault(self.key, [])
        self.donar[self.key].append({
            "Book_name": book_name,
            "Date": today.strftime("%d-%m-%Y")
        })

        self.save_bdata()
        self.save_udetails()

    # ---------- Pay fine ----------
    def pay_fine(self):
        if not self.name:
            print("You must be logged in to pay a fine.")
            return

        for user in self.users:
            if user.get("name") == self.name and user.get("no") == self.no:
                print(f"Your total fine is ₹{user.get('fine', 0)}.")
                status = input("Fine paid ? Yes/No ").lower()
                if status == "yes":
                    self.ammount += user.get('fine', 0)
                    user['fine'] = 0
                    print("Fine cleared. Thank you.")
                else:
                    print("Payment not completed.")
                break
        else:
            print("User record not found.")

        self.save_bdata()
        self.save_udetails()

    # ---------- History ----------
    def show_history(self):
        if not self.key or self.key not in self.history:
            print("No history found !!")
            return
        print(f"Borrow history of {self.key} : ")
        for record in self.history[self.key]:
            print(record)

    # ---------- Show books ----------
    def show_books(self):
        print("\nAvailable Books:")
        for i, book in enumerate(sorted(self.books), start=1):
            print(f"{i}. {book}")

    # ---------- Menu ----------
    def show_menu(self):
        while True:
            print("\n--- MAIN MENU ---")
            print("1. Issue a Book")
            print("2. Return a Book")
            print("3. Give (Donate) a Book")
            print("4. Show Available Books")
            print("5. Search Book by Name")
            print("6. Show My Borrow History")
            print("7. Pay fine")
            print("8. Change Details")
            print("9. Logout")
            print("0. EXIT")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.borrow_book()
            elif choice == "2":
                self.return_book()
            elif choice == "3":
                self.give_book()
            elif choice == "4":
                self.show_books()
            elif choice == "5":
                self.search_books()
            elif choice == "6":
                self.show_history()
            elif choice == "7":
                self.pay_fine()
            elif choice == "8":
                self.change_details()
            elif choice == "9":
                print("Logging out.")
                # clear session
                self.name = None
                self.no = None
                self.pin = None
                self.key = None
                return
            elif choice == "0":
                print("Thank you for visiting. Exiting system.")
                sys.exit(0)
            else:
                print("Invalid choice. Try again.")

# ---------- Program entry ----------
if __name__ == "__main__":
    main = library()
    s = True
    while s:
        start = input("\nLogin / Register / Close : ").strip().lower()
        if start == "register":
            main.create_id()
            continue
        elif start == "login":
            ok = main.login()
            if ok:
                main.show_menu()
            else:
                print("Login failed.")
                continue
        elif start == "close" or start == "exit":
            s = False
            print("SYSTEM CLOSED")
        else:
            print("Type 'login', 'register' or 'close'.")

