import sqlite3
import datetime
from tabulate import tabulate
import pandas as pd

class FuelTracker:
    def __init__(self):
        self.conn = sqlite3.connect('fuel_data.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS fuel_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            liters REAL,
            cost REAL,
            odometer INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        self.conn.commit()

    def add_record(self, liters, cost, odometer):
        cursor = self.conn.cursor()
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        cursor.execute('INSERT INTO fuel_records (date, liters, cost, odometer) VALUES (?, ?, ?, ?)',
                      (date, liters, cost, odometer))
        self.conn.commit()
        print('Record added successfully!')

    def view_history(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT date, liters, cost, odometer FROM fuel_records ORDER BY date DESC')
        records = cursor.fetchall()
        if records:
            headers = ['Date', 'Liters', 'Cost', 'Odometer']
            print(tabulate(records, headers=headers, tablefmt='grid'))
        else:
            print('No records found.')

    def calculate_statistics(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        SELECT 
            COUNT(*) as fill_ups,
            SUM(cost) as total_cost,
            SUM(liters) as total_liters,
            MAX(odometer) - MIN(odometer) as total_distance
        FROM fuel_records
        ''')
        stats = cursor.fetchone()
        if stats[0] > 0:
            fill_ups, total_cost, total_liters, total_distance = stats
            avg_consumption = (total_liters * 100) / total_distance if total_distance else 0
            print('\nStatistics:')
            print(f'Total fill-ups: {fill_ups}')
            print(f'Total cost: ${total_cost:.2f}')
            print(f'Average consumption: {avg_consumption:.2f}L/100km')
        else:
            print('No data available for statistics.')

    def export_to_csv(self):
        query = 'SELECT * FROM fuel_records'
        df = pd.read_sql_query(query, self.conn)
        df.to_csv('fuel_records.csv', index=False)
        print('Data exported to fuel_records.csv')

def main():
    tracker = FuelTracker()
    
    while True:
        print('\nBike Fuel Tracker - Commands:')
        print('1. add - Add new fuel record')
        print('2. history - View fuel history')
        print('3. stats - View statistics')
        print('4. export - Export to CSV')
        print('5. exit - Exit application')
        
        command = input('\nEnter command: ').lower()
        
        if command == 'add':
            try:
                liters = float(input('Enter liters filled: '))
                cost = float(input('Enter total cost: '))
                odometer = int(input('Enter current odometer reading: '))
                tracker.add_record(liters, cost, odometer)
            except ValueError:
                print('Please enter valid numbers.')
        
        elif command == 'history':
            tracker.view_history()
        
        elif command == 'stats':
            tracker.calculate_statistics()
        
        elif command == 'export':
            tracker.export_to_csv()
        
        elif command == 'exit':
            print('Goodbye!')
            break
        
        else:
            print('Invalid command. Please try again.')

if __name__ == '__main__':
    main()