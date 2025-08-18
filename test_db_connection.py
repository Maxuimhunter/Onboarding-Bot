import os
import sys
from database import Database

def test_database_connection():
    print("Testing database connection...")
    try:
        # Create a new database instance
        db = Database()
        
        # Test connection
        result = db.execute_query("SELECT VERSION()", fetch=True)
        if result:
            print(f"✅ Successfully connected to MySQL. Version: {result[0][0]}")
            
            # Test creating a test table
            db.execute_query("""
                CREATE TABLE IF NOT EXISTS test_table (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    test_data VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """, commit=True)
            print("✅ Test table created successfully")
            
            # Test inserting data
            test_data = "This is a test record"
            db.execute_query(
                "INSERT INTO test_table (test_data) VALUES (%s)",
                (test_data,),
                commit=True
            )
            print("✅ Test data inserted successfully")
            
            # Test reading data
            results = db.execute_query("SELECT * FROM test_table", fetch=True)
            if results:
                print("✅ Test data retrieved successfully:")
                for row in results:
                    print(f"ID: {row[0]}, Data: {row[1]}, Created: {row[2]}")
            
            # Clean up
            db.execute_query("DROP TABLE IF EXISTS test_table", commit=True)
            print("✅ Test table cleaned up")
            
            return True
            
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting database test...")
    success = test_database_connection()
    if success:
        print("✅ All database tests completed successfully!")
    else:
        print("❌ Database tests failed")
        sys.exit(1)
