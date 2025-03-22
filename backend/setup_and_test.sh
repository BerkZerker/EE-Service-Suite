#!/bin/bash
# Setup and test script for Users CRUD API

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up environment for testing...${NC}"

# Check if python/pip is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 is not installed. Please install it first.${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate || source venv/Scripts/activate

# Install requirements
echo -e "${YELLOW}Installing requirements...${NC}"
pip install -r requirements.txt

# Make sure bcrypt is installed (needed for password hashing)
echo -e "${YELLOW}Ensuring bcrypt is installed...${NC}"
pip install bcrypt

# Run migrations
echo -e "${YELLOW}Running database migrations...${NC}"
alembic upgrade head

# Create admin user if it doesn't exist
echo -e "${YELLOW}Creating admin user...${NC}"
python create_admin.py --email=admin@example.com --username=admin --password=adminpassword --full-name="Admin User"

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
pytest -xvs tests/test_users_api.py

# If we got here, tests passed
echo -e "${GREEN}All tests completed successfully!${NC}"
echo -e "${GREEN}You can now start the server with:${NC}"
echo -e "${GREEN}uvicorn main:app --reload${NC}"
echo -e "${GREEN}And access the API documentation at:${NC}"
echo -e "${GREEN}http://localhost:8000/docs${NC}"