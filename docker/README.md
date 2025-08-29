# CFB Database Setup

This directory contains the PostgreSQL database setup for the CFB (College Football) data project.

## Quick Start

1. **Start the database:**
   ```bash
   ./db-manage.sh start
   ```

2. **Start with pgAdmin (web interface):**
   ```bash
   ./db-manage.sh start-admin
   ```

3. **Connect to the database:**
   - **Host:** localhost
   - **Port:** 5432
   - **Database:** cfb_data
   - **Username:** cfb_user
   - **Password:** cfb_password

4. **Access pgAdmin (if started with admin):**
   - **URL:** http://localhost:8080
   - **Email:** admin@cfb.local
   - **Password:** admin

## Database Schema

The database includes the following main tables:

- **`cfb.teams`** - Team information (name, conference, colors, etc.)
- **`cfb.games`** - Game data (scores, dates, venues, etc.)
- **`cfb.fpi_rankings`** - ESPN FPI rankings by week
- **`cfb.sp_rankings`** - SP+ rankings by week  
- **`cfb.game_predictions`** - Game predictions from various sources
- **`cfb.luck_rankings`** - Luck rankings from TeamRankings.com

## Management Commands

Use the `./db-manage.sh` script for database operations:

```bash
# Start/Stop
./db-manage.sh start           # Start database only
./db-manage.sh start-admin     # Start database + pgAdmin
./db-manage.sh stop            # Stop all services
./db-manage.sh restart         # Restart services
./db-manage.sh status          # Show service status

# Backup/Restore
./db-manage.sh backup          # Create timestamped backup
./db-manage.sh restore backup.sql  # Restore from backup file

# Maintenance
./db-manage.sh shell           # Connect to database shell
./db-manage.sh logs            # View database logs
./db-manage.sh reset           # Reset database (deletes all data)
./db-manage.sh clean           # Remove all containers and volumes
```

## Data Import Process

After setting up the database, you'll want to import your JSON data:

1. **Teams data:** Import from `data/team_info/2025.json`
2. **Games data:** Import from `data/games/2025_game_list.json`
3. **FPI Rankings:** Import from `data/fpi_rankings/*.json`
4. **SP+ Rankings:** Import from `data/sp_pull_rankings/*.json`
5. **Game Predictions:** Import from `data/fpi_game_predictions/*.json`
6. **Luck Rankings:** Import from `data/luck_rankings/*.json`

## File Structure

```
docker/
├── postgres/
│   ├── init/               # Database initialization scripts
│   │   └── 01-init-schema.sql
│   ├── data/               # PostgreSQL data directory (mounted)
│   └── backups/            # Database backups
├── pgadmin/                # pgAdmin configuration
docker-compose.yml          # Docker services configuration
db-manage.sh               # Database management script
.env.example               # Environment variables template
```

## Environment Variables

Copy `.env.example` to `.env` and modify as needed:

```bash
cp .env.example .env
```

## Troubleshooting

**Port 5432 already in use:**
```bash
# Check what's using the port
lsof -i :5432

# Kill existing PostgreSQL processes if needed
sudo pkill -f postgres
```

**Permission issues:**
```bash
# Fix ownership of data directory
sudo chown -R $(id -u):$(id -g) docker/postgres/data
```

**Container won't start:**
```bash
# Check logs
./db-manage.sh logs

# Reset everything
./db-manage.sh clean
./db-manage.sh start
```

## Next Steps

1. Start the database: `./db-manage.sh start`
2. Create Python scripts to parse and import your JSON data
3. Build data pipelines to keep the database updated
4. Create analysis and reporting tools
