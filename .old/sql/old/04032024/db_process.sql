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
(default, 'login', 'login', default, default),
(default, 'download', 'download', default, default),
(default, 'browser', 'browser', default, default),
(default, 'open', 'open', default, default),
(default, 'anexo', 'anexo', default, default),
(default, 'localizar', 'localizar', default, default),
(default, 'sucesso', 'sucesso', default, default),
(default, 'falha', 'falha', default, default),
(default, 'erro', 'erro', default, default);

INSERT INTO db_process (name, process) VALUES ('erro', 'erro');

update db_process set diretorio = 'Desktop' where id = 1;

select * from db_process;