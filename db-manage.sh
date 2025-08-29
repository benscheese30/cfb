#!/bin/bash

# CFB Database Management Script
# Usage: ./db-manage.sh [command]

set -e

# Configuration
COMPOSE_FILE="docker-compose.yml"
DB_CONTAINER="cfb_postgres"
DB_NAME="cfb_data"
DB_USER="cfb_user"
BACKUP_DIR="./docker/postgres/backups"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_usage() {
    echo "CFB Database Management Script"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  start           Start the database (without pgAdmin)"
    echo "  start-admin     Start database with pgAdmin"
    echo "  stop            Stop all services"
    echo "  restart         Restart all services"
    echo "  status          Show service status"
    echo "  logs            Show database logs"
    echo "  backup          Create database backup"
    echo "  restore [file]  Restore database from backup"
    echo "  shell           Connect to database shell"
    echo "  reset           Reset database (WARNING: deletes all data)"
    echo "  clean           Remove all containers and volumes"
    echo ""
}

start_db() {
    echo -e "${GREEN}Starting CFB PostgreSQL database...${NC}"
    docker-compose -f $COMPOSE_FILE up -d postgres
    echo -e "${GREEN}Database started successfully!${NC}"
    echo "Connection details:"
    echo "  Host: localhost"
    echo "  Port: 5432"
    echo "  Database: $DB_NAME"
    echo "  Username: $DB_USER"
}

start_with_admin() {
    echo -e "${GREEN}Starting CFB PostgreSQL database with pgAdmin...${NC}"
    docker-compose -f $COMPOSE_FILE --profile admin up -d
    echo -e "${GREEN}Database and pgAdmin started successfully!${NC}"
    echo "Connection details:"
    echo "  Database - Host: localhost, Port: 5432, DB: $DB_NAME, User: $DB_USER"
    echo "  pgAdmin - http://localhost:8080 (admin@cfb.local / admin)"
}

stop_services() {
    echo -e "${YELLOW}Stopping CFB services...${NC}"
    docker-compose -f $COMPOSE_FILE down
    echo -e "${GREEN}Services stopped.${NC}"
}

restart_services() {
    echo -e "${YELLOW}Restarting CFB services...${NC}"
    docker-compose -f $COMPOSE_FILE restart
    echo -e "${GREEN}Services restarted.${NC}"
}

show_status() {
    echo -e "${GREEN}CFB Services Status:${NC}"
    docker-compose -f $COMPOSE_FILE ps
}

show_logs() {
    echo -e "${GREEN}Database logs:${NC}"
    docker-compose -f $COMPOSE_FILE logs -f postgres
}

backup_db() {
    echo -e "${GREEN}Creating database backup...${NC}"
    
    # Create backup directory if it doesn't exist
    mkdir -p $BACKUP_DIR
    
    # Generate backup filename with timestamp
    BACKUP_FILE="$BACKUP_DIR/cfb_backup_$(date +%Y%m%d_%H%M%S).sql"
    
    # Create backup
    docker exec $DB_CONTAINER pg_dump -U $DB_USER -d $DB_NAME > "$BACKUP_FILE"
    
    echo -e "${GREEN}Backup created: $BACKUP_FILE${NC}"
    
    # Compress backup
    gzip "$BACKUP_FILE"
    echo -e "${GREEN}Backup compressed: $BACKUP_FILE.gz${NC}"
}

restore_db() {
    if [ -z "$1" ]; then
        echo -e "${RED}Error: Please specify backup file to restore${NC}"
        echo "Usage: $0 restore <backup_file>"
        exit 1
    fi
    
    BACKUP_FILE="$1"
    
    if [ ! -f "$BACKUP_FILE" ]; then
        echo -e "${RED}Error: Backup file '$BACKUP_FILE' not found${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Restoring database from $BACKUP_FILE...${NC}"
    echo -e "${RED}WARNING: This will overwrite all existing data!${NC}"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Check if file is gzipped
        if [[ "$BACKUP_FILE" == *.gz ]]; then
            gunzip -c "$BACKUP_FILE" | docker exec -i $DB_CONTAINER psql -U $DB_USER -d $DB_NAME
        else
            docker exec -i $DB_CONTAINER psql -U $DB_USER -d $DB_NAME < "$BACKUP_FILE"
        fi
        echo -e "${GREEN}Database restored successfully!${NC}"
    else
        echo -e "${YELLOW}Restore cancelled.${NC}"
    fi
}

db_shell() {
    echo -e "${GREEN}Connecting to database shell...${NC}"
    docker exec -it $DB_CONTAINER psql -U $DB_USER -d $DB_NAME
}

reset_db() {
    echo -e "${RED}WARNING: This will delete ALL database data!${NC}"
    read -p "Are you sure you want to reset the database? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Resetting database...${NC}"
        docker-compose -f $COMPOSE_FILE down -v
        docker-compose -f $COMPOSE_FILE up -d postgres
        echo -e "${GREEN}Database reset complete!${NC}"
    else
        echo -e "${YELLOW}Reset cancelled.${NC}"
    fi
}

clean_all() {
    echo -e "${RED}WARNING: This will remove all containers, volumes, and data!${NC}"
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Cleaning up all CFB Docker resources...${NC}"
        docker-compose -f $COMPOSE_FILE down -v --remove-orphans
        docker system prune -f
        echo -e "${GREEN}Cleanup complete!${NC}"
    else
        echo -e "${YELLOW}Cleanup cancelled.${NC}"
    fi
}

# Main script logic
case "$1" in
    start)
        start_db
        ;;
    start-admin)
        start_with_admin
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    backup)
        backup_db
        ;;
    restore)
        restore_db "$2"
        ;;
    shell)
        db_shell
        ;;
    reset)
        reset_db
        ;;
    clean)
        clean_all
        ;;
    *)
        print_usage
        exit 1
        ;;
esac
