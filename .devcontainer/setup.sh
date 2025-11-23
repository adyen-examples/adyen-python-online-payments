#!/bin/bash
# Adyen Python Online Payments - Codespaces Setup Script
set -euo pipefail

echo "Setting up Adyen Python Online Payments..."

# Install Python dependencies
echo "Installing Python dependencies..."
source ./setup.sh

echo ""
echo "Setup complete!"
echo ""
echo "Before running the server, set the following environment variables by exporting them in the terminal:"
echo "   - ADYEN_API_KEY"
echo "   - ADYEN_MERCHANT_ACCOUNT"
echo "   - ADYEN_CLIENT_KEY"
echo "   - ADYEN_HMAC_KEY"
echo ""
echo "Then run: ./start.sh"