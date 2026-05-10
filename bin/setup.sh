#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Starting local environment setup...${NC}"

# 1. Install mkcert if not present
if ! command -v mkcert &> /dev/null; then
    echo -e "${YELLOW}mkcert not found. Installing...${NC}"
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y libnss3-tools curl
        # Install mkcert using pre-built binary
        curl -JLO "https://dl.filippo.io/mkcert/latest?for=linux/amd64"
        chmod +x mkcert-v*-linux-amd64
        sudo cp mkcert-v*-linux-amd64 /usr/local/bin/mkcert
        rm mkcert-v*-linux-amd64
    else
        echo "Please install mkcert manually for your OS: https://github.com/FiloSottile/mkcert"
        exit 1
    fi
else
    echo -e "${GREEN}mkcert is already installed.${NC}"
fi

# 2. Setup mkcert CA
echo -e "${GREEN}Installing local CA...${NC}"
mkcert -install

# 3. Generate certificates for e_squirell.home
CERTS_DIR="$HOME/e_squirell_certs"
if [ ! -d "$CERTS_DIR" ]; then
    echo -e "${YELLOW}Creating certificates directory at $CERTS_DIR...${NC}"
    mkdir -p "$CERTS_DIR"
fi

echo -e "${GREEN}Generating SSL certificates...${NC}"
cd "$CERTS_DIR"
mkcert -cert-file cert.pem -key-file key.pem "e_squirell.home" "localhost" "127.0.0.1" "::1"
cd - > /dev/null

# 4. Update /etc/hosts
HOST_ENTRY="127.0.0.1 e_squirell.home"
if grep -q "e_squirell.home" /etc/hosts; then
    echo -e "${GREEN}e_squirell.home is already in /etc/hosts.${NC}"
else
    echo -e "${YELLOW}Adding e_squirell.home to /etc/hosts (requires sudo)...${NC}"
    echo "$HOST_ENTRY" | sudo tee -a /etc/hosts > /dev/null
    echo -e "${GREEN}Host entry added.${NC}"
fi

echo -e "${GREEN}Setup complete! You can now run 'make dev'.${NC}"
