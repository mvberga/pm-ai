#!/bin/bash

# PM AI MVP - ELK Stack Deployment Script
# This script deploys the ELK Stack for logging and monitoring

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    print_status "Checking Docker status..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if Docker Compose is available
check_docker_compose() {
    print_status "Checking Docker Compose availability..."
    if ! command -v docker-compose > /dev/null 2>&1; then
        print_error "Docker Compose is not installed. Please install Docker Compose and try again."
        exit 1
    fi
    print_success "Docker Compose is available"
}

# Function to create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    # Create logging directories
    mkdir -p logging/elasticsearch/data
    mkdir -p logging/elasticsearch/logs
    mkdir -p logging/logstash/pipeline
    mkdir -p logging/logstash/config
    mkdir -p logging/logstash/templates
    mkdir -p logging/kibana/dashboards
    mkdir -p logging/kibana/index-patterns
    mkdir -p logging/filebeat
    mkdir -p logging/metricbeat
    mkdir -p logging/apm-server
    
    # Set proper permissions
    chmod -R 755 logging/
    
    print_success "Directories created successfully"
}

# Function to validate configuration files
validate_configs() {
    print_status "Validating configuration files..."
    
    # Check if required config files exist
    required_files=(
        "logging/elasticsearch/elasticsearch.yml"
        "logging/logstash/config/logstash.yml"
        "logging/logstash/pipeline/main.conf"
        "logging/logstash/templates/pm-ai-logs.json"
        "logging/kibana/kibana.yml"
        "logging/filebeat/filebeat.yml"
        "logging/metricbeat/metricbeat.yml"
        "logging/apm-server/apm-server.yml"
        "docker-compose.elk.yml"
    )
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            print_error "Required configuration file not found: $file"
            exit 1
        fi
    done
    
    print_success "All configuration files are present"
}

# Function to set up environment variables
setup_environment() {
    print_status "Setting up environment variables..."
    
    # Create .env file for ELK if it doesn't exist
    if [ ! -f ".env.elk" ]; then
        cat > .env.elk << EOF
# ELK Stack Environment Variables
ENVIRONMENT=development
ELASTICSEARCH_HEAP_SIZE=2g
LOGSTASH_HEAP_SIZE=1g
KIBANA_HEAP_SIZE=1g
REDIS_PASSWORD=your_redis_password
POSTGRES_PASSWORD=your_postgres_password
EOF
        print_warning "Created .env.elk file. Please update the passwords before proceeding."
    fi
    
    print_success "Environment variables set up"
}

# Function to deploy ELK Stack
deploy_elk() {
    print_status "Deploying ELK Stack..."
    
    # Pull latest images
    print_status "Pulling latest Docker images..."
    docker-compose -f docker-compose.elk.yml pull
    
    # Build and start services
    print_status "Starting ELK Stack services..."
    docker-compose -f docker-compose.elk.yml up -d --build
    
    print_success "ELK Stack deployment initiated"
}

# Function to wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for Elasticsearch
    print_status "Waiting for Elasticsearch..."
    for i in {1..60}; do
        if curl -f http://localhost:9200/_cluster/health > /dev/null 2>&1; then
            print_success "Elasticsearch is ready"
            break
        fi
        if [ $i -eq 60 ]; then
            print_error "Elasticsearch failed to start within 5 minutes"
            exit 1
        fi
        sleep 5
    done
    
    # Wait for Kibana
    print_status "Waiting for Kibana..."
    for i in {1..60}; do
        if curl -f http://localhost:5601/api/status > /dev/null 2>&1; then
            print_success "Kibana is ready"
            break
        fi
        if [ $i -eq 60 ]; then
            print_error "Kibana failed to start within 5 minutes"
            exit 1
        fi
        sleep 5
    done
    
    # Wait for Logstash
    print_status "Waiting for Logstash..."
    for i in {1..60}; do
        if curl -f http://localhost:9600/_node/stats > /dev/null 2>&1; then
            print_success "Logstash is ready"
            break
        fi
        if [ $i -eq 60 ]; then
            print_error "Logstash failed to start within 5 minutes"
            exit 1
        fi
        sleep 5
    done
}

# Function to set up index patterns and dashboards
setup_kibana() {
    print_status "Setting up Kibana index patterns and dashboards..."
    
    # Wait a bit more for Kibana to be fully ready
    sleep 30
    
    # Create index pattern
    print_status "Creating index pattern..."
    curl -X POST "localhost:5601/api/saved_objects/index-pattern/pm-ai-logs-*" \
        -H "kbn-xsrf: true" \
        -H "Content-Type: application/json" \
        -d '{
            "attributes": {
                "title": "pm-ai-logs-*",
                "timeFieldName": "@timestamp"
            }
        }' > /dev/null 2>&1 || print_warning "Index pattern creation failed (may already exist)"
    
    # Import dashboards
    print_status "Importing dashboards..."
    if [ -f "logging/kibana/dashboards/pm-ai-dashboard.json" ]; then
        curl -X POST "localhost:5601/api/saved_objects/_import" \
            -H "kbn-xsrf: true" \
            -H "Content-Type: application/json" \
            --data-binary @logging/kibana/dashboards/pm-ai-dashboard.json > /dev/null 2>&1 || print_warning "Dashboard import failed"
    fi
    
    print_success "Kibana setup completed"
}

# Function to display service URLs
display_urls() {
    print_success "ELK Stack deployment completed successfully!"
    echo ""
    echo "Service URLs:"
    echo "  Elasticsearch: http://localhost:9200"
    echo "  Kibana:        http://localhost:5601"
    echo "  Logstash:      http://localhost:9600"
    echo "  APM Server:    http://localhost:8200"
    echo ""
    echo "Default credentials:"
    echo "  No authentication required (development mode)"
    echo ""
    echo "Useful commands:"
    echo "  View logs:     docker-compose -f docker-compose.elk.yml logs -f"
    echo "  Stop services: docker-compose -f docker-compose.elk.yml down"
    echo "  Restart:       docker-compose -f docker-compose.elk.yml restart"
    echo ""
}

# Function to show logs
show_logs() {
    print_status "Showing ELK Stack logs..."
    docker-compose -f docker-compose.elk.yml logs -f
}

# Function to stop services
stop_services() {
    print_status "Stopping ELK Stack services..."
    docker-compose -f docker-compose.elk.yml down
    print_success "ELK Stack services stopped"
}

# Function to show status
show_status() {
    print_status "ELK Stack service status:"
    docker-compose -f docker-compose.elk.yml ps
}

# Main function
main() {
    case "${1:-deploy}" in
        "deploy")
            check_docker
            check_docker_compose
            create_directories
            validate_configs
            setup_environment
            deploy_elk
            wait_for_services
            setup_kibana
            display_urls
            ;;
        "logs")
            show_logs
            ;;
        "stop")
            stop_services
            ;;
        "status")
            show_status
            ;;
        "restart")
            stop_services
            sleep 5
            main deploy
            ;;
        *)
            echo "Usage: $0 {deploy|logs|stop|status|restart}"
            echo ""
            echo "Commands:"
            echo "  deploy  - Deploy the ELK Stack (default)"
            echo "  logs    - Show logs from all services"
            echo "  stop    - Stop all services"
            echo "  status  - Show service status"
            echo "  restart - Restart all services"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
