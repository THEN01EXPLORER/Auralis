#!/bin/bash
echo "Starting Auralis Backend and Frontend..."
cd backend && python -m uvicorn main:app --reload &
cd frontend && npm start
