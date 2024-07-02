use vincibot_db;

create table if not exists db_mailmessage (
id int not null auto_increment,
name varchar (45) not null,
mail varchar (300) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table db_mailmessage;

insert into db_mailmessage values 
(default, 'repositorio.rpa', 'repositorio.rpa@catagua.com.br', default, default),
(default, 'leonardo.vinci', 'leonardo.vinci@catagua.com.br', default, default),
(default, 'brenno.brossi', 'brenno.brossi@catagua.com.br', default, default);

INSERT INTO db_mailmessage (name, url) VALUES ('sid_cliente_workflow', 'https://sid.catagua.com.br/cliente/workflow.php');

update db_mailmessage set url = 'http://onbasehomolog.catagua.com.br/' where id = 3;

select * from db_mailmessage;