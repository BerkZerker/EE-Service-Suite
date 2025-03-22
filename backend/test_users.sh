#!/bin/bash
# Test script for Users CRUD API

pip install bcrypt pytest httpx
cd /mnt/c/Users/Sam/Desktop/EE-Service-Suite/backend
pytest -xvs tests/test_users_api.py