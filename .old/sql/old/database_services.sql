use vincibot_db;

create table if not exists database_services (
id int not null auto_increment,
name varchar (45) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table database_services;

insert into database_services values 
(default, 'fsist', default, default),
(default, 'sienge', default, default),
(default, 'sid', default, default);

INSERT INTO database_services (name) VALUES ('clientes');

update database_services set name = 'sid' where id = 3;

select * from database_services;