use vincibot_db;

create table if not exists db_control_temp (
id int not null auto_increment,
path varchar (300) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table db_control_temp;

insert into db_control_temp values 
(default, 'fsist', 'https://www.fsist.com.br/', default, default);

INSERT INTO db_control_temp (name, url) VALUES ('sid_cliente_workflow', 'https://sid.catagua.com.br/cliente/workflow.php');

update db_control_temp set url = 'http://onbasehomolog.catagua.com.br/' where id = 3;

select * from db_control_temp;