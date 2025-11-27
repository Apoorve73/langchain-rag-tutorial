# n8n Local Setup Guide

## Quick Start

### Option 1: Using npx (No Installation Required)

Run n8n directly without installing globally:

```bash
npx n8n
```

This will start n8n and you can access it at `http://localhost:5678`

### Option 2: Install Globally

1. **Install Node.js** (minimum version 18.17.0)
   - Check if you have it: `node --version`
   - If not, install from [nodejs.org](https://nodejs.org/)

2. **Install n8n globally**:
   ```bash
   npm install n8n -g
   ```

3. **Start n8n**:
   ```bash
   n8n start
   ```

4. **Access n8n**: Open `http://localhost:5678` in your browser

### Option 3: Using Docker

If you have Docker installed:

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

## VS Code Integration

### Recommended VS Code Extensions

1. **ESLint** - For code quality
2. **n8n-utils** - VS Code extension specifically for n8n development
   - Install from VS Code marketplace
   - Provides hot reload and node parameter navigation

### VS Code Tasks Configuration

A `tasks.json` file has been created in `.vscode/` to help you start n8n directly from VS Code.

Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux) and type "Tasks: Run Task" → Select "Start n8n"

## Workflow Development

### Creating Workflows

1. Start n8n (using any method above)
2. Open `http://localhost:5678` in your browser
3. Create your first workflow in the web interface
4. Workflows are saved locally in `~/.n8n/` directory

### Exporting Workflows

You can export workflows as JSON files and version control them:

1. In n8n UI, click on your workflow
2. Click the "..." menu → "Download"
3. Save the JSON file in your project (e.g., `workflows/` directory)

### Importing Workflows

1. In n8n UI, click "+" → "Import from File"
2. Select your workflow JSON file

## Custom Nodes Development

If you want to create custom n8n nodes:

1. **Create a new node project**:
   ```bash
   npx @n8n/n8n-nodes-langchain create-node
   ```

2. **Build your node**:
   ```bash
   npm run build
   ```

3. **Link your node to n8n**:
   ```bash
   npm link
   cd ~/.n8n  # or wherever n8n is installed
   npm link <your-node-package-name>
   ```

4. **Restart n8n** to load your custom node

## Environment Variables

Create a `.env` file in your project root for n8n configuration:

```env
# n8n Configuration
N8N_PORT=5678
N8N_HOST=localhost
N8N_PROTOCOL=http

# Database (optional - defaults to SQLite)
# N8N_DB_TYPE=postgresdb
# N8N_DB_POSTGRESDB_HOST=localhost
# N8N_DB_POSTGRESDB_PORT=5432
# N8N_DB_POSTGRESDB_DATABASE=n8n
# N8N_DB_POSTGRESDB_USER=n8n
# N8N_DB_POSTGRESDB_PASSWORD=password

# Encryption Key (generate a random string)
# N8N_ENCRYPTION_KEY=your-encryption-key-here
```

## Integration with Your RAG Project

You can create n8n workflows that:
- Trigger when new documents are added
- Process documents and add them to your ChromaDB
- Query your RAG system via API
- Schedule periodic updates to your vector database

## Troubleshooting

- **Port already in use**: Change the port with `n8n start --port 5679`
- **Permission issues**: On Mac/Linux, you might need `sudo` for global npm installs
- **Node version**: Ensure you have Node.js 18.17.0 or higher

## Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community Forum](https://community.n8n.io/)
- [n8n GitHub](https://github.com/n8n-io/n8n)

