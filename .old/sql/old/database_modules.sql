create database vincibot_db;

use vincibot_db;

create table if not exists Database_Modules (
id int not null auto_increment,
name varchar (45) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table Database_Modules;

insert into Database_Modules values 
(default, 'ecossistemanf', default, default),
(default, 'conciliacao', default, default),
(default, 'clientes', default, default);

INSERT INTO Database_Modules (name) VALUES ('sid');

update Database_Modules set name = 'clientes' where id = 3;

select * from Database_Modules;
