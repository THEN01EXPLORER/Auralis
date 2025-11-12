#!/bin/bash
# Auralis Slither Installation Script
# Ensures reproducible Slither environment for development and CI

set -e

echo "🔧 Installing Slither Analyzer..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Install Slither
pip install slither-analyzer

# Verify installation
if command -v slither &> /dev/null; then
    echo "✅ Slither installed successfully!"
    slither --version
else
    echo "❌ Slither installation failed"
    exit 1
fi

# Install Solidity compiler (solc)
echo "📦 Installing Solidity compiler..."
pip install solc-select

# Install and use a stable Solidity version
solc-select install 0.8.20
solc-select use 0.8.20

echo "✅ Slither environment setup complete!"
echo ""
echo "Usage:"
echo "  slither <contract.sol>"
echo "  slither <contract.sol> --json output.json"
