use vincibot_db;

create table if not exists db_fluxos (
id int not null auto_increment,
name varchar (45) not null,
db_services_id int,
db_modules_id int,
db_process_id int,
db_subprocess_id int,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id),
foreign key (db_services_id) references db_services(id),
foreign key (db_modules_id) references db_modules(id),
foreign key (db_process_id) references db_process(id),
foreign key (db_subprocess_id) references db_subprocess(id)
) default charset = utf8mb4;

drop table db_fluxos;

insert into db_fluxos values 
(default, 'web_fsist_login', 1, 1, 1, 1, default, default),
(default, 'web_sienge_login', 2, 2, 1, 1, default, default),
(default, 'web_sid_login', 3, 3, 1, 1, default, default),
(default, 'web_sid_cliente', 3, 3, 3, 1, default, default),
(default, 'web_sid_cliente_workflow', 3, 3, 5, 8, default, default),
(default, 'server_ecossistemanf', 1, 1, 6, 3, default, default),
(default, 'server_sid_cliente', 3, 3, 6, 3, default, default),
(default, 'server_sid_cliente_anexos', 3, 3, 6, 3, default, default),
(default, 'control', 4, null, null, null, default, default),
(default, 'control_sid', 3, 3, null, null, default, default),
(default, 'control_sid_cliente', 3, 3, null, null, default, default),
(default, 'control_sid_cliente_sucesso', 3, 3, 7, null, default, default),
(default, 'control_sid_cliente_falha', 3, 3, 8, null, default, default),
(default, 'control_sid_cliente_erro', 3, 3, 9, null, default, default);

INSERT INTO db_fluxos (name, db_services_id, db_modules_id, db_process_id, db_subprocess_id) VALUES ('control_sid_cliente_erro', 3, 3, 9, null);

update db_fluxos set name = 'control' where id = 9;

DELETE FROM db_fluxos WHERE id = 8;

select * from db_fluxos;