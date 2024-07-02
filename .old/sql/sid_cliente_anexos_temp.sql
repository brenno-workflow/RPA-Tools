use vincibot_db;

create table if not exists sid_cliente_anexos_temp (
id int not null auto_increment,
file varchar (45) not null,
folder varchar (45) not null,
path varchar (300) not null,
path_old varchar (300) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table sid_cliente_anexos_temp;

INSERT INTO sid_cliente_anexos_temp (name) VALUES ('clientes');

truncate sid_cliente_anexos_temp;

update sid_cliente_anexos_temp set name = 'sid' where id = 3;

select * from sid_cliente_anexos_temp;