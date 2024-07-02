use vincibot_db;

create table if not exists db_user (
id int not null auto_increment,
name varchar (45) not null,
user varchar (300) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table db_user;

insert into db_user values 
(default, 'leonardo.vinci', 'leonardo.vinci', default, default),
(default, 'brenno.brossi', 'brenno.brossi', default, default);

INSERT INTO db_user (name, url) VALUES ('sid_cliente_workflow', 'https://sid.catagua.com.br/cliente/workflow.php');

update db_user set url = 'http://onbasehomolog.catagua.com.br/' where id = 3;

select * from db_user;