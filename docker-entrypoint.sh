
#!/bin/bash

# Docker entrypoint script for Research made Readable application
# This script handles initialization and graceful startup

set -e

echo "🐳 Starting Research made Readable Docker Container..."

# Check if required environment variables are set
if [ -z "$ABACUSAI_API_KEY" ]; then
    echo "⚠️  WARNING: ABACUSAI_API_KEY environment variable is not set"
    echo "   Please set your AbacusAI API key in the .env file or docker-compose.yml"
    echo "   Get your API key from: https://abacus.ai/"
fi

# Create necessary directories if they don't exist
mkdir -p /app/data/db /app/data/uploads /app/data/exports /app/logs

# Set proper permissions
chmod -R 755 /app/data /app/logs

# Check if data directory is properly mounted
if [ ! -w "/app/data" ]; then
    echo "⚠️  WARNING: Data directory is not writable"
    echo "   Please ensure the data directory is properly mounted and has write permissions"
fi

echo "✅ Environment checks completed"
echo "🚀 Starting Streamlit application..."

# Execute the main command
exec "$@"
