-- sudo -i -u postgres
-- psql
create database management;
-- \l #list of db's
-- \c management #connect to db

CREATE TABLE IF NOT EXISTS users (
            id bigint not null PRIMARY KEY,
            username varchar(33) default NULL,
            jointime timestamp without time zone default CURRENT_TIMESTAMP(1)
);

CREATE TABLE IF NOT EXISTS reports (
            id serial PRIMARY KEY,
            report_date date default CURRENT_DATE,
            actions json default '[]'
);

CREATE TABLE IF NOT EXISTS user_report (
    user_id INT,
    report_id INT,
    PRIMARY KEY (user_id, report_id),
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES users(id),
    CONSTRAINT fk_report FOREIGN KEY(report_id) REFERENCES reports(id)
);

createuser -P management_app

grant all on reports to management_app;
grant all on reports_id_seq to management_app;
grant all on users to management_app;
grant all on user_report to management_app;
grant all on users_id_seq to management_app;




