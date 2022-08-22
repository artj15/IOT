--migrate:up


INSERT INTO data(filename, data_path, status) VALUES
    ('data_1.csv', './data/data_1.csv', 'add');
INSERT INTO data(filename, data_path, status) VALUES
    ('data_2.csv', './data/data_2.csv', 'add');
INSERT INTO data(filename, data_path, status) VALUES
    ('data_3.csv', './data/data_1.csv', 'add');


-- migrate:down


TRUNCATE data CASCADE;
