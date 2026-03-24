#!/usr/bin/env bash
#
# Notion CLI Setup Wizard
# One-command setup for notion-cli
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_banner() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║                                                            ║"
    echo "║              📝 Notion CLI Setup Wizard                    ║"
    echo "║                                                            ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
}

print_step() {
    echo -e "${BLUE}▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if Python is installed
check_python() {
    print_step "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
    else
        print_error "Python 3 is required but not installed"
        echo "   Please install Python 3.10 or higher from https://python.org"
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_step "Checking pip installation..."
    if command -v pip3 &> /dev/null; then
        print_success "pip found"
    else
        print_error "pip is required but not installed"
        echo "   Please install pip: https://pip.pypa.io/en/stable/installation/"
        exit 1
    fi
}

# Check for uv and offer to use it
check_uv() {
    print_step "Checking for uv (optional but recommended)..."
    if command -v uv &> /dev/null; then
        print_success "uv found - will use uv for faster installation"
        USE_UV=true
    else
        print_warning "uv not found (optional)"
        echo "   Consider installing uv for faster package management:"
        echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
        USE_UV=false
    fi
}

# Install notion-cli
install_cli() {
    print_step "Installing notion-cli..."
    
    if [ "$USE_UV" = true ]; then
        uv pip install notion-cli || pip3 install notion-cli
    else
        pip3 install notion-cli
    fi
    
    if command -v notion &> /dev/null; then
        VERSION=$(notion --version 2>/dev/null || echo "installed")
        print_success "notion-cli $VERSION installed successfully"
    else
        print_error "Installation failed"
        exit 1
    fi
}

# Setup authentication
setup_auth() {
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo ""
    print_step "Setting up Notion authentication..."
    echo ""
    echo "To use notion-cli, you need a Notion integration token."
    echo ""
    echo -e "${YELLOW}Quick Setup Guide:${NC}"
    echo "   1. Go to: https://www.notion.so/my-integrations"
    echo "   2. Click 'New integration'"
    echo "   3. Give it a name (e.g., 'Notion CLI')"
    echo "   4. Select your workspace"
    echo "   5. Click 'Submit'"
    echo "   6. Copy the 'Internal Integration Token'"
    echo ""
    echo -e "${BLUE}Press Enter when you're ready to paste your token...${NC}"
    read -r
    
    # Run interactive auth setup
    notion auth setup
}

# Test the connection
test_connection() {
    echo ""
    print_step "Testing connection to Notion..."
    
    if notion auth status --json | grep -q '"authenticated": true'; then
        print_success "Connected to Notion successfully!"
        echo ""
        echo "════════════════════════════════════════════════════════════"
        echo ""
        echo -e "${GREEN}🎉 Setup complete!${NC}"
        echo ""
        echo "Quick start:"
        echo "   notion search 'my page'        # Search your workspace"
        echo "   notion auth status             # Check authentication"
        echo "   notion --help                # See all commands"
        echo ""
        echo "For more help: https://github.com/chen-gdp/notion-cli"
        echo ""
    else
        print_error "Connection failed"
        echo "   Please check your token and try: notion auth setup"
        exit 1
    fi
}

# Offer to install OpenCode skill
offer_opencode_skill() {
    echo ""
    print_step "OpenCode Integration (Optional)"
    echo ""
    echo "Would you like to install the notion-cli skill for OpenCode?"
    echo "This allows OpenCode AI agents to use notion-cli commands."
    echo ""
    echo -n "Install OpenCode skill? [y/N]: "
    read -r response
    
    if [[ "$response" =~ ^[Yy]$ ]]; then
        if [ -d "$HOME/.config/opencode" ]; then
            mkdir -p "$HOME/.config/opencode/skills"
            git clone https://github.com/chen-gdp/notion-cli.git "$HOME/.config/opencode/skills/notion-cli" 2>/dev/null || {
                print_warning "Skill already installed or git not available"
            }
            print_success "OpenCode skill installed!"
            echo "   Restart OpenCode to use: 'notion search ...'"
        else
            print_warning "OpenCode not detected"
            echo "   Install OpenCode first: https://opencode.ai"
        fi
    fi
}

# Main setup flow
main() {
    print_banner
    
    echo "This wizard will:"
    echo "   1. Check prerequisites (Python, pip)"
    echo "   2. Install notion-cli"
    echo "   3. Set up Notion authentication"
    echo "   4. Test the connection"
    echo ""
    echo -n "Continue? [Y/n]: "
    read -r response
    
    if [[ "$response" =~ ^[Nn]$ ]]; then
        echo "Setup cancelled."
        exit 0
    fi
    
    check_python
    check_pip
    check_uv
    install_cli
    setup_auth
    test_connection
    offer_opencode_skill
}

# Run main function
main