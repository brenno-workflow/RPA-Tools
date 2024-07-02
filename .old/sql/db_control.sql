use vincibot_db;

create table if not exists db_control (
id int not null auto_increment,
name varchar (45) not null,
path varchar (300) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table db_control;

insert into db_control values 
(default, 'control', 'teste', default, default),
(default, 'control_sid', 'teste', default, default),
(default, 'control_sid_cliente', 'teste', default, default),
(default, 'control_sid_cliente_sucesso', 'teste', default, default),
(default, 'control_sid_cliente_falha', 'teste', default, default),
(default, 'control_sid_cliente_erro', 'teste', default, default),
(default, 'control_simpliss', 'teste', default, default),
(default, 'control_simpliss_piracicaba', 'teste', default, default),
(default, 'control_simpliss_piracicaba_sucesso', 'teste', default, default),
(default, 'control_simpliss_piracicaba_falha', 'teste', default, default),
(default, 'control_simpliss_piracicaba_erro', 'teste', default, default),
(default, 'control_simpliss_piracicaba_download', 'teste', default, default);

INSERT INTO db_control (name, url) VALUES ('sid_cliente_workflow', 'https://sid.catagua.com.br/cliente/workflow.php');

update db_control set url = 'http://onbasehomolog.catagua.com.br/' where id = 3;

select * from db_control;

select * from db_fluxos;