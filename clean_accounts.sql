CREATE OR REPLACE TABLE clean_accounts AS
SELECT
    account,
    CASE
        WHEN sector = 'technolgy' THEN 'technology'
        ELSE sector
    END AS sector,
    year_established,
    revenue,
    employees,
    CASE
        WHEN office_location = 'Philipines' THEN 'Philippines'
        ELSE office_location
    END AS office_location,
    subsidiary_of
FROM raw_accounts;