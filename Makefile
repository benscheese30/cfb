# CFB Database Makefile
# Provides convenient shortcuts for database management

.PHONY: help start start-admin stop restart status logs backup restore shell reset clean

# Default target
help:
	@echo "CFB Database Management Commands"
	@echo ""
	@echo "Database Operations:"
	@echo "  make start        Start PostgreSQL database"
	@echo "  make start-admin  Start database with pgAdmin web interface"
	@echo "  make stop         Stop all services"
	@echo "  make restart      Restart all services"
	@echo "  make status       Show service status"
	@echo "  make logs         Show database logs"
	@echo ""
	@echo "Data Management:"
	@echo "  make backup       Create database backup"
	@echo "  make restore      Restore database from backup (requires BACKUP_FILE=path)"
	@echo "  make shell        Connect to database shell"
	@echo ""
	@echo "Maintenance:"
	@echo "  make reset        Reset database (WARNING: deletes all data)"
	@echo "  make clean        Remove all containers and volumes"
	@echo ""
	@echo "Examples:"
	@echo "  make start                    # Start database"
	@echo "  make restore BACKUP_FILE=backup.sql  # Restore from backup"
	@echo ""

# Database operations
start:
	@./db-manage.sh start

start-admin:
	@./db-manage.sh start-admin

stop:
	@./db-manage.sh stop

restart:
	@./db-manage.sh restart

status:
	@./db-manage.sh status

logs:
	@./db-manage.sh logs

# Data management
backup:
	@./db-manage.sh backup

restore:
	@if [ -z "$(BACKUP_FILE)" ]; then \
		echo "Error: Please specify BACKUP_FILE=path"; \
		echo "Example: make restore BACKUP_FILE=docker/postgres/backups/backup.sql"; \
		exit 1; \
	fi
	@./db-manage.sh restore $(BACKUP_FILE)

shell:
	@./db-manage.sh shell

# Maintenance
reset:
	@./db-manage.sh reset

clean:
	@./db-manage.sh clean

# Development helpers
dev-start: start
	@echo "Database started for development"
	@echo "Connection: postgresql://cfb_user:cfb_password@localhost:5432/cfb_data"

dev-start-admin: start-admin
	@echo "Database and pgAdmin started for development"
	@echo "Database: postgresql://cfb_user:cfb_password@localhost:5432/cfb_data"
	@echo "pgAdmin: http://localhost:8080 (admin@cfb.local / admin)"

# Quick backup with timestamp
quick-backup:
	@echo "Creating quick backup..."
	@./db-manage.sh backup
	@echo "Backup completed!"

# Show connection info
connection-info:
	@echo "CFB Database Connection Information:"
	@echo "  Host: localhost"
	@echo "  Port: 5432"
	@echo "  Database: cfb_data"
	@echo "  Username: cfb_user"
	@echo "  Password: cfb_password"
	@echo ""
	@echo "Connection String:"
	@echo "  postgresql://cfb_user:cfb_password@localhost:5432/cfb_data"
