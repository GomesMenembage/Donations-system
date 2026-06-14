#!/usr/bin/env bash
set -euo pipefail

echo "Creating virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Copy .env.example to .env and edit with your settings"
echo "  2. For production, set DATABASE_URL to a PostgreSQL connection string"
echo "  3. Run: ./scripts/start.sh"
echo ""
echo "  Development: ./scripts/start.sh"
echo "  Production:  ENVIRONMENT=production ./scripts/start.sh"
