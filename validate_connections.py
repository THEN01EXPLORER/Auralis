#!/usr/bin/env python3
"""
Auralis Connection Validation Script
Tests all connections between frontend and backend components
"""

import sys
import os
import json
import subprocess
import time
from pathlib import Path

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print_success(f"{description}: {filepath}")
        return True
    else:
        print_error(f"{description} not found: {filepath}")
        return False

def check_import_in_file(filepath, import_statement, description):
    """Check if an import statement exists in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if import_statement in content:
                print_success(f"{description}")
                return True
            else:
                print_error(f"{description} - Import not found: {import_statement}")
                return False
    except Exception as e:
        print_error(f"Error reading {filepath}: {e}")
        return False

def check_dependency_in_requirements(dependency, requirements_file='backend/requirements.txt'):
    """Check if a dependency is in requirements.txt"""
    try:
        with open(requirements_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if dependency in content:
                print_success(f"Dependency found: {dependency}")
                return True
            else:
                print_error(f"Missing dependency: {dependency}")
                return False
    except Exception as e:
        print_error(f"Error reading {requirements_file}: {e}")
        return False

def main():
    print_header("AURALIS CONNECTION VALIDATION")
    
    all_checks_passed = True
    
    # Change to project root
    project_root = Path(__file__).parent.absolute()
    os.chdir(project_root)
    print_info(f"Project root: {project_root}")
    
    # ===== Backend Structure Checks =====
    print_header("Backend Structure")
    
    checks = [
        ('backend/main.py', 'Main backend entry point'),
        ('backend/requirements.txt', 'Backend dependencies'),
        ('backend/gunicorn.conf.py', 'Gunicorn configuration'),
        ('backend/Dockerfile', 'Backend Docker configuration'),
        ('backend/app/models/contract.py', 'Pydantic models'),
        ('backend/app/services/analyzer.py', 'Static analyzer'),
        ('backend/app/services/bedrock_analyzer.py', 'AI analyzer'),
        ('backend/app/services/analysis_orchestrator.py', 'Analysis orchestrator'),
        ('backend/app/utils/risk_calculator.py', 'Risk calculator'),
    ]
    
    for filepath, desc in checks:
        if not check_file_exists(filepath, desc):
            all_checks_passed = False
    
    # Check for problematic duplicate
    if os.path.exists('backend/app/main.py'):
        print_error("Duplicate main.py found in backend/app/ - should be removed or renamed")
        all_checks_passed = False
    else:
        print_success("No duplicate main.py in backend/app/")
    
    # ===== Backend Import Checks =====
    print_header("Backend Imports")
    
    import_checks = [
        ('backend/main.py', 'from app.services.analyzer import', 'Analyzer import in main.py'),
        ('backend/main.py', 'from app.services.bedrock_analyzer import', 'Bedrock analyzer import'),
        ('backend/main.py', 'from app.services.analysis_orchestrator import', 'Orchestrator import'),
        ('backend/main.py', 'from app.models.contract import', 'Contract models import'),
        ('backend/lambda_handler.py', 'from main import app', 'Lambda handler import'),
    ]
    
    for filepath, import_stmt, desc in import_checks:
        if os.path.exists(filepath):
            if not check_import_in_file(filepath, import_stmt, desc):
                all_checks_passed = False
        else:
            print_warning(f"File not found: {filepath}")
    
    # ===== Dependency Checks =====
    print_header("Python Dependencies")
    
    dependencies = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'boto3',
        'gitpython',
        'gunicorn',
        'slowapi',
        'psutil',
        'mangum',
    ]
    
    for dep in dependencies:
        if not check_dependency_in_requirements(dep):
            all_checks_passed = False
    
    # ===== Frontend Structure Checks =====
    print_header("Frontend Structure")
    
    frontend_checks = [
        ('frontend/src/App.js', 'Main App component'),
        ('frontend/src/index.js', 'React entry point'),
        ('frontend/src/pages/Home.js', 'Home page'),
        ('frontend/src/components/CodeEditor.js', 'Code editor component'),
        ('frontend/src/components/VulnerabilityReport.js', 'Vulnerability report component'),
        ('frontend/src/services/api.js', 'API service'),
        ('frontend/package.json', 'Frontend dependencies'),
        ('frontend/Dockerfile', 'Frontend Docker configuration'),
        ('frontend/nginx.conf', 'Nginx configuration'),
    ]
    
    for filepath, desc in frontend_checks:
        if not check_file_exists(filepath, desc):
            all_checks_passed = False
    
    # ===== Frontend Import Checks =====
    print_header("Frontend Imports")
    
    frontend_import_checks = [
        ('frontend/src/services/api.js', 'import axios', 'Axios import in api.js'),
        ('frontend/src/pages/Home.js', 'import CodeEditor', 'CodeEditor import in Home.js'),
        ('frontend/src/pages/Home.js', 'import VulnerabilityReport', 'VulnerabilityReport import'),
        ('frontend/src/pages/Home.js', 'from \'../services/api\'', 'API service import'),
        ('frontend/src/App.js', 'import Home', 'Home page import'),
    ]
    
    for filepath, import_stmt, desc in frontend_import_checks:
        if os.path.exists(filepath):
            if not check_import_in_file(filepath, import_stmt, desc):
                all_checks_passed = False
    
    # ===== API Endpoint Checks =====
    print_header("API Endpoint Configuration")
    
    # Check frontend API configuration
    if os.path.exists('frontend/src/services/api.js'):
        with open('frontend/src/services/api.js', 'r') as f:
            content = f.read()
            if 'process.env.REACT_APP_API_URL' in content:
                print_success("Frontend uses REACT_APP_API_URL environment variable")
            if '/api/v1/analyze' in content:
                print_success("Frontend calls /api/v1/analyze endpoint")
            if '/api/v1/analyze_repo' in content:
                print_success("Frontend calls /api/v1/analyze_repo endpoint")
    
    # Check backend endpoints
    if os.path.exists('backend/main.py'):
        with open('backend/main.py', 'r') as f:
            content = f.read()
            if '@app.post("/api/v1/analyze")' in content:
                print_success("Backend has /api/v1/analyze endpoint")
            if '@app.post("/api/v1/analyze_repo")' in content:
                print_success("Backend has /api/v1/analyze_repo endpoint")
            if 'CORSMiddleware' in content:
                print_success("Backend has CORS middleware configured")
    
    # ===== Docker Configuration Checks =====
    print_header("Docker Configuration")
    
    if check_file_exists('docker-compose.yml', 'Docker Compose file'):
        with open('docker-compose.yml', 'r') as f:
            content = f.read()
            if 'backend:' in content and 'frontend:' in content:
                print_success("Docker Compose defines both backend and frontend services")
            if 'depends_on:' in content:
                print_success("Frontend service depends on backend")
            if 'REACT_APP_API_URL' in content:
                print_success("Frontend API URL configured in docker-compose")
    
    # ===== Environment Files Check =====
    print_header("Environment Configuration")
    
    env_files = [
        'frontend/.env',
        'backend/.env.example',
    ]
    
    for env_file in env_files:
        if os.path.exists(env_file):
            print_success(f"Found: {env_file}")
        else:
            print_warning(f"Optional file missing: {env_file}")
    
    # ===== Final Summary =====
    print_header("Validation Summary")
    
    if all_checks_passed:
        print_success("All critical checks passed! ✨")
        print_info("Your Auralis application is properly connected and ready to run.")
        print_info("\nTo start the application:")
        print_info("  docker-compose up")
        print_info("  OR")
        print_info("  cd backend && python -m uvicorn main:app --reload")
        print_info("  cd frontend && npm start")
        return 0
    else:
        print_error("Some checks failed. Please review the errors above.")
        print_info("See CONNECTIONS_VERIFIED.md for detailed connection documentation.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
