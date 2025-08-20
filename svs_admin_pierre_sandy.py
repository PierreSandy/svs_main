# ============== Selwyn Vet Services MAIN PROGRAM ==============
# Student Name: Pierre D Sandy 
# Student ID : 
# NOTE: Make sure your two files are in the same folder
# =================================================================================

from svs_data import col_invoices,col_customers,col_treatments,col_services,db_customers,db_treatments,db_services,unique_id,display_formatted_row   # svs_data.py MUST be in the SAME FOLDER as this file!
                    # spb_data.py contains the data
import datetime     # We areusing date times for this assessment, and it is
                    # available in the column_output() fn, so do not delete this line



def add_customer():
    # Add a customer to the db_customers database, use the unique_id to get an id for the customer.
    # Remember to add all required dictionaries.

    pass  # REMOVE this line once yourts have some function code (a function must have one line of code, so this temporary line keeps Python happy so you can run the code)

def add_booking():
    # Add a booking to a customer
    # Remember to validate treatment and service ids
    pass  # REMOVE this line once you have some function code (a function must have one line of code, so this temporary line keeps Python happy so you can run the code)


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
def pay_invoice():
    invoice_id = input("Enter the invoice ID to pay: ")
    
    if invoice_id not in db_customers:
        print("Invalid invoice ID.")
        return
    
    customer = db_customers[invoice_id]
    if "invoice" not in customer or customer["invoice"]["paid"]:
        print("This invoice has already been paid or does not exist.")
        return
    
    # Mark the invoice as paid
    customer["invoice"]["paid"] = True
    print(f"Invoice {invoice_id} has been marked as paid.")
    
    input("\nPress Enter to continue.")

def invoices_to_pay():
    display_list = []
    for invoice in db_customers.keys():
        customer = db_customers[invoice]
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

# Main function to run the program
# This function will display the menu and handle user input

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

