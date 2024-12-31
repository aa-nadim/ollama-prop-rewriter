# scripts/startup.sh
#!/bin/bash

# Stop any existing containers
docker-compose down

# Remove existing volumes (optional - uncomment if needed)
# docker-compose down -v

# Start services
docker-compose up -d --build

# Wait for services to be healthy
echo "Waiting for services to become healthy..."
sleep 30

# Check if services are running
docker-compose ps


echo "Setup completed!"