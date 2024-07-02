use vincibot_db;

create table if not exists database_credentials (
id int not null auto_increment,
name varchar (45) not null,
login varchar (45) not null,
password varchar (45) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table database_credentials;

insert into database_credentials values 
(default, 'fsist', 'cataguasist', 'c3LM6SD1Z6@9jFOy', default, default),
(default, 'sienge', 'leonardo.vinci', 'BI.ctg20241', default, default),
(default, 'sid', 'leonardo.vinci@catagua.com.br', 'BI.ctg2024', default, default);

INSERT INTO database_modules (name) VALUES ('sid');

update database_credentials set diretorio = 'Desktop' where id = 1;

select * from database_credentials;