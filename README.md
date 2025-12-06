# AdvancedGenAI-HW5-Option-A

## Overview

This project implements a multi-agent customer service system that uses Agent-to-Agent (A2A) communication for coordination and the Model Context Protocol (MCP) for database access. The system consists of three specialized agents that work together to handle customer service requests.

## System Architecture

The system includes three main agents:

- **Router Agent** (port 10022): Orchestrates queries and coordinates between specialist agents
- **Customer Data Agent** (port 10020): Accesses customer database via MCP tools
- **Support Agent** (port 10021): Handles customer support issues and ticket creation

Additionally, an **MCP Server** (port 8001) provides database access tools for customer and ticket management.

## Requirements

- Python 3.10 or higher
- Google API Key (for Gemini models)
- SQLite3

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AdvancedGenAI-HW5-Option-A.git
cd AdvancedGenAI-HW5-Option-A
```

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

Replace `your_google_api_key_here` with your actual Google API key.

### 5. Initialize the Database

Run the database setup script to create and populate the customer service database:

```bash
python setup_database.py
```

This will create `customer_service.db` with sample customers and tickets.

## Running the System

The system requires two components to be running:

### Step 1: Start the MCP Server

In a terminal window, start the MCP server:

```bash
python mcp_server.py
```

The server will start on `http://127.0.0.1:8001/sse`

Keep this terminal window open while running tests.

### Step 2: Run the Jupyter Notebook

In a separate terminal window:

```bash
jupyter notebook final_code.ipynb
```

The notebook will open in your browser. Execute the cells in order:

1. **Cell 1-7**: Setup and configuration
2. **Cell 8-15**: Agent and server definitions
3. **Cell 16-18**: Server startup
4. **Cell 19**: Start the A2A servers in background
5. **Cells 20-25**: Execute individual test scenarios

## Test Scenarios

The system demonstrates five test scenarios:

1. **Simple Query**: Get customer information for ID 5
   - Tests basic MCP tool usage
   
2. **Coordinated Query**: Customer upgrade request
   - Tests multi-agent coordination between Customer Data and Support agents
   
3. **Complex Query**: List active customers with open tickets
   - Tests complex data aggregation across multiple customers
   
4. **Escalation**: Billing dispute with high priority
   - Tests priority detection and ticket creation
   
5. **Multi-Intent**: Update email and show ticket history
   - Tests sequential operations within a single request

## Database Schema

### Customers Table
- id (INTEGER PRIMARY KEY)
- name (TEXT NOT NULL)
- email (TEXT)
- phone (TEXT)
- status (TEXT: 'active' or 'disabled')
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)

### Tickets Table
- id (INTEGER PRIMARY KEY)
- customer_id (INTEGER, foreign key to customers.id)
- issue (TEXT NOT NULL)
- status (TEXT: 'open', 'in_progress', 'resolved')
- priority (TEXT: 'low', 'medium', 'high')
- created_at (TIMESTAMP)

## MCP Tools

The MCP server provides five tools:

1. **get_customer(customer_id)**: Retrieve a single customer by ID
2. **list_customers(status, limit)**: List customers by status
3. **update_customer(customer_id, data)**: Update customer fields
4. **create_ticket(customer_id, issue, priority)**: Create a support ticket
5. **get_customer_history(customer_id)**: Get all tickets for a customer

## Port Configuration

The system uses the following ports:

- 8001: MCP Server (SSE endpoint)
- 10020: Customer Data Agent
- 10021: Support Agent
- 10022: Router Agent

Ensure these ports are available before starting the system.

## Troubleshooting

### Port Already in Use

If you see "Address already in use" errors:

```bash
# On macOS/Linux
lsof -ti:8001 | xargs kill -9
lsof -ti:10020 | xargs kill -9
lsof -ti:10021 | xargs kill -9
lsof -ti:10022 | xargs kill -9

# On Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

Alternatively, uncomment and run Cell 1 in the notebook to clear ports automatically.

### MCP Server Connection Errors

If you see "peer closed connection" errors:

1. Verify the MCP server is running on port 8001
2. Check that the database file exists: `customer_service.db`
3. Restart the MCP server
4. Increase timeout values in the notebook if needed

### Database Not Found

If you see "database not found" errors:

1. Run `python setup_database.py` to create the database
2. Verify `customer_service.db` exists in the project directory

## Project Structure

```
AdvancedGenAI-HW5-Option-A/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create this)
├── .gitignore                   # Git ignore rules
├── setup_database.py            # Database initialization script
├── mcp_server.py               # MCP server implementation
├── final_code.ipynb            # Main implementation notebook
└── customer_service.db         # SQLite database (created by setup)
```

## Technology Stack

- **Agent Framework**: Google ADK (Agent Development Kit)
- **LLM Model**: Gemini 2.5 Flash
- **A2A Protocol**: Agent-to-Agent SDK v0.3.20
- **MCP**: Model Context Protocol with FastMCP
- **Database**: SQLite3
- **Web Framework**: Uvicorn with SSE transport

# Main challenges:
I had a few challenges during this assignment. 
- I first tried building the system with LangGraph, and I truly had a tough time. I thought the SDK system was indeed easier to set up. Nonetheless, it was still challenging. I struggled to workout the two different ways A2A could've been set up. Originally, I attempted to do manual set up, but later on I changed to `to_a2a()`.
- Additionally, I spent way too long debugging why my `AgentCards` weren't working. While the python module uses snake_case, the `AgentCard` parameters need parameters in camelCase.
- I would constantly getthis cryptic error: "Expected response header Content-Type to contain 'text/event-stream', got 'application/json'". My A2A client was trying to stream responses but the server was sending regular JSON. The agents were speaking different protocols. Had to make sure everyone was on the same page about how they're communicating.
