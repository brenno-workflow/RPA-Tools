use vincibot_db;

create table if not exists db_services (
id int not null auto_increment,
name varchar (45) not null,
service varchar (45) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table db_services;

insert into db_services values 
(default, 'fsist', 'fsist', default, default),
(default, 'sienge', 'sienge', default, default),
(default, 'sid', 'sid', default, default);

INSERT INTO db_services (name, service) VALUES ('control', 'control');

update db_services set name = 'sid' where id = 3;

select * from db_services;