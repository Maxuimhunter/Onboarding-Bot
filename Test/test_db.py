from database import Database
import mysql.connector
from mysql.connector import Error

def test_connection():
    print("🔍 Testing database connection to XAMPP MySQL...")
    try:
        # Test basic connection first
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            port=3306
        )
        
        if connection.is_connected():
            print("✅ Successfully connected to MySQL server!")
            
            # Check if database exists
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES LIKE 'discord_bot_db'")
            db_exists = cursor.fetchone()
            
            if db_exists:
                print("✅ Database 'discord_bot_db' exists")
                cursor.execute("USE discord_bot_db")
                
                # Check tables
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                
                required_tables = {'members', 'identity_info'}
                missing_tables = required_tables - set(tables)
                
                if not missing_tables:
                    print("✅ All required tables exist")
                    
                    # Show tables structure
                    print("\n📋 Database structure:")
                    for table in required_tables:
                        cursor.execute(f"DESCRIBE {table}")
                        print(f"\nTable: {table}")
                        for row in cursor:
                            print(f"  - {row[0]}: {row[1]} ({'NULL' if row[2] == 'YES' else 'NOT NULL'})")
                else:
                    print(f"⚠️  Missing tables: {', '.join(missing_tables)}")
                    print("   Tables will be created when you run the bot for the first time.")
            else:
                print("ℹ️  Database 'discord_bot_db' doesn't exist yet.")
                print("   It will be created when you run the bot for the first time.")
            
            cursor.close()
            return True
            
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure XAMPP is running and MySQL is started")
        print("2. Check if MySQL is running on port 3306")
        print("3. Verify your MySQL user has the correct permissions")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("\n🔌 MySQL connection closed")

if __name__ == "__main__":
    test_connection()
