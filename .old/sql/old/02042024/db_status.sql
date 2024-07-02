use vincibot_db;

create table if not exists db_status (
id int not null auto_increment,
name varchar (45) not null,
status varchar (45) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table db_status;

insert into db_status values 
(default, 'true', 'true', default, default),
(default, 'false', 'false', default, default);

INSERT INTO db_status (name, url) VALUES ('sid_cliente_workflow', 'https://sid.catagua.com.br/cliente/workflow.php');

update db_status set diretorio = 'Desktop' where id = 1;

select * from db_status;