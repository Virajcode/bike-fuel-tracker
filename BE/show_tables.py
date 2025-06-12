from sqlalchemy import inspect, text
from models import engine, SessionLocal

# Create an inspector and session
inspector = inspect(engine)
session = SessionLocal()

# Get table names
print("\nAvailable tables:")
print("-" * 50)
for table_name in inspector.get_table_names():
    print(f"\nTable: {table_name}")
    print("-" * 50)
    
    # Get column information
    print("Columns:")
    print("-" * 30)
    for column in inspector.get_columns(table_name):
        print(f"Column: {column['name']}")
        print(f"Type: {column['type']}")
        print(f"Nullable: {column['nullable']}")
        print("-" * 30)
    
    # Get table data
    print("\nTable Data:")
    print("-" * 30)
    try:
        result = session.execute(text(f'SELECT * FROM {table_name}'))
        rows = result.fetchall()
        if rows:
            # Print column names
            print("| " + " | ".join(str(col) for col in result.keys()) + " |")
            print("-" * 80)
            # Print rows
            for row in rows:
                print("| " + " | ".join(str(val) for val in row) + " |")
        else:
            print("No data in this table")
        print("-" * 80)
    except Exception as e:
        print(f"Error fetching data: {e}")
    print("\n")

session.close()
