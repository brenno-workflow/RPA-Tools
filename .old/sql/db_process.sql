use vincibot_db;

create table if not exists db_process (
id int not null auto_increment,
name varchar (45) not null,
process varchar (45) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table db_process;

insert into db_process values 
(default, 'web', 'web', default, default),
(default, 'server', 'server', default, default),
(default, 'control', 'control', default, default),
(default, 'mail', 'mail', default, default);

INSERT INTO db_process (name, process) VALUES ('repositorio', 'repositorio');

update db_process set diretorio = 'Desktop' where id = 1;

select * from db_process;