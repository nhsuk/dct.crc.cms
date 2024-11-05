SELECT tablename AS "table"
FROM pg_tables
WHERE schemaname = lower('public')
ORDER BY tablename;

SELECT viewname AS "view"
FROM pg_views
WHERE schemaname = lower('public')
ORDER BY viewname;

SELECT sequence_name AS "sequence"
FROM information_schema.sequences
WHERE sequence_schema = lower('public')
ORDER BY sequence_name;

SELECT conname AS "constraint"
FROM pg_constraint c
JOIN pg_namespace n ON n.oid = c.connamespace
WHERE contype IN ('p') AND n.nspname = lower('public')
ORDER BY conname;

DO $$
DECLARE
    r RECORD;
    v_sql TEXT;
    v_hash TEXT;
BEGIN
    -- Loop through each table in the list
    FOR r IN (SELECT table_schema, table_name
              FROM information_schema.tables
              WHERE table_schema = 'public'
              AND table_name != 'wagtailsearch_indexentry' -- this table will always be out of sync
              AND table_type = 'BASE TABLE' ORDER BY table_name)
    LOOP
        -- Dynamically build the SQL query for each table
        v_sql := format('
            WITH row_hashes AS (
                SELECT md5(row_to_json(t)::text) AS row_hash
                FROM %I.%I t
            )
            SELECT md5(string_agg(row_hash, '''')) AS table_hash
            FROM row_hashes;',
            r.table_schema, r.table_name);

        -- Execute the dynamic SQL and store the result in v_hash
        EXECUTE v_sql INTO v_hash;

        -- Display the result
        RAISE NOTICE 'Table: %, Hash: %', r.table_name, v_hash;
    END LOOP;
END $$;
