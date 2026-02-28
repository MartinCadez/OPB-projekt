import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

df = pd.read_csv("processed_ships.csv")

df['status'] = df['status'].astype(str)

df['ship_id'] = pd.factorize(df['ship_name'])[0] + 1

# --- Country ---
countries_data = [
    (1, "Slovenia", "SI", "Europe"),
    (2, "Italy", "IT", "Europe")
]
countries_table = pd.DataFrame(countries_data, columns=['country_id', 'country_name', 'iso_code', 'region'])

# --- Port ---
ports = {
    'Koper': {'port_id': 1, 'country_id': 1, 'latitude': 45.546, 'longitude': 13.729}
}
random_ports = ['Genoa','Trieste','Ravenna','Venice']
for i, port_name in enumerate(random_ports, start=2):
    ports[port_name] = {
        'port_id': i,
        'country_id': 2,
        'latitude': 44.0 + random.random(),
        'longitude': 12.0 + random.random()
    }

def get_port(status):
    if str(status).lower() <= 'na sidru':
        return ports['Koper']['port_id']
    else:
        return random.choice(list(range(2, len(ports)+1)))

df['port_id'] = df['status'].apply(get_port)

# ---  generiranje ETA/ATA/ETD/ATD ---
def generate_times(date_str):
    try:
        base = datetime.strptime(date_str, "%d.%m.%Y")
    except:
        base = datetime.today()
    eta = base + timedelta(hours=random.randint(0,23), minutes=random.randint(0,59))
    ata = eta + timedelta(hours=random.randint(0,6), minutes=random.randint(0,59))
    etd = ata + timedelta(days=random.randint(1,30), hours=random.randint(0,23), minutes=random.randint(0,59))
    atd = etd + timedelta(hours=random.randint(0,6), minutes=random.randint(0,59))
    return eta, ata, etd, atd

df[['ETA','ATA','ETD','ATD']] = df.apply(lambda row: pd.Series(generate_times(row['date'])), axis=1)

# --- Visit ID ---
df['visit_id'] = range(1, len(df)+1)

# --- Cargo table ---
cargo_data = [
    (1,'IRON ORE', 'Iron Ore Bulk', False),
    (2,'KONTS IMO', 'Container IMO', False),
    (3,'ZIVE ZIVALI', 'Live Animals', False),
    (4,'ZELEZOVA RUDA', 'Iron Ore', False),
    (5,'VOZILA', 'Vehicles', False),
    (6,'JEKLENI KOLUTI', 'Steel Coils', False),
    (7,'ULSD', 'Ultra Low Sulfur Diesel', True),
    (8,'KONT', 'Container Generic', False),
    (9,'PA', 'Palm Oil', True),
    (10,'FERTILIZER', 'Fertilizer', True),
    (11,'POTNIKI', 'Passengers', False),
    (12,'KONTEJNERJI', 'Containers', False),
    (13,'SOYA', 'Soybeans', False),
    (14,'METANOL', 'Methanol', True),
    (15,'G.T. V KONT.', 'General Transport in Container', False),
    (16,'LES', 'Wood Logs', False),
    (17,'WPA', 'Wood Products Assorted', False),
    (18,'KONTS', 'Containers', False),
    (19,'LES V VEZIH', 'Wood Bundles', False),
    (20,'GASOLINE', 'Gasoline', True),
    (21,'VOZILA + RORO', 'Vehicles Ro-Ro', False),
    (22,'PLOCEVINA V KOLUTIH', 'Sheet Steel Coils', False),
    (23,'AVTOMOBILI', 'Cars', False),
    (24,'ULSD 10 PPM', 'Ultra Low Sulfur Diesel 10ppm', True),
    (25,'KRETNICE', 'Switches/Valves', False),
    (26,'VISIT', 'Generic Visit Cargo', False),
    (27,'VOZILA+MAFI TRAILER', 'Vehicles + Trailers', False),
    (28,'SOL', 'Salt', False),
    (29,'JET A1', 'Jet Fuel', True),
    (30,'METHANOL', 'Methanol', True),
    (31,"KONT 20'", '20ft Container', False),
    (32,'NIL', 'None', False),
    (33,'SBM', 'Single Buoy Mooring', False),
    (34,'GT V KONTEJNERJIH', 'General Transport in Containers', False),
    (35,'GAS OIL', 'Gas Oil', True),
    (36,'AVTI MER.', 'Cars Measurement', False),
    (37,'UNLEADED GASOLINE', 'Unleaded Gasoline', True),
    (38,'BORAX ETIBOR - 48', 'Borax ETIBOR', True),
    (39,'FOSFAT', 'Phosphate', False),
    (40,'COILS', 'Steel Coils', False),
    (41,'GENERALNI TOVOR', 'General Cargo', False),
    (42,'ODPADNO ZELEZO', 'Scrap Metal', False),
    (43,'PROJECT CARGO', 'Project Cargo', False),
    (44,'RABLJENA VOZILA', 'Used Vehicles', False),
    (45,'JET', 'Jet Fuel', True),
    (46,'PROJEKTNI TOVOR', 'Project Cargo', False),
    (47,'FOSFATI', 'Phosphates', False),
    (48,'BATERIJE', 'Batteries', True),
    (49,'MOP', 'Misc Oil Products', True),
    (50,'COAL', 'Coal', False),
    (51,'SALT', 'Salt', False),
    (52,'BAUXITE', 'Bauxite', False),
    (53,'UREA', 'Urea', True)
]
cargo_table = pd.DataFrame(cargo_data, columns=['cargo_type_id','cargo_name','cargo_detailed_name','hazardous'])


if 'cargo_type' not in df.columns:
    raise ValueError("Stolpec 'cargo_type' ne obstaja v CSV-ju!")
df['cargo_type_id'] = pd.factorize(df['cargo_type'])[0] + 1

df = df.merge(cargo_table[['cargo_type_id','cargo_name']], how='left', on='cargo_type_id')

# ---  določitev ship_type_id ---
def assign_ship_type(cargo_name):
    bulk = ['IRON ORE', 'ZELEZOVA RUDA', 'COAL', 'BAUXITE']
    container = ['KONTEJNERJI', "KONT 20'", 'KONTS IMO', 'KONTS', 'PA', 'SOYA', 'FERTILIZER', 'GT V KONTEJNERJIH']
    roro = ['VOZILA', 'AVTOMOBILI', 'RABLJENA VOZILA', 'VOZILA + RORO', 'VOZILA+MAFI TRAILER']
    general_cargo = ['PLOCEVINA V KOLUTIH', 'JEKLENI KOLUTI', 'GENERALNI TOVOR', 'COILS', 'LES', 'LES V VEZIH', 'WPA']
    tanker = ['JET A1', 'GASOLINE', 'ULSD', 'ULSD 10 PPM', 'METHANOL', 'METANOL', 'GAS OIL', 'UNLEADED GASOLINE']
    project = ['PROJECT CARGO', 'PROJEKTNI TOVOR']
    if cargo_name in bulk:
        return 1
    elif cargo_name in container:
        return 2
    elif cargo_name in roro:
        return 3
    elif cargo_name in general_cargo:
        return 4
    elif cargo_name in tanker:
        return 5
    elif cargo_name in project:
        return 6
    else:
        return 4

def get_ship_type_id(sid):
    cargo_names = df[df['ship_id']==sid]['cargo_name'].unique()
    if len(cargo_names) == 0:
        return 4
    return assign_ship_type(cargo_names[0])

# --- Ship table ---
ship_table = df[['ship_id','ship_name','ship_code','length','draft','gross_tonnage']].drop_duplicates()
ship_table['ship_type_id'] = ship_table['ship_id'].apply(get_ship_type_id)

# --- generiranje IMO/MMSI/Call Sign ---
def generate_imo_number():
    return random.randint(100000, 999999)
def generate_mmsi():
    return random.randint(100000000, 999999999)
def generate_call_sign():
    letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
    digits = ''.join(random.choices('0123456789', k=1))
    return letters + digits

ship_table['imo_number'] = [generate_imo_number() for _ in range(len(ship_table))]
ship_table['mmsi'] = [generate_mmsi() for _ in range(len(ship_table))]
ship_table['call_sign'] = [generate_call_sign() for _ in range(len(ship_table))]

# --- preuredimo stolpce ---
ship_table = ship_table[['ship_id','ship_name','imo_number','mmsi','call_sign','length','draft','gross_tonnage','ship_type_id']]

# --- Port table with country_id ---
port_table = pd.DataFrame([
    {'port_id': v['port_id'], 'port_name': k, 'country_id': v['country_id'], 
     'latitude': v['latitude'], 'longitude': v['longitude']}
    for k,v in ports.items()
])

# --- Visit ---
visit_table = df[['visit_id','ship_id','port_id','ETA','ATA','ETD','ATD','status','cargo_type_id']]

# --- Ship type ---
ship_types_data = [
    (1, 'Bulk Carrier', 'Heavy cargo'),
    (2, 'Container Ship', 'Container transport'),
    (3, 'Ro-Ro / Car Carrier', 'Vehicle transport'),
    (4, 'General Cargo', 'Mixed cargo'),
    (5, 'Tanker', 'Liquid cargo'),
    (6, 'Project / Heavy Lift', 'Special cargo')
]
ship_type_table = pd.DataFrame(ship_types_data, columns=['ship_type_id','type_name','description'])

# --- Shrani CSV ---
ship_table.to_csv('ship.csv', index=False)
port_table.to_csv('port.csv', index=False)
countries_table.to_csv('country.csv', index=False)
cargo_table.to_csv('cargo_type.csv', index=False)
visit_table.to_csv('visit.csv', index=False)
ship_type_table.to_csv('ship_type.csv', index=False)

print("CSV datoteke so ustvarjene")