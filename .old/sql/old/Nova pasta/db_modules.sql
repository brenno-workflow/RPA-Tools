create database vincibot_db;

use vincibot_db;

create table if not exists db_modules (
id int not null auto_increment,
name varchar (45) not null,
module varchar (45) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table db_modules;

insert into db_modules values 
(default, 'ecossistemanf', 'ecossistemanf', default, default),
(default, 'conciliacao', 'conciliacao', default, default),
(default, 'cliente', 'cliente', default, default);

INSERT INTO db_modules (name) VALUES ('sid');

update db_modules set name = 'clientes' where id = 3;

select * from db_modules;
