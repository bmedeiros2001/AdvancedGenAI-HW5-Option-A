import sqlite3
import json
from typing import Optional, Dict, Any, List
from fastmcp import FastMCP


DB_FILE = "customer_service.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Create MCP server
mcp = FastMCP(
    name="customer_support",
    host="127.0.0.1",
    port=8001,
)

# Tool 1: get_customer information by ID
@mcp.tool()
def get_customer(customer_id:int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()
    

# Tool 2: list_customers
@mcp.tool()
def list_customers(status: str ="active", limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if status:
            cursor.execute(
                """
                SELECT * FROM customers 
                WHERE status = ? 
                ORDER BY id
                LIMIT ?
                """, 
                (status, limit))
        else:
            raise ValueError("Status must be 'active' or 'disabled'")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

# Tool 3: update_customer
@mcp.tool()
def update_customer(customer_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
    allowed_fields = {"name", "email", "phone", "status"}
    
    # Validate input
    if not data:
        raise ValueError("No fields provided to update")
    
    # Check for unknown fields
    unknown = set(data.keys()) - allowed_fields
    if unknown:
        raise ValueError(f"Unknown fields in data: {sorted(unknown)}")
    
    # Validate status value if provided
    if "status" in data and data["status"] not in {"active", "disabled"}:
        raise ValueError("status must be 'active' or 'disabled'")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if customer exists
        cursor.execute('SELECT id FROM customers WHERE id = ?', (customer_id,))
        if cursor.fetchone() is None:
            raise ValueError(f"Customer {customer_id} does not exist")
        
        # Build dynamic update query (single query for all fields)
        columns = []
        values: List[Any] = []
        for field, value in data.items():
            columns.append(f"{field} = ?")
            values.append(value)
        
        # Add updated_at timestamp
        columns.append("updated_at = CURRENT_TIMESTAMP")
        values.append(customer_id)
        
        sql = f"UPDATE customers SET {', '.join(columns)} WHERE id = ?"
        cursor.execute(sql, values)
        conn.commit()
        
        # Return updated row
        cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        row = cursor.fetchone()
        if row is None:
            raise RuntimeError("Customer vanished after update")
        return dict(row)
    finally:
        conn.close()

# Tool 4: create_ticket
@mcp.tool()
def create_ticket(customer_id: int, issue: str, priority: str = 'medium') -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if customer exists
        cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        if not cursor.fetchone():
            return None
        
        cursor.execute(
            'INSERT INTO tickets (customer_id, issue, priority) VALUES (?, ?, ?)',
            (customer_id, issue, priority)
        )
        conn.commit()
        
        cursor.execute('SELECT * FROM tickets WHERE id = ?', (cursor.lastrowid,))
        return dict(cursor.fetchone())
    finally:
        conn.close()

# Tool 5: get_customer_history
@mcp.tool()
def get_customer_history(customer_id: int) -> List[Dict[str, Any]]:
    """Get all tickets for a customer."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM tickets WHERE customer_id = ?', (customer_id,))
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8001)