use vincibot_db;

create table if not exists db_fluxosweb (
id int not null auto_increment,
name varchar (45) not null,
db_fluxos_id int,
db_sites_id int,
db_credentials_id int,
db_status_id int,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id),
foreign key (db_fluxos_id) references db_fluxos(id),
foreign key (db_sites_id) references db_sites(id),
foreign key (db_credentials_id) references db_credentials(id),
foreign key (db_status_id) references db_status(id)
) default charset = utf8mb4;

drop table db_fluxosweb;

insert into db_fluxosweb values 
(default, 'fsist', 1, 1, 1, 1, default, default),
(default, 'sienge', 2, 2, 2, 1, default, default),
(default, 'sid', 3, 3, 3, 1, default, default),
(default, 'sid_cliente', 4, 4, null, 1, default, default),
(default, 'sid_cliente_worflow', 5, 5, null, 1, default, default),
(default, 'simpliss_piracicaba_issqn', 30, 7, null, 1, default, default),
(default, 'simpliss_piracicaba_registro_tomador', 31, 8, null, 1, default, default);

insert into db_fluxosweb values 
(default, 'simpliss_piracicaba', 5, 5, null, 1, default, default),
(default, 'simpliss_piracicaba_registro_tomador', 5, 5, null, 1, default, default);

update db_fluxosweb set diretorio = 'Desktop' where id = 1;

select * from db_fluxosweb;