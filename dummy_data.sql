-- Create a dummy user (password is 'password')
INSERT INTO users (email, name, institution, hashed_password, created_at, updated_at)
VALUES ('admin@example.com', 'Admin User', 'SESAME Institute', '$2b$12$1xxxxxxxxxxxxxxxxxxxxuZLbwlOAVXsNdFE/KxPcUEZcgKUPDO', NOW(), NOW());

-- Create some balancing authorities
INSERT INTO balancing_authorities (code, name)
VALUES 
  ('CAISO', 'California Independent System Operator'),
  ('NYISO', 'New York Independent System Operator'),
  ('PJM', 'PJM Interconnection'),
  ('ERCOT', 'Electric Reliability Council of Texas'),
  ('MISO', 'Midcontinent Independent System Operator');

-- Create some utilities
INSERT INTO utilities (utlsrvid, name)
VALUES 
  ('UTIL001', 'Pacific Gas & Electric'),
  ('UTIL002', 'Southern California Edison'),
  ('UTIL003', 'Duke Energy'),
  ('UTIL004', 'Exelon'),
  ('UTIL005', 'NextEra Energy');

-- Create some plants
INSERT INTO plants (utility_id, balancing_authority_id, orispl, state, name, nerc_region, subregion_acronym, subregion_name, isorto, county_name, latitude, longitude, num_units, num_generators, primary_fuel, nameplate_capacity, power_to_heat_ratio)
VALUES 
  (1, 1, '12345', 'CA', 'Diablo Canyon', 'WECC', 'CAMX', 'California', 'CAISO', 'San Luis Obispo', 35.2108, -120.8561, 2, 2, 'NUC', 2256, 0.33),
  (2, 1, '23456', 'CA', 'San Onofre', 'WECC', 'CAMX', 'California', 'CAISO', 'San Diego', 33.3689, -117.5551, 3, 3, 'NUC', 2150, 0.33),
  (3, 3, '34567', 'PA', 'Three Mile Island', 'RFC', 'RFCE', 'RFC East', 'PJM', 'Dauphin', 40.1531, -76.7248, 1, 1, 'NUC', 819, 0.33),
  (4, 2, '45678', 'NY', 'Indian Point', 'NPCC', 'NYCW', 'NYC/Westchester', 'NYISO', 'Westchester', 41.2697, -73.9522, 2, 2, 'NUC', 2060, 0.33),
  (5, 4, '56789', 'TX', 'South Texas Project', 'TRE', 'ERCT', 'ERCOT', 'ERCOT', 'Matagorda', 28.7964, -96.0489, 2, 2, 'NUC', 2708, 0.33);

-- Create some egrid data
INSERT INTO egrid (year, plant_id, annual_nox_rate, ozone_season_nox_rate, annual_so2_rate, annual_co2_rate, annual_ch4_rate, annual_n2o_rate, annual_co2_equivalent_rate, annual_hg_rate, nominal_heat_rate)
VALUES 
  (2020, 1, 0.01, 0.01, 0.01, 0.1, 0.001, 0.0001, 0.11, 0.00001, 10.5),
  (2020, 2, 0.02, 0.02, 0.02, 0.2, 0.002, 0.0002, 0.22, 0.00002, 10.6),
  (2020, 3, 0.03, 0.03, 0.03, 0.3, 0.003, 0.0003, 0.33, 0.00003, 10.7),
  (2020, 4, 0.04, 0.04, 0.04, 0.4, 0.004, 0.0004, 0.44, 0.00004, 10.8),
  (2020, 5, 0.05, 0.05, 0.05, 0.5, 0.005, 0.0005, 0.55, 0.00005, 10.9);

-- Create some pathway metadata
INSERT INTO pathway_metadata (id, name, description, created_at, updated_at)
VALUES 
  (1, 'Hydrogen Production', 'Pathway for hydrogen production', NOW(), NOW()),
  (2, 'Battery Electric Vehicles', 'Pathway for battery electric vehicles', NOW(), NOW()),
  (3, 'Fuel Cell Electric Vehicles', 'Pathway for fuel cell electric vehicles', NOW(), NOW()),
  (4, 'Solar Power Generation', 'Pathway for solar power generation', NOW(), NOW()),
  (5, 'Wind Power Generation', 'Pathway for wind power generation', NOW(), NOW());

-- Create some pathway versions
INSERT INTO pathway_versions (pathway_id, version, data, created_at, updated_at)
VALUES 
  (1, '1.0', '{"steps": [{"source": "electrolysis", "inputs": {"electricity": 50, "water": 10}}]}', NOW(), NOW()),
  (1, '1.1', '{"steps": [{"source": "electrolysis", "inputs": {"electricity": 45, "water": 9}}]}', NOW(), NOW()),
  (2, '1.0', '{"steps": [{"source": "battery_manufacturing", "inputs": {"electricity": 30, "materials": 20}}]}', NOW(), NOW()),
  (3, '1.0', '{"steps": [{"source": "fuel_cell_manufacturing", "inputs": {"electricity": 40, "materials": 25}}]}', NOW(), NOW()),
  (4, '1.0', '{"steps": [{"source": "solar_panel_manufacturing", "inputs": {"electricity": 20, "materials": 30}}]}', NOW(), NOW());

-- Create grid_unit_genmap table data
CREATE TABLE IF NOT EXISTS grid_unit_genmap (
    "Seqno" INTEGER,
    state CHARACTER VARYING NOT NULL,
    plant_name CHARACTER VARYING,
    orispl integer NOT NULL,
    unit CHARACTER VARYING,
    prime_mover CHARACTER VARYING,
    fuel CHARACTER VARYING,
    online_year CHARACTER VARYING,
    egrid_year INTEGER,
    gen CHARACTER VARYING,
    number_of_boiler INTEGER,
    genstatus CHARACTER VARYING,
    gen_prime_mover CHARACTER VARYING,
    gen_fuel CHARACTER VARYING,
    capacity_mw NUMERIC,
    match_score NUMERIC,
    plant_id NUMERIC
);

INSERT INTO grid_unit_genmap ("Seqno", state, plant_name, orispl, unit, prime_mover, fuel, online_year, egrid_year, gen, number_of_boiler, genstatus, gen_prime_mover, gen_fuel, capacity_mw, match_score, plant_id)
VALUES 
  (1, 'CA', 'Diablo Canyon', 12345, '1', 'ST', 'NUC', '1985', 2020, 'G1', 1, 'OP', 'ST', 'NUC', 1138, 1.0, 1),
  (2, 'CA', 'Diablo Canyon', 12345, '2', 'ST', 'NUC', '1986', 2020, 'G2', 1, 'OP', 'ST', 'NUC', 1118, 1.0, 1),
  (3, 'CA', 'San Onofre', 23456, '1', 'ST', 'NUC', '1968', 2020, 'G1', 1, 'RE', 'ST', 'NUC', 436, 1.0, 2),
  (4, 'CA', 'San Onofre', 23456, '2', 'ST', 'NUC', '1983', 2020, 'G2', 1, 'RE', 'ST', 'NUC', 1070, 1.0, 2),
  (5, 'CA', 'San Onofre', 23456, '3', 'ST', 'NUC', '1984', 2020, 'G3', 1, 'RE', 'ST', 'NUC', 1080, 1.0, 2);

-- Create loading_fraction table
CREATE TABLE IF NOT EXISTS loading_fraction (
    prime_mover CHARACTER VARYING,
    loading_fraction NUMERIC,
    status CHARACTER VARYING,
    type TEXT
);

INSERT INTO loading_fraction (prime_mover, loading_fraction, status, type)
VALUES 
  ('ST', 0.2, 'Minimum', 'Baseload'),
  ('ST', 0.75, 'Intermediate', 'Baseload'),
  ('ST', 0.9, 'Maximum', 'Baseload'),
  ('CT', 0.2, 'Minimum', 'Peaker'),
  ('CT', 0.75, 'Intermediate', 'Peaker'),
  ('CT', 0.9, 'Maximum', 'Peaker'),
  ('CT', 1.0, 'Overload', 'Peaker'),
  ('CC', 0.2, 'Minimum', 'Intermediate'),
  ('CC', 0.75, 'Intermediate', 'Intermediate'),
  ('CC', 0.9, 'Maximum', 'Intermediate'),
  ('CC', 1.0, 'Overload', 'Intermediate');

-- Create some ARP data (simplified)
INSERT INTO arp (timestamp, plant_id, unit, gload, so2_mass, nox_mass, co2_mass, heat_input)
VALUES 
  ('2020-01-01 00:00:00', 1, '1', 1000, 0.1, 0.1, 100, 10000),
  ('2020-01-01 01:00:00', 1, '1', 1050, 0.11, 0.11, 105, 10500),
  ('2020-01-01 02:00:00', 1, '1', 1100, 0.12, 0.12, 110, 11000),
  ('2020-01-01 00:00:00', 1, '2', 950, 0.09, 0.09, 95, 9500),
  ('2020-01-01 01:00:00', 1, '2', 1000, 0.1, 0.1, 100, 10000),
  ('2020-01-01 02:00:00', 1, '2', 1050, 0.11, 0.11, 105, 10500),
  ('2020-01-01 00:00:00', 2, '1', 400, 0.04, 0.04, 40, 4000),
  ('2020-01-01 01:00:00', 2, '1', 420, 0.042, 0.042, 42, 4200),
  ('2020-01-01 02:00:00', 2, '1', 440, 0.044, 0.044, 44, 4400);
