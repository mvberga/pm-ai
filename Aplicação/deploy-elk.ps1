# PM AI MVP - ELK Stack Deployment Script (PowerShell)
# This script deploys the ELK Stack for logging and monitoring

param(
    [Parameter(Position=0)]
    [ValidateSet("deploy", "logs", "stop", "status", "restart")]
    [string]$Action = "deploy"
)

# Function to print colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Function to check if Docker is running
function Test-Docker {
    Write-Status "Checking Docker status..."
    try {
        docker info | Out-Null
        Write-Success "Docker is running"
    }
    catch {
        Write-Error "Docker is not running. Please start Docker and try again."
        exit 1
    }
}

# Function to check if Docker Compose is available
function Test-DockerCompose {
    Write-Status "Checking Docker Compose availability..."
    try {
        docker-compose --version | Out-Null
        Write-Success "Docker Compose is available"
    }
    catch {
        Write-Error "Docker Compose is not installed. Please install Docker Compose and try again."
        exit 1
    }
}

# Function to create necessary directories
function New-Directories {
    Write-Status "Creating necessary directories..."
    
    # Create logging directories
    $directories = @(
        "logging/elasticsearch/data",
        "logging/elasticsearch/logs",
        "logging/logstash/pipeline",
        "logging/logstash/config",
        "logging/logstash/templates",
        "logging/kibana/dashboards",
        "logging/kibana/index-patterns",
        "logging/filebeat",
        "logging/metricbeat",
        "logging/apm-server"
    )
    
    foreach ($dir in $directories) {
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
        }
    }
    
    Write-Success "Directories created successfully"
}

# Function to validate configuration files
function Test-Configs {
    Write-Status "Validating configuration files..."
    
    $requiredFiles = @(
        "logging/elasticsearch/elasticsearch.yml",
        "logging/logstash/config/logstash.yml",
        "logging/logstash/pipeline/main.conf",
        "logging/logstash/templates/pm-ai-logs.json",
        "logging/kibana/kibana.yml",
        "logging/filebeat/filebeat.yml",
        "logging/metricbeat/metricbeat.yml",
        "logging/apm-server/apm-server.yml",
        "docker-compose.elk.yml"
    )
    
    foreach ($file in $requiredFiles) {
        if (!(Test-Path $file)) {
            Write-Error "Required configuration file not found: $file"
            exit 1
        }
    }
    
    Write-Success "All configuration files are present"
}

# Function to set up environment variables
function Set-Environment {
    Write-Status "Setting up environment variables..."
    
    # Create .env file for ELK if it doesn't exist
    if (!(Test-Path ".env.elk")) {
        $envContent = @"
# ELK Stack Environment Variables
ENVIRONMENT=development
ELASTICSEARCH_HEAP_SIZE=2g
LOGSTASH_HEAP_SIZE=1g
KIBANA_HEAP_SIZE=1g
REDIS_PASSWORD=your_redis_password
POSTGRES_PASSWORD=your_postgres_password
"@
        $envContent | Out-File -FilePath ".env.elk" -Encoding UTF8
        Write-Warning "Created .env.elk file. Please update the passwords before proceeding."
    }
    
    Write-Success "Environment variables set up"
}

# Function to deploy ELK Stack
function Start-ELK {
    Write-Status "Deploying ELK Stack..."
    
    # Pull latest images
    Write-Status "Pulling latest Docker images..."
    docker-compose -f docker-compose.elk.yml pull
    
    # Build and start services
    Write-Status "Starting ELK Stack services..."
    docker-compose -f docker-compose.elk.yml up -d --build
    
    Write-Success "ELK Stack deployment initiated"
}

# Function to wait for services to be ready
function Wait-Services {
    Write-Status "Waiting for services to be ready..."
    
    # Wait for Elasticsearch
    Write-Status "Waiting for Elasticsearch..."
    for ($i = 1; $i -le 60; $i++) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:9200/_cluster/health" -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Success "Elasticsearch is ready"
                break
            }
        }
        catch {
            if ($i -eq 60) {
                Write-Error "Elasticsearch failed to start within 5 minutes"
                exit 1
            }
            Start-Sleep -Seconds 5
        }
    }
    
    # Wait for Kibana
    Write-Status "Waiting for Kibana..."
    for ($i = 1; $i -le 60; $i++) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:5601/api/status" -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Success "Kibana is ready"
                break
            }
        }
        catch {
            if ($i -eq 60) {
                Write-Error "Kibana failed to start within 5 minutes"
                exit 1
            }
            Start-Sleep -Seconds 5
        }
    }
    
    # Wait for Logstash
    Write-Status "Waiting for Logstash..."
    for ($i = 1; $i -le 60; $i++) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:9600/_node/stats" -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -eq 200) {
                Write-Success "Logstash is ready"
                break
            }
        }
        catch {
            if ($i -eq 60) {
                Write-Error "Logstash failed to start within 5 minutes"
                exit 1
            }
            Start-Sleep -Seconds 5
        }
    }
}

# Function to set up index patterns and dashboards
function Set-Kibana {
    Write-Status "Setting up Kibana index patterns and dashboards..."
    
    # Wait a bit more for Kibana to be fully ready
    Start-Sleep -Seconds 30
    
    # Create index pattern
    Write-Status "Creating index pattern..."
    try {
        $indexPattern = @{
            attributes = @{
                title = "pm-ai-logs-*"
                timeFieldName = "@timestamp"
            }
        } | ConvertTo-Json -Depth 3
        
        Invoke-WebRequest -Uri "localhost:5601/api/saved_objects/index-pattern/pm-ai-logs-*" `
            -Method POST `
            -Headers @{"kbn-xsrf" = "true"; "Content-Type" = "application/json"} `
            -Body $indexPattern `
            -UseBasicParsing | Out-Null
    }
    catch {
        Write-Warning "Index pattern creation failed (may already exist)"
    }
    
    # Import dashboards
    Write-Status "Importing dashboards..."
    if (Test-Path "logging/kibana/dashboards/pm-ai-dashboard.json") {
        try {
            $dashboardContent = Get-Content "logging/kibana/dashboards/pm-ai-dashboard.json" -Raw
            Invoke-WebRequest -Uri "localhost:5601/api/saved_objects/_import" `
                -Method POST `
                -Headers @{"kbn-xsrf" = "true"; "Content-Type" = "application/json"} `
                -Body $dashboardContent `
                -UseBasicParsing | Out-Null
        }
        catch {
            Write-Warning "Dashboard import failed"
        }
    }
    
    Write-Success "Kibana setup completed"
}

# Function to display service URLs
function Show-URLs {
    Write-Success "ELK Stack deployment completed successfully!"
    Write-Host ""
    Write-Host "Service URLs:"
    Write-Host "  Elasticsearch: http://localhost:9200"
    Write-Host "  Kibana:        http://localhost:5601"
    Write-Host "  Logstash:      http://localhost:9600"
    Write-Host "  APM Server:    http://localhost:8200"
    Write-Host ""
    Write-Host "Default credentials:"
    Write-Host "  No authentication required (development mode)"
    Write-Host ""
    Write-Host "Useful commands:"
    Write-Host "  View logs:     docker-compose -f docker-compose.elk.yml logs -f"
    Write-Host "  Stop services: docker-compose -f docker-compose.elk.yml down"
    Write-Host "  Restart:       docker-compose -f docker-compose.elk.yml restart"
    Write-Host ""
}

# Function to show logs
function Show-Logs {
    Write-Status "Showing ELK Stack logs..."
    docker-compose -f docker-compose.elk.yml logs -f
}

# Function to stop services
function Stop-Services {
    Write-Status "Stopping ELK Stack services..."
    docker-compose -f docker-compose.elk.yml down
    Write-Success "ELK Stack services stopped"
}

# Function to show status
function Show-Status {
    Write-Status "ELK Stack service status:"
    docker-compose -f docker-compose.elk.yml ps
}

# Main function
function Main {
    switch ($Action) {
        "deploy" {
            Test-Docker
            Test-DockerCompose
            New-Directories
            Test-Configs
            Set-Environment
            Start-ELK
            Wait-Services
            Set-Kibana
            Show-URLs
        }
        "logs" {
            Show-Logs
        }
        "stop" {
            Stop-Services
        }
        "status" {
            Show-Status
        }
        "restart" {
            Stop-Services
            Start-Sleep -Seconds 5
            Main -Action "deploy"
        }
        default {
            Write-Host "Usage: .\deploy-elk.ps1 {deploy|logs|stop|status|restart}"
            Write-Host ""
            Write-Host "Commands:"
            Write-Host "  deploy  - Deploy the ELK Stack (default)"
            Write-Host "  logs    - Show logs from all services"
            Write-Host "  stop    - Stop all services"
            Write-Host "  status  - Show service status"
            Write-Host "  restart - Restart all services"
            exit 1
        }
    }
}

# Run main function
Main
