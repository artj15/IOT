-- migrate:up


CREATE TYPE data_status_enum AS ENUM ('add', 'pending', 'done');

CREATE TABLE data (
    id BIGSERIAL PRIMARY KEY,
    filename TEXT UNIQUE,
    data_path TEXT,
    status data_status_enum DEFAULT 'add',
    summ double precision DEFAULT NULL,
    ctime TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT (NOW() at time zone 'utc'),
    atime TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL,
    dtime TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL
);

CREATE UNIQUE INDEX data_file_name on data(filename);
CREATE INDEX data_file_name_status on data(filename, status);

INSERT INTO data(filename, data_path, status) VALUES
    ('data.csv', './data/data.csv', 'add');


-- migrate:down


DROP TABLE data CASCADE;
