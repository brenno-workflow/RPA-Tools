use vincibot_db;

create table if not exists db_fluxosserver (
id int not null auto_increment,
name varchar (45) not null,
db_fluxos_id int,
db_servers_id int,
db_status_id int,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id),
foreign key (db_fluxos_id) references db_fluxos(id),
foreign key (db_servers_id) references db_servers(id),
foreign key (db_status_id) references db_status(id)
) default charset = utf8mb4;

drop table db_fluxosserver;

insert into db_fluxosserver values 
(default, 'ecossistemanf', 6, 1, 1, default, default),
(default, 'sid_cliente', 7, 3, 1, default, default),
(default, 'sid_cliente_anexos', 8, 4, 1, default, default);

INSERT INTO db_fluxosserver (name, db_sites_id) VALUES ('sid_cliente_workflow', 5);

update db_fluxosserver set db_servers_id = 4 where id = 3;

alter table db_fluxosserver add foreign key (id_subprocess) references subprocess(id);

select * from db_fluxosserver;