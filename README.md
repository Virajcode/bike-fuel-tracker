# Bike Fuel Tracker

A command-line application to track your motorcycle/bike fuel expenses and mileage.

## Features

- Track fuel fill-ups with date, amount, cost, and odometer reading
- Calculate average fuel consumption
- View fuel expense history
- Generate basic statistics and reports
- Data stored in SQLite database

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Virajcode/bike-fuel-tracker.git
   cd bike-fuel-tracker
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python bike_fuel_tracker.py
```

Available commands:
- `add`: Add a new fuel fill-up record
- `history`: View fuel fill-up history
- `stats`: View statistics (avg. consumption, total expenses)
- `export`: Export data to CSV
- `help`: Show help message
- `exit`: Exit the application

## Data Storage

All data is stored locally in a SQLite database file named `fuel_data.db`.

## Contributing

Feel free to open issues or submit pull requests to improve the application.

## License

MIT License