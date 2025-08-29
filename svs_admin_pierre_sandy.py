# ============== Selwyn Vet Services MAIN PROGRAM ==============
# Student Name: Pierre D Sandy 
# Student ID : 1160455
# NOTE: Make sure your two files are in the same folder
# =================================================================================

from svs_data import col_invoices,col_customers,col_treatments,col_services,db_customers,db_treatments,db_services,unique_id,display_formatted_row   # svs_data.py MUST be in the SAME FOLDER as this file!
                    # spb_data.py contains the data
import datetime     # We areusing date times for this assessment, and it is
                    # available in the column_output() fn, so do not delete this line


# function to display the menu
def disp_menu():
    print("==== WELCOME TO SELWYN VET SERVICES ===")
    print(" 1 - List Customers")
    print(" 2 - List Services")
    print(" 3 - List Treatments")
    print(" 4 - Add Customer")
    print(" 5 - Add Booking")
    print(" 6 - Display Unpaid Invoices")
    print(" 7 - Pay Invoice")
    print(" X - Exit (stops the program)")


# ------------ This is the main program ------------------------

def add_booking():
    # Function to add a booking to a customer
    customer_id = input("Enter Customer ID: ")
    
    # Check if the customer exists
    if customer_id not in db_customers:
        print("Invalid Customer ID.")
        return
    
    # Get the customer's details
    customer = db_customers[customer_id]
    
    # Get treatment and service details
    treatment_id = input("Enter Treatment ID: ")
    service_id = input("Enter Service ID: ")

    # Validate treatment and service IDs
    if treatment_id not in db_treatments or service_id not in db_services:
        print("Invalid Treatment or Service ID.")
        return

    # Create a booking entry
    booking = {
        "treatment": db_treatments[treatment_id],
        "service": db_services[service_id],
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Add booking to the customer's bookings list
    customer["bookings"].append(booking)
    
    print(f"Booking added for Customer ID {customer_id}.")
    input("\nPress Enter to continue.")

def add_customer():
    # Function to add a new customer to the database
    customer_id = unique_id()
    firstname = input("Enter Customer's First Name: ")
    lastname = input("Enter Customer's Last Name: ")
    while True:
        telephone = input("Enter Customer's Telephone Number: ")
        if telephone.isdigit():
            break
        print("Error: please enter a valid phone number")
    email = input("Enter Customer's Email Address: ")

    # Create a new customer entry
    db_customers[customer_id] = {
        "details": [firstname, telephone, email],
        "bookings": [],
        "invoice": None
    }
    
    print(f"Customer {firstname, lastname} has been added with ID {customer_id}.")
    input("\nPress Enter to continue.")


# Function to pay an invoice
def pay_invoice():
    invoice_id = input("Enter the Invoice ID to pay: ")
    
    # Check if the invoice ID exists in the database
    if invoice_id not in db_customers:
        print("Invalid Invoice ID.")
        return
    
    # Check if the invoice exists and is unpaid
    customer = db_customers[invoice_id]
    if "invoice" not in customer or customer["invoice"]["paid"]:
        print("This invoice has already been paid or does not exist.")
        return
    
    # Mark the invoice as paid
    customer["invoice"]["paid"] = True
    print(f"Invoice {invoice_id} has been marked as paid.")
    
    input("\nPress Enter to continue.")

# Function to display unpaid invoices
def invoices_to_pay():

    # Display a list of unpaid invoices
    display_list = []
    for invoice in db_customers.keys():
        customer = db_customers[invoice]

        # Check if the customer has an invoice and if it is unpaid
        if "invoice" not in customer:
            continue    
        try:
            if not customer ["invoice"]["paid"]:
                display_list.append({
                        "id": invoice,
                        "name": customer["details"][0],
                        "amount": customer["invoice"]["amount"],
                        "due_date": customer["invoice"]["due_date"]                
                    })
        # Handle case where invoice data might be missing
        except KeyError:
            print(f"Invalid invoice data for {invoice} ")

    format_columns = "{: >4} | {: <15} | {: >10} | {: <12}"
    print("\nUnpaid Invoices LIST\n")

    display_formatted_row(list(col_invoices.keys()), format_columns)
    for row in display_list:
        row = (row['id'], row['name'], f"{row['amount']:.2f}", row['due_date'])
        display_formatted_row(row, format_columns)

    if not display_list:
        print("\nNo unpaid invoices available.")
        return
    
    input("\nPress Enter to continue.")


# List Functions for Customers, Services, and Treatments
def list_customers():
    display_list = []
    for customer_id, customer in db_customers.items():
        display_list.append({
            "id": customer_id,
            "name": customer["details"][0],
            "telephone": customer["details"][1],
            "email": customer["details"][2]
        })

    format_columns = "{: >4} | {: <15} | {: <12} | {: ^12}"
    print("\nCustomer LIST\n")
    display_formatted_row(list(col_customers.keys()), format_columns)
    
    for row in display_list:
        row_data = (row['id'], row['name'], row['telephone'], row['email'])
        display_formatted_row(row_data, format_columns)

    input("\nPress Enter to continue.")


def list_services():
    display_list = []
    for service in db_services.keys():
        display_list.append({
                             "id": service,
                             "name":db_services[service][0],
                             "cost":db_services[service][1]})
    format_columns = "{: >4} | {: <15} | {: >10}"
    print("\nService LIST\n")

    display_formatted_row(list(col_services.keys()), format_columns)
    for row in display_list:
        row = (row['id'], row['name'], f"{row['cost']:.2f}")
        display_formatted_row(row, format_columns)

# Check if there are any services to display
    if not db_services:
        print("\nNo services available.")
        return
    
    input("\nPress Enter to continue.")


def list_treatments():
    display_list = []
    for treatment in db_treatments.keys():
        display_list.append({
                             "id": treatment,
                             "name": db_treatments[treatment][0],
                             "cost": db_treatments[treatment][1]})   
    format_columns = "{: >4} | {: <15} | {: >10}"
    print("\nTreatment LIST\n") 

    display_formatted_row(list(col_treatments.keys()), format_columns)
    for row in display_list:
        row = (row['id'], row['name'], f"{row['cost']:.2f}")
        display_formatted_row(row, format_columns)

    
    input("\nPress Enter to continue.") 

# Main function to run the program also this function will display the menu and handle user input

def main():
    disp_menu()
    response = input("Please enter menu choice: ")

    while response != "X" and response != "x": #handle both upper and lower case
        if response == "1":
            list_customers()
        elif response == "2":
            list_services()
        elif response == "3":
            list_treatments()
        elif response == "4":
            add_customer()
        elif response == "5":
            add_booking()
        elif response == "6":
            invoices_to_pay()
        elif response == "7":
            pay_invoice()
        else:
            print("\n***Invalid response, please try again (enter 1-7 or X)")

        print("")
        disp_menu()
        response = input("Please enter menu choice: ")


if __name__ == "__main__":
    main()

