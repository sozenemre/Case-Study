CREATE TABLE clans
(
    id uuid DEFAULT uuid_generate_v4() NOT NULL PRIMARY KEY,
    name varchar(255) NOT NULL
    CONSTRAINT unique_clan_name UNIQUE,
    region varchar(10),
    created_at timestamp with time zone DEFAULT NOW()
);

ALTER TABLE clans
    OWNER TO admin;