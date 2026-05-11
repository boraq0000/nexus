"""
Management command to apply database schema migrations
"""

from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Apply database schema changes for multi-role project management system'

    # Run schema update SQL commands from Django management.
    def handle(self, *args, **options):
        sql_commands = [
            # Step 1: Modify Projects table - Add professor_id column
            """
            ALTER TABLE projects 
            ADD COLUMN IF NOT EXISTS professor_id INT;
            """,
            
            # Step 2: Add approval_status column
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
            ALTER TABLE projects 
            RENAME COLUMN score TO professor_score;
            """,
            
            # Step 5: Add foreign key for professor
            """
            DO $$ 
            BEGIN 
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint 
                    WHERE conname = 'fk_projects_professor'
                ) THEN
                    ALTER TABLE projects 
                    ADD CONSTRAINT fk_projects_professor 
                    FOREIGN KEY (professor_id) REFERENCES users(user_id)
                    ON DELETE SET NULL;
                END IF;
            END $$;
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
        
        success_count = 0
        error_count = 0
        
        with connection.cursor() as cursor:
            for i, sql in enumerate(sql_commands, 1):
                try:
                    cursor.execute(sql.strip())
                    self.stdout.write(self.style.SUCCESS(f"✓ Step {i}: Success"))
                    success_count += 1
                except Exception as e:
                    error_msg = str(e).lower()
                    # Only warn if it's not an "already exists" or similar harmless error
                    if any(phrase in error_msg for phrase in ['already exists', 'duplicate', 'already has a column']):
                        self.stdout.write(self.style.WARNING(f"ℹ Step {i}: {str(e)[:80]}..."))
                    else:
                        self.stdout.write(self.style.WARNING(f"✗ Step {i}: {str(e)[:80]}..."))
                    error_count += 1
                    # Continue with next command even if one fails
        
        # Commit all changes
        connection.commit()
        
        self.stdout.write(self.style.SUCCESS(f"\n✓ Migration completed! ({success_count} successful, {error_count} warnings)"))
