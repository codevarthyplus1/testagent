#!/bin/bash
# Start the Shopping Cart Web Application

echo "======================================================================"
echo "Shopping Cart Customer Service - Web Application"
echo "======================================================================"
echo ""

# Check if database exists
if [ ! -f "shopping_cart.db" ]; then
    echo "Database not found. Initializing database..."
    python3 init_database.py
    echo ""
fi

echo "Starting web server..."
echo "Open your browser to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 web_app.py
