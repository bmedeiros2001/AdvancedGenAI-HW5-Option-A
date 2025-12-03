import sqlite3
from datetime import datetime, timedelta
import os

# Database filename
DB_FILE = "customer_service.db"

def create_database():

    # delete old database if it exists
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Old database deleted: {DB_FILE}")

    # connect to database (create file if it doesn't exist)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    print(f"New database created: {DB_FILE}")

    # CUSTOMERS TABLE
    cursor.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            email   TEXT,
            phone   TEXT,
            status  TEXT DEFAULT 'active',
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)    
    print("[OK] Customers table created")

    # TICKETS TABLE
    cursor.execute("""
        CREATE TABLE tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            issue TEXT NOT NULL,
            status  TEXT DEFAULT 'open',
            priority TEXT DEFAULT 'medium',
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    """)
    print("[OK] Tickets table created")

    #save changes
    conn.commit()
    return conn, cursor

def add_sample_data(cursor, conn):
    print("Adding sample data to database...")

    # sample customers
    customers = [
        ("Alice Johnson", "alice@email.com", "555-0101", "active"),
        ("Bob Smith", "bob@email.com", "555-0102", "active"),
        ("Charlie Brown", "charlie@email.com", "555-0103", "active"),
        ("Diana Prince", "diana@email.com", "555-0104", "disabled"),
        ("Eve Martinez", "eve@email.com", "555-0105", "active"),
        ("Frank Wilson", "frank@email.com", "555-0106", "active"),
        ("Grace Lee", "grace@email.com", "555-0107", "active"),
        ("Henry Davis", "henry@email.com", "555-0108", "disabled"),
        ("Ivy Chen", "ivy@email.com", "555-0109", "active"),
        ("Jack Thompson", "jack@email.com", "555-0110", "active"),
        ("Karen White", "karen@email.com", "555-0111", "active"),
        ("Leo Garcia", "leo@email.com", "555-0112", "disabled"),
        ("Maria Rodriguez", "maria@email.com", "555-0113", "active"),
        ("Nathan Kim", "nathan@email.com", "555-0114", "active"),
        ("Olivia Taylor", "olivia@email.com", "555-0115", "active"),
    ]

    # Insert customers into the database
    cursor.executemany("INSERT INTO customers (name, email, phone, status) VALUES (?, ?, ?, ?)", customers)
    print(f" Added {len(customers)} customers")

    # Sample tickets
    tickets = [
        # Customer 1 - Alice (multiple issues)
        (1, "Cannot login to my account", "open", "high"),
        (1, "Password reset email not received", "open", "medium"),
        (1, "Two-factor authentication not working", "resolved", "high"),
        
        # Customer 2 - Bob
        (2, "Need help upgrading subscription", "in_progress", "low"),
        (2, "Billing cycle question", "resolved", "low"),
        
        # Customer 3 - Charlie
        (3, "Billing issue - charged twice", "open", "high"),
        (3, "Refund request for duplicate charge", "open", "high"),
        
        # Customer 4 - Diana (disabled account)
        (4, "Feature request: dark mode", "open", "low"),
        (4, "Account reactivation request", "open", "medium"),
        
        # Customer 5 - Eve
        (5, "Password reset not working", "resolved", "medium"),
        
        # Customer 6 - Frank
        (6, "App crashes on startup", "open", "high"),
        (6, "Data sync issue between devices", "in_progress", "medium"),
        
        # Customer 7 - Grace
        (7, "Cannot export reports to PDF", "open", "medium"),
        
        # Customer 8 - Henry (disabled)
        (8, "Account was hacked", "open", "high"),
        
        # Customer 9 - Ivy
        (9, "Integration with Slack not working", "in_progress", "medium"),
        (9, "API rate limit exceeded", "open", "low"),
        
        # Customer 10 - Jack
        (10, "Mobile app notification issues", "open", "low"),
        
        # Customer 11 - Karen
        (11, "Cannot cancel subscription", "open", "high"),
        (11, "Charged after cancellation", "open", "high"),
        
        # Customer 13 - Maria
        (13, "Need invoice for tax purposes", "open", "medium"),
        
        # Customer 14 - Nathan
        (14, "Feature request: calendar integration", "open", "low"),
        
        # Customer 15 - Olivia
        (15, "Slow loading times", "in_progress", "medium"),
        (15, "Search function not returning results", "open", "high"),
    ]

    # Insert tickets into the database
    cursor.executemany("INSERT INTO tickets (customer_id, issue, status, priority) VALUES (?, ?, ?, ?)", tickets)
    print(f" Added {len(tickets)} tickets")

    #save changes
    conn.commit()

def verify_database(cursor):
    """ Print database contents to verify it worked """

    print("\n","="*60)
    print("DATABASE CONTENTS")
    print("="*60)

    # show customers
    print("\nCustomers:")
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    for customer in customers:
        print(customer, "\n")
        print(f"  ID {customer[0]}: {customer[1]} ({customer[4]})")

    # show tickets
    print("\nTICKETS:")
    cursor.execute(""" 
        SELECT t.id, c.name, t.issue, t.status, t.priority, t.created_at
        FROM tickets t
        JOIN customers c ON t.customer_id = c.id
    """)
    tickets = cursor.fetchall()

    for ticket in tickets:
        print(f"   Ticket #{ticket[0]} - {ticket[1]}: {ticket[2]} [{ticket[3]} {ticket[4]}]")

    print("\n" + "="*60)

def main():
    """ Main function to set up everything """
    print(" Setting up custmer service database\n")

    # create database
    conn, cursor = create_database()

    # add sample data
    add_sample_data(cursor, conn)

    # verify database
    verify_database(cursor)

    # close connection
    conn.close()
    print("Database setup complete")
    print(f"Database saved as: {DB_FILE}")

if __name__ == "__main__":
    main()