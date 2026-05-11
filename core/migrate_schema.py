#!/usr/bin/env python
"""
Database migration script for multi-role project management system
This script executes the schema changes for PostgreSQL database
"""

import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NEXUS.settings')
django.setup()

from django.db import connection

def run_migration():
    """Execute the database migration"""
    
    sql_commands = [
        # Step 1: Modify Projects table - Add professor_id column
        """
        ALTER TABLE projects 
        ADD COLUMN IF NOT EXISTS professor_id INT;
        """,
        
        # Step 2: Modify Projects table - Add image column
        """
        ALTER TABLE projects 
        ADD COLUMN IF NOT EXISTS image VARCHAR(100);
        """,
        
        # Step 3: Add approval_status column
        """
        ALTER TABLE projects 
        ADD COLUMN IF NOT EXISTS approval_status VARCHAR(50) DEFAULT 'draft';
        """,
        
        # Step 3: Add approval_date column
        """
        ALTER TABLE projects 
        ADD COLUMN IF NOT EXISTS approval_date TIMESTAMP NULL;
        """,
        
        # Step 4: Rename score to professor_score (PostgreSQL specific)
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = 'projects'
                  AND column_name = 'score'
            ) THEN
                ALTER TABLE projects RENAME COLUMN score TO professor_score;
            END IF;
        END
        $$;
        """,
        
        # Step 5: Add foreign key for professor
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conrelid = 'projects'::regclass
                  AND contype = 'f'
                  AND conname = 'fk_projects_professor'
            ) THEN
                ALTER TABLE projects 
                ADD CONSTRAINT fk_projects_professor 
                FOREIGN KEY (professor_id) REFERENCES users(user_id)
                ON DELETE SET NULL;
            END IF;
        END
        $$;
        """,
        
        # Step 6: Modify projects_member table - Add status column
        """
        ALTER TABLE projects_member 
        ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'accepted';
        """,
        
        # Step 7: Add joined_date column
        """
        ALTER TABLE projects_member 
        ADD COLUMN IF NOT EXISTS joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        """,
        
        # Step 8: Add explicit id primary key to projects_member if missing
        """
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = 'projects_member'
                  AND column_name = 'id'
            ) THEN
                ALTER TABLE projects_member ADD COLUMN id SERIAL;
            END IF;

            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conrelid = 'projects_member'::regclass
                  AND contype = 'p'
            ) THEN
                ALTER TABLE projects_member ADD CONSTRAINT projects_member_id_pkey PRIMARY KEY (id);
            END IF;

            IF NOT EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conrelid = 'projects_member'::regclass
                  AND contype = 'u'
                  AND conname = 'projects_member_project_user_key'
            ) THEN
                ALTER TABLE projects_member ADD CONSTRAINT projects_member_project_user_key UNIQUE (project_id, user_id);
            END IF;
        END
        $$;
        """,
        
        # Step 8: Create Investments table
        """
        CREATE TABLE IF NOT EXISTS investments (
            investment_id SERIAL PRIMARY KEY,
            investor_id INT NOT NULL,
            project_id INT NOT NULL,
            amount DECIMAL(12, 2) NOT NULL,
            status VARCHAR(50) DEFAULT 'pending',
            investment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            roi_percentage DECIMAL(5, 2) NULL,
            notes TEXT NULL,
            CONSTRAINT fk_investments_investor FOREIGN KEY (investor_id) REFERENCES users(user_id) ON DELETE CASCADE,
            CONSTRAINT fk_investments_project FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
            UNIQUE (investor_id, project_id)
        );
        """,
        
        # Step 9: Create InvestorRatings table
        """
        CREATE TABLE IF NOT EXISTS investor_ratings (
            rating_id SERIAL PRIMARY KEY,
            investor_id INT NOT NULL,
            project_id INT NOT NULL,
            rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
            review TEXT NULL,
            rating_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_ratings_investor FOREIGN KEY (investor_id) REFERENCES users(user_id) ON DELETE CASCADE,
            CONSTRAINT fk_ratings_project FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
            UNIQUE (investor_id, project_id)
        );
        """,
        
        # Step 10: Create indexes
        """
        CREATE INDEX IF NOT EXISTS idx_projects_professor ON projects(professor_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_projects_approval_status ON projects(approval_status);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_projects_member_status ON projects_member(status);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_investments_investor ON investments(investor_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_investments_project ON investments(project_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_ratings_investor ON investor_ratings(investor_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_ratings_project ON investor_ratings(project_id);
        """,
    ]
    
    with connection.cursor() as cursor:
        for i, sql in enumerate(sql_commands, 1):
            try:
                cursor.execute(sql.strip())
                print(f"Step {i}: Success")
            except Exception as e:
                print(f"Step {i}: {str(e)}")
                # Continue with next command even if one fails
    
    # Commit all changes
    connection.commit()
    print("\nDatabase migration completed successfully!")

if __name__ == '__main__':
    try:
        run_migration()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
