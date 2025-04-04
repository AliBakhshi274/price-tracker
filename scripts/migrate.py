"""
This script simplifies the execution of Flask-Migrate commands for database migrations.
It provides two functions: 'migrate' and 'upgrade', which execute the corresponding Flask-Migrate commands.

Usage:
To run the script, use the following command in your terminal:

python scripts/migrate.py <command>

where <command> can be either 'migrate' or 'upgrade'.

- 'migrate': Executes the 'flask db migrate' command to generate a new migration script based on changes in your SQLAlchemy models.
- 'upgrade': Executes the 'flask db upgrade' command to apply all pending migrations to your database.

This script ensures that the 'migrations' folder exists before executing the commands. If it doesn't exist, it creates it using the 'flask db init' command.

Example:
To generate a new migration script:

python scripts/migrate.py migrate

To apply all pending migrations:

python scripts/migrate.py upgrade

This script helps streamline database migration management in Flask projects.
"""

import subprocess, os

def migrate():
    if not os.path.exists("../migrations"):
        subprocess.run(["flask", "db", "init"])
    subprocess.run(["flask", "db", "migrate", "-m", "Add product and PriceHistory model"])

def upgrade():
    subprocess.run(["flask", "db", "upgrade"])

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "migrate":
            migrate()
        elif command == "upgrade":
            upgrade()
        else:
            print("Unknown command")
    else:
        print("Usage: migrate or upgrade")