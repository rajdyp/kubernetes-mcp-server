# kubernetes-mcp-server

MCP (Model Context Protocol) server for read-only Kubernetes operations using the official Kubernetes Python client.

## Features

- 🚀 Simple and lightweight
- 📖 Read-only operations (safe to use)
- 🔧 Easy to extend with more Kubernetes API operations
- 🐍 Built with Python, fastmcp, and the official Kubernetes client

## Prerequisites

- Python 3.10 or higher
- A kubeconfig file (usually at `~/.kube/config`)
- Access to a Kubernetes cluster

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd kubernetes-mcp-server
```

2. Install dependencies:
```bash
pip install fastmcp kubernetes
# or using the project file:
pip install -e .
```

## Repository Structure

```
kubernetes-mcp-server/
├── k8s_mcp_server/          # Main package directory
│   ├── __init__.py          # Package initialization
│   ├── server.py            # MCP server with Kubernetes tools
│   ├── client.py            # Kubernetes API client setup
│   ├── config.py            # Configuration and logging
│   └── resources/           # Resource-specific modules
│       ├── __init__.py
│       └── pods.py          # Pod operations
├── pyproject.toml           # Project configuration and dependencies
├── README.md                # This file
└── LICENSE                  # License file
```

## Usage

### Running the Server

```bash
python -m k8s_mcp_server.server
```

Or using fastmcp directly:
```bash
fastmcp run k8s_mcp_server/server.py
```

## License

See [LICENSE](LICENSE) file for details.
