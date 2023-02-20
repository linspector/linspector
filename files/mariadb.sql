--id;date;time;status;message;monitor;monitor_id;service;enabled;host;hostgroups;job_threshold;raw;
-- https://dba.stackexchange.com/questions/305649/is-a-unique-index-required-for-a-sequential-autoincrementing-id
-- https://stackoverflow.com/questions/289727/which-mysql-data-type-to-use-for-storing-boolean-values
-- https://database.guide/drop-table-if-exists-in-mysql/

DROP TABLE IF EXISTS log;
CREATE TABLE log (
    -- maybe do not use a autoincrement field because of limits. maybe just index more fields. since there is no
    -- relation to other tables a primary key makes no sense.
    id BIGINT UNSIGNED AUTO_INCREMENT, -- maybe this could be the monitor id because they are unique and will not change after restart
    date date, -- current date
    time time, -- current time
    timestamp timestamp, -- execution timestamp returned from the monitor's service (last_execution)
    status VARCHAR(5), -- NONE, OK, ERROR (maybe assign number to the codes for fast database searches?)
    message VARCHAR(255), -- a short message returned by each monitor (max 255?)
    monitor VARCHAR(255),
    monitor_args LONGTEXT, -- kwargs passed to the monitor's service
    monitor_id VARCHAR(64),
    service VARCHAR(255),
    job_id VARCHAR(32),
    enabled TINYINT(1),
    host VARCHAR(255),
    hostgroups VARCHAR(255),
    job_threshold INT(128),
    raw LONGTEXT, -- raw json response data from a monitor's service. maybe write this data to a different database optimized for json object storage and use the monitor_id for relation.
    PRIMARY KEY(id, monitor_id),
    INDEX monitor_id(monitor_id)
);
