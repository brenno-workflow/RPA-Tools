use vincibot_db;

create table if not exists db_fluxossid_cliente_anexos (
id int not null auto_increment,
name varchar (45) not null,
db_fluxos_id int,
db_sid_cliente_anexos_id int,
db_status_id int,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id),
foreign key (db_fluxos_id) references db_fluxos(id),
foreign key (db_sid_cliente_anexos_id) references db_sid_cliente_anexos(id),
foreign key (db_status_id) references db_status(id)
) default charset = utf8mb4;

drop table db_fluxossid_cliente_anexos;

insert into db_fluxossid_cliente_anexos values 
(default, 'sid_cliente_anexos', 8, 3, 1, default, default);

INSERT INTO db_fluxossid_cliente_anexos (name, db_sites_id) VALUES ('sid_cliente_workflow', 5);

update db_fluxossid_cliente_anexos set diretorio = 'Desktop' where id = 1;

alter table db_fluxossid_cliente_anexos add foreign key (id_subprocess) references subprocess(id);

select * from db_fluxossid_cliente_anexos;