use vincibot_db;

create table if not exists database_subprocess (
id int not null auto_increment,
name varchar (45) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table database_subprocess;

insert into database_subprocess values 
(default, 'pagamento', default, default),
(default, 'recebimento', default, default),
(default, 'extrato', default, default);

INSERT INTO database_modules (name) VALUES ('sid');

update database_subprocess set diretorio = 'Desktop' where id = 1;

select * from database_subprocess;