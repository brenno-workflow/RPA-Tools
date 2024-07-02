use vincibot_db;

create table if not exists database_process (
id int not null auto_increment,
name varchar (45) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table database_process;

insert into database_process values 
(default, 'login', default, default),
(default, 'download', default, default),
(default, 'leitura', default, default),
(default, 'importacao', default, default);

INSERT INTO database_modules (name) VALUES ('sid');

update database_process set diretorio = 'Desktop' where id = 1;

select * from database_process;