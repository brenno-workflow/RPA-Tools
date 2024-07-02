use vincibot_db;

create table if not exists db_subprocess (
id int not null auto_increment,
name varchar (45) not null,
subporcess varchar (45) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table db_subprocess;

insert into db_subprocess values 
(default, 'site', 'site', default, default),
(default, 'sistema', 'sistema', default, default),
(default, 'pasta', 'pasta', default, default),
(default, 'arquivo', 'arquivo', default, default),
(default, 'pagamento', 'pagamento', default, default),
(default, 'recebimento', 'recebimento', default, default),
(default, 'extrato', 'extrato', default, default),
(default, 'contrato', 'contrato', default, default);

INSERT INTO db_subprocess (name) VALUES ('sid');

update db_subprocess set diretorio = 'Desktop' where id = 1;

select * from db_subprocess;