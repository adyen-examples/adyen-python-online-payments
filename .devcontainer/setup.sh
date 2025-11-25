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
echo "   - ADYEN_API_KEY          (https://docs.adyen.com/user-management/how-to-get-the-api-key)"
echo "   - ADYEN_CLIENT_KEY       (https://docs.adyen.com/user-management/client-side-authentication)"
echo "   - ADYEN_MERCHANT_ACCOUNT       (https://docs.adyen.com/account/account-structure)"
echo "   - ADYEN_HMAC_KEY         (https://docs.adyen.com/development-resources/webhooks/verify-hmac-signatures)"
echo ""
echo "Then run: ./start.sh"
