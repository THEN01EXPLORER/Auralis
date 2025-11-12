#!/bin/bash
# Auralis Quick Start Script
# Automatically sets up the entire MVP environment

set -e

echo "🛡️  Auralis MVP Quick Start"
echo "=============================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+"
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm not found. Please install npm"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Backend setup
echo "📦 Setting up backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -q -r requirements.txt

echo "✅ Backend setup complete"
echo ""

# Optional: Install Slither
read -p "Install Slither for static analysis? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing Slither..."
    bash ../tools/install_slither.sh
    echo "✅ Slither installed"
fi
echo ""

# Start backend in background
echo "Starting backend server..."
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend is running at http://localhost:8000"
else
    echo "❌ Backend failed to start"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

cd ..
echo ""

# VS Code extension setup
echo "📦 Setting up VS Code extension..."
cd vscode-extension

echo "Installing npm dependencies..."
npm install

echo "Compiling TypeScript..."
npm run compile

echo "Packaging extension..."
npm run package

echo "✅ VS Code extension packaged: auralis-vscode-0.1.0.vsix"
cd ..
echo ""

# Summary
echo "=============================="
echo "🎉 Setup Complete!"
echo "=============================="
echo ""
echo "Next steps:"
echo ""
echo "1. Install VS Code extension:"
echo "   - Open VS Code"
echo "   - Extensions → ... → Install from VSIX"
echo "   - Select: vscode-extension/auralis-vscode-0.1.0.vsix"
echo ""
echo "2. Configure VS Code settings:"
echo "   {"
echo "     \"auralis.apiEndpoint\": \"http://localhost:8000\","
echo "     \"auralis.enableRealTimeAnalysis\": true"
echo "   }"
echo ""
echo "3. Test the extension:"
echo "   - Open a .sol file"
echo "   - Save to trigger analysis"
echo "   - View results in Problems panel"
echo ""
echo "4. Backend is running at: http://localhost:8000"
echo "   - Health check: http://localhost:8000/health"
echo "   - API docs: http://localhost:8000/docs"
echo ""
echo "5. To stop backend:"
echo "   kill $BACKEND_PID"
echo ""
echo "📖 Read MVP_README.md for detailed usage instructions"
echo "🎬 Read DEMO_INSTRUCTIONS.md for demo setup"
echo ""
echo "Happy auditing! 🛡️"
