# viki - Server Configuration Management Tool

## Project Overview

**viki** is a Python CLI application that manages servers using declarative configuration files and state management. It provides an idempotent, Terraform-like workflow for server configuration management via SSH, using YAML configuration files and JSON state files.

### Key Features
- Declarative server configuration management
- Idempotent operations with state tracking
- SSH-based remote execution with sudo support
- Terraform-like workflow: `fetch` → `plan` → `apply`
- Environment variable integration for sensitive data
- Modular command system with easy extensibility

### Project Structure
```
viki/
├── README.md
├── .gitignore
├── app/
│   ├── viki.py                 # Main CLI application
│   ├── Makefile               # Build automation
│   ├── Pipfile                # Python dependencies
│   ├── Pipfile.lock           # Locked dependencies
│   └── common/
│       ├── __init__.py
│       ├── cli.py             # Command-line interface
│       ├── cli_request.py     # Configuration & state management
│       ├── logger.py          # Logging utilities
│       ├── my_ssh.py          # SSH connection handling
│       ├── fetch_response.py  # Data fetching operations
│       ├── plan_response.py   # Change planning
│       ├── apply_response.py  # Change application
│       ├── base_response.py   # Base response class
│       └── ssh_command.py     # SSH command execution
└── ../viki.wiki/              # Documentation wiki
```

## Development Setup

### Prerequisites
- Python 3.11.9
- pipenv (for dependency management)
- SSH access to target servers
- Visual Studio Code (recommended)

### Installation
```bash
cd app/
make install_new
```

This installs:
- `paramiko==3.4.0` (SSH client)
- `pyyaml==6.0.1` (YAML parsing)
- `pytest==8.2.2` (testing framework, dev dependency)

### Environment Setup
1. Enter the pipenv shell:
```bash
cd app/
pipenv shell
```

2. Set required environment variables:
```bash
export VK_VAR_hostname="your-server-ip"
export VK_VAR_username="your-username"
export VK_VAR_password="your-password"
export VK_VAR_sudopassword="your-sudo-password"  # or empty for passwordless sudo
```

## Core Commands

### Available Commands
- **`fetch`**: Retrieve current state from server and update state file
- **`plan`**: Compare configuration with current state and show planned changes
- **`apply`**: Execute planned changes on the server

### Basic Usage
```bash
# Fetch current server state
make fetch DIR=/path/to/config

# Plan changes
make plan DIR=/path/to/config

# Apply changes (with approval prompt)
make apply DIR=/path/to/config
```

### Direct Usage
```bash
python viki.py -p /path/to/config fetch
python viki.py -p /path/to/config plan
python viki.py -p /path/to/config apply
```

## Configuration Files

### Configuration Structure
Configuration files use `.vk.yaml` extension and follow this structure:

```yaml
viki:
  vars:
    hostname: "VK_VAR_hostname"
    username: "VK_VAR_username" 
    password: "VK_VAR_password"
    sudo_password: "VK_VAR_sudopassword"
  data:
    ls:  # Read-only data modules
      template-iso:
        path: "/var/lib/vz/template/iso"
  mods:  # Read-write command modules
    wget:
      ubuntu-20.04.6:
        path: "/var/lib/vz/template/iso"
        url: "https://releases.ubuntu.com/20.04.6/ubuntu-20.04.6-live-server-amd64.iso"
        output: "ubuntu-20.04.6-live-server-amd64.iso"
```

### State Management
- State is stored in `state.vk.json`
- Automatically created and managed by viki
- Contains current server state and applied configurations
- Used for idempotent operations and change detection

## Development Patterns

### Module System
- **Data Modules**: Read-only operations (e.g., `ls` for directory listing)
- **Command Modules**: Read-write operations (e.g., `wget` for file downloads)
- Modules are defined in `DATA_COMMAND` and `MODS_COMMAND` dictionaries
- Easy to extend without modifying core Python code

### Response Architecture
- **FetchResponse**: Handles data retrieval operations
- **PlanResponse**: Compares desired vs. current state
- **ApplyResponse**: Executes planned changes
- All inherit from `BaseResponse` for common functionality

### Error Handling
- Comprehensive logging with correlation IDs
- SSH connection validation before operations
- User approval required for destructive changes
- Graceful handling of missing files and invalid configurations

### Security Features
- Sensitive data stored in environment variables with `VK_VAR_` prefix
- SSH key-based and password authentication support
- Sudo operations with optional password authentication
- No hardcoded credentials in configuration files

## Testing

### Running Tests
```bash
# Run all tests
make test

# Run with verbose output
make test_verbose

# Direct pytest usage
PYTHONPATH=.:../ pytest
PYTHONPATH=.:../ pytest -v -s
```

### Test Structure
- Tests use pytest framework
- Environment paths configured for module imports
- Tests should be placed in appropriate test directories

## Dependencies

### Production Dependencies
- **paramiko** (3.4.0): SSH client library for remote connections
- **pyyaml** (6.0.1): YAML configuration file parsing

### Development Dependencies
- **pytest** (8.2.2): Testing framework

### Optional Tools
- **check-jsonschema**: YAML configuration validation
- **Docker**: For containerized deployments

## Workflow Commands

### Development Workflow
```bash
# Clean environment
make shell_clean

# Fresh setup
make install_new

# Development cycle
make test           # Run tests
make plan DIR=...   # Test configurations
make apply DIR=...  # Apply changes
```

### Project Maintenance
```bash
# Remove pipenv environment
pipenv --rm

# Reinstall dependencies
pipenv install
pipenv install --dev
```

## Configuration Schema

### Variable Types
Variables support these types:
- `string`: Text values
- `number`: Numeric values  
- `list`: Array values
- `map`: Object/dictionary values

### Module Parameters
Each module type has specific parameters:
- **ls module**: `path` (directory to list)
- **wget module**: `path`, `url`, `output` (file download)

## Limitations

1. **No dependency management**: Modules execute independently
2. **No update operations**: Must destroy and recreate resources
3. **No execution priority**: Use numbered config files for ordering (01.vk.yaml, 02.vk.yaml)
4. **Remote servers only**: No localhost support (planned feature)
5. **Sequential execution**: No parallel module execution

## Integration Notes

### CI/CD Integration
- Use environment variables for credentials
- Validate configurations with `check-jsonschema`
- Implement approval workflows for production deployments

### Monitoring
- All operations logged with correlation IDs
- State files track change history
- SSH connection status monitoring

This tool provides a simple yet powerful approach to server configuration management, balancing ease of use with operational safety through its declarative approach and state management.