use vincibot_db;

create table if not exists db_servers (
id int not null auto_increment,
name varchar (45) not null,
path varchar (300) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table db_servers;

insert into db_servers values 
(default, 'ecossistemanf', '//192.168.125.30//ecossistemanf', default, default),
(default, 'sid', 'C://Users//brossi.brenno//Desktop//SID', default, default),
(default, 'sid_cliente', 'C://Users//brossi.brenno//Desktop//SID//Cliente', default, default),
(default, 'sid_cliente_anexos', 'C://Users//brossi.brenno//Desktop//SID//Cliente//Anexos', default, default);

INSERT INTO db_servers (name, path) VALUES ('sid_cliente_anexos', 'C://Users//brossi.brenno//Desktop//SID//Cliente//Anexos');

update db_servers set path = 'C:\\Users\\brossi.brenno\\Desktop\\SID\\Cliente\\Anexos' where id = 4;

select * from db_servers;