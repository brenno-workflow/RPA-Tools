use vincibot_db;

create table if not exists db_fluxos (
id int not null auto_increment,
name varchar (45) not null,
db_process_id int,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id),
foreign key (db_process_id) references db_process(id)
) default charset = utf8mb4;

drop table db_fluxos;

insert into db_fluxos values 
(default, 'web_fsist_login', 1, default, default),
(default, 'web_sienge_login', 1, default, default),
(default, 'web_sid_login', 1, default, default),
(default, 'web_sid_cliente', 1, default, default),
(default, 'web_sid_cliente_workflow', 1, default, default),
(default, 'server_ecossistemanf', 2, default, default),
(default, 'server_sid_cliente', 2, default, default),
(default, 'server_sid_cliente_anexos', 2, default, default),
(default, 'control', 3, default, default),
(default, 'control_sid', 3, default, default),
(default, 'control_sid_cliente', 3, default, default),
(default, 'control_sid_cliente_sucesso', 3, default, default),
(default, 'control_sid_cliente_falha', 3, default, default),
(default, 'control_sid_cliente_erro', 3, default, default),
(default, 'mail', 4, default, default),
(default, 'mail_repositorio', 4, default, default),
(default, 'mail_sid_cliente_anexos_sucesso', 4, default, default),
(default, 'mail_sid_cliente_anexos_falha', 4, default, default),
(default, 'mail_sid_cliente_anexos_erro', 4, default, default),
(default, 'web_simpliss_piracicaba_login', 1, default, default),
(default, 'control_simpliss', 3, default, default),
(default, 'control_simpliss_piracicaba', 3, default, default),
(default, 'control_simpliss_piracicaba_sucesso', 3, default, default),
(default, 'control_simpliss_piracicaba_falha', 3, default, default),
(default, 'control_simpliss_piracicaba_erro', 3, default, default),
(default, 'control_simpliss_piracicaba_download', 3, default, default),
(default, 'mail_simpliss_piracicaba_sucesso', 4, default, default),
(default, 'mail_simpliss_piracicabas_falha', 4, default, default),
(default, 'mail_simpliss_piracicaba_erro', 4, default, default),
(default, 'web_simpliss_piracicaba_issqn', 4, default, default),
(default, 'web_simpliss_piracicaba_registro_tomador', 4, default, default);

insert into db_fluxos values
(default, 'web_simpliss_piracicaba_registro_tomador', 4, default, default);

update db_fluxos set name = 'web_simpliss_piracicaba_issqn' where id = 30;

DELETE FROM db_fluxos WHERE id = 8;

select * from db_fluxos;