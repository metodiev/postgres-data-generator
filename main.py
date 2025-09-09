import argparse
from db.connection import get_engines
from sqlalchemy import Table, MetaData
import importlib

# --- Generic insert function ---
def insert_rows(engine, table_name, rows):
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=engine)
    with engine.begin() as conn:  # handles commit automatically
        conn.execute(table.insert(), rows)

# --- Dynamically load the generator for a given table ---
def get_generator_for_table(table_name):
    try:
        module_name = f"data_generators.{table_name}_generator"
        class_name = ''.join(word.capitalize() for word in table_name.split('_')) + "Generator"
        module = importlib.import_module(module_name)
        generator_class = getattr(module, class_name)
        return generator_class()
    except (ModuleNotFoundError, AttributeError) as e:
        print(f"No generator found for table '{table_name}': {e}")
        return None

# --- Main entry ---
def main():
    parser = argparse.ArgumentParser(description="Postgres Data Generator")
    parser.add_argument("--db", type=str, help="Database name from config.yaml", required=True)
    parser.add_argument("--table", type=str, help="Table name to populate", required=True)
    parser.add_argument("--rows", type=int, help="Number of rows", default=100)
    args = parser.parse_args()

    engines = get_engines()
    engine = engines.get(args.db)
    if not engine:
        print(f"Failed to find engine for database: {args.db}")
        return

    generator = get_generator_for_table(args.table)
    if not generator:
        print(f"Cannot generate data for table: {args.table}")
        return

    rows = [generator.generate() for _ in range(args.rows)]
    insert_rows(engine, args.table, rows)
    print(f"Inserted {len(rows)} rows into {args.db}.{args.table}")

if __name__ == "__main__":
    main()
