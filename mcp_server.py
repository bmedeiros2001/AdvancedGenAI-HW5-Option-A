import sqlite3
import json
from mcp.server.fastmcp import FastMCP

# connect to exisiting database
conn = sqlite3.connect("customer_service.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Create MCP server
mcp = FastMCP(
    name="customer_support"
)

# Tool 1: get_customer
@mcp_tool()
def get_customer(customer_id):
    cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    row = cursor.fetchone()
    return dict(row) if row else None

# Tool 2: list_customers
@mcp.tool()
def list_customers(status=None, limit=10):
    if status:
        cursor.execute('SELECT * FROM customers WHERE status = ? LIMIT ?', (status, limit))
    else:
        cursor.execute('SELECT * FROM customers LIMIT ?', (limit,))
    return [dict(row) for row in cursor.fetchall()]

# Tool 3: update_customer
@mcp.tool()
def update_customer(customer_id, data):
    if not get_customer(customer_id):
        return False
    for key, value in data.items():
        if key in ['name', 'email', 'phone', 'status']:
            cursor.execute(f'UPDATE customers SET {key} = ? WHERE id = ?', (value, customer_id))
    conn.commit()
    return True

# Tool 4: create_ticket
@mcp.tool()
def create_ticket(customer_id, issue, priority='medium'):
    if not get_customer(customer_id):
        return None
    cursor.execute('INSERT INTO tickets (customer_id, issue, priority) VALUES (?, ?, ?)',
                   (customer_id, issue, priority))
    conn.commit()
    cursor.execute('SELECT * FROM tickets WHERE id = ?', (cursor.lastrowid,))
    return dict(cursor.fetchone())

# Tool 5: get_customer_history
@mcp.tool()
def get_customer_history(customer_id):
    cursor.execute('SELECT * FROM tickets WHERE customer_id = ?', (customer_id,))
    return [dict(row) for row in cursor.fetchall()]

if __name__ == "__main__":
    mcp.run(host="127.0.0.1", port=8001)