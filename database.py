import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME', 'discord_bot_db')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '') or None  # Empty string becomes None for no password
        self.port = int(os.getenv('DB_PORT', '3306'))
        self.connection = None
        try:
            self.connect()
            self.initialize_database()
        except Exception as e:
            print(f"Error during database initialization: {e}")
            if self.connection:
                self.connection.close()

    def connect(self):
        try:
            # For XAMPP, we need to connect without a database first to create it if needed
            connection_params = {
                'host': self.host,
                'user': self.user,
                'port': self.port
            }
            if self.password:
                connection_params['password'] = self.password
                
            self.connection = mysql.connector.connect(**connection_params)
            
            # Create database if it doesn't exist
            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cursor.close()
            
            # Reconnect with the database selected
            connection_params['database'] = self.database
            self.connection = mysql.connector.connect(**connection_params)
            print("Successfully connected to MySQL database")
            return True
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return False

    def execute_query(self, query, params=None, fetch=False, commit=False):
        """Execute a SQL query"""
        cursor = None
        try:
            if not self.connection or not hasattr(self.connection, 'is_connected') or not self.connection.is_connected():
                self.connect()
                
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            
            if commit:
                self.connection.commit()
                return cursor.lastrowid
                
            if fetch:
                return cursor.fetchall()
                
            return True
            
        except Error as e:
            print(f"Error executing query: {e}")
            if self.connection:
                self.connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()

    def initialize_database(self):
        """Initialize the database and create tables if they don't exist"""
        try:
            # Create members table
            # Create database if not exists
            self.execute_query(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            self.connection.database = self.database
            
            # Create members table
            members_table = """
            CREATE TABLE IF NOT EXISTS members (
                id INT AUTO_INCREMENT PRIMARY KEY,
                entry_code VARCHAR(255) UNIQUE NOT NULL,
                user_id VARCHAR(255) NOT NULL,
                full_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(50),
                date_of_birth VARCHAR(50),
                file_path TEXT,
                registration_date VARCHAR(50) NOT NULL,
                status VARCHAR(20) DEFAULT 'Active' CHECK (status IN ('Active', 'Inactive', 'Suspended')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_user_id (user_id),
                INDEX idx_entry_code (entry_code)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            
            # Create identity_info table for sensitive data
            identity_table = """
            CREATE TABLE IF NOT EXISTS identity_info (
                id INT AUTO_INCREMENT PRIMARY KEY,
                member_id INT,
                id_number VARCHAR(50),
                passport_number VARCHAR(50),
                kra_number VARCHAR(50),
                last_updated VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE,
                UNIQUE (member_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """
            
            # Enable foreign key checks
            self.execute_query("SET FOREIGN_KEY_CHECKS=0")
            
            # Create tables
            self.execute_query(members_table)
            self.execute_query(identity_table)
            
            # Enable foreign key checks
            self.execute_query("SET FOREIGN_KEY_CHECKS=1")
            
        except Error as e:
            print(f"Error initializing database: {e}")
            raise

    def save_member(self, user_id, data):
        """Save member data to the database"""
        try:
            # Check if user exists
            existing_member = self.execute_query(
                "SELECT id FROM members WHERE user_id = %s ORDER BY id DESC LIMIT 1",
                (user_id,),
                fetch=True
            )
            
            # Always create a new entry
            entry_code = self._generate_entry_code()
            
            # Insert member data
            member_id = self.execute_query(
                """
                INSERT INTO members 
                (entry_code, user_id, full_name, email, phone, date_of_birth, file_path, registration_date, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    entry_code,
                    str(user_id),
                    data.get('full_name', '').title(),
                    data.get('email', '').lower(),
                    data.get('phone', ''),
                    data.get('dob', None),
                    data.get('file_path', 'No file uploaded'),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'Active'
                ),
                commit=True
            )
            
            # Save identity information if available
            if any(key in data for key in ['id_number', 'passport', 'kra']):
                self.save_identity_info(member_id, data)
            
            return entry_code
            
        except Error as e:
            print(f"Error saving member: {e}")
            raise

    def save_identity_info(self, member_id, data):
        """Save identity information for a member"""
        try:
            # Check if identity info already exists
            existing = self.execute_query(
                "SELECT id FROM identity_info WHERE member_id = %s",
                (member_id,),
                fetch=True
            )
            
            if existing:
                # Update existing identity info
                self.execute_query(
                    """
                    UPDATE identity_info 
                    SET id_number = %s, 
                        passport_number = %s, 
                        kra_number = %s,
                        last_updated = %s
                    WHERE member_id = %s
                    """,
                    (
                        data.get('id_number'),
                        data.get('passport'),
                        data.get('kra'),
                        datetime.now(),
                        member_id
                    ),
                    commit=True
                )
            else:
                # Insert new identity info
                self.execute_query(
                    """
                    INSERT INTO identity_info 
                    (member_id, id_number, passport_number, kra_number, last_updated)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        member_id,
                        data.get('id_number'),
                        data.get('passport'),
                        data.get('kra'),
                        datetime.now()
                    ),
                    commit=True
                )
                
        except Error as e:
            print(f"Error saving identity info: {e}")
            raise

    def get_member(self, entry_code=None, user_id=None):
        """Get member data by entry code or user ID"""
        try:
            if entry_code:
                return self.execute_query(
                    """
                    SELECT m.*, i.id_number, i.passport_number, i.kra_number
                    FROM members m
                    LEFT JOIN identity_info i ON m.id = i.member_id
                    WHERE m.entry_code = %s
                    """,
                    (entry_code,),
                    fetch=True
                )
            elif user_id:
                return self.execute_query(
                    """
                    SELECT m.*, i.id_number, i.passport_number, i.kra_number
                    FROM members m
                    LEFT JOIN identity_info i ON m.id = i.member_id
                    WHERE m.user_id = %s
                    ORDER BY m.id DESC
                    LIMIT 1
                    """,
                    (str(user_id),),
                    fetch=True
                )
            return None
        except Error as e:
            print(f"Error getting member: {e}")
            raise

    def update_member_status(self, entry_code, status):
        """Update member status"""
        try:
            self.execute_query(
                "UPDATE members SET status = %s WHERE entry_code = %s",
                (status, entry_code),
                commit=True
            )
            return True
        except Error as e:
            print(f"Error updating member status: {e}")
            return False

    def get_all_members(self):
        """Get all members with their details"""
        try:
            return self.execute_query(
                """
                SELECT m.entry_code, m.full_name, m.email, m.phone, m.registration_date, m.status
                FROM members m
                ORDER BY m.registration_date DESC
                """,
                fetch=True
            )
        except Error as e:
            print(f"Error getting all members: {e}")
            return []

    def _generate_entry_code(self, length=8):
        """Generate a unique entry code"""
        import string
        import random
        
        while True:
            # Generate random code
            chars = string.ascii_uppercase + string.digits
            code = ''.join(random.choice(chars) for _ in range(length))
            
            # Check if code already exists
            existing = self.execute_query(
                "SELECT id FROM members WHERE entry_code = %s",
                (code,),
                fetch=True
            )
            
            if not existing:
                return code

# Create a global database instance
db = Database()
