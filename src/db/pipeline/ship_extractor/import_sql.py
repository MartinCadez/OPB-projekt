import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

ship_df = pd.read_csv("ship.csv")
ship_type_df = pd.read_csv("ship_type.csv")
country_df = pd.read_csv("country.csv")
port_df = pd.read_csv("port.csv")
cargo_type_df = pd.read_csv("cargo_type.csv")
visit_df = pd.read_csv("visit.csv")

conn = psycopg2.connect(
    dbname="dash_analytics",
    user="app_user",
    password="mysecretpassword",
    host="localhost",
    port="5434"
)
cur = conn.cursor()

def bulk_insert(df, table, columns):
    values = [tuple(x) for x in df[columns].to_numpy()]
    execute_values(cur,
        f"INSERT INTO {table} ({', '.join(columns)}) VALUES %s ON CONFLICT DO NOTHING",
        values
    )

bulk_insert(ship_type_df, 'dim_ship_type', ['ship_type_id','type_name','description'])
bulk_insert(country_df, 'dim_country', ['country_id','country_name','iso_code','region'])
bulk_insert(port_df, 'dim_port', ['port_id','port_name','country_id','latitude','longitude'])
bulk_insert(ship_df, 'dim_ship', ['ship_id','ship_name','imo_number','mmsi','call_sign','length','draft','gross_tonnage','ship_type_id'])
bulk_insert(cargo_type_df, 'dim_cargo_type', ['cargo_type_id','cargo_name','cargo_detailed_name','hazardous'])
bulk_insert(visit_df, 'fact_visit', ['visit_id','ship_id','port_id','ETA','ATA','ETD','ATD','status','cargo_type_id'])

conn.commit()
cur.close()
conn.close()

print("Podatki so vstavljeni v tabele!")