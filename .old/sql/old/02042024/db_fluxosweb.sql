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
(default, 'sid_cliente_worflow', 5, 5, null, 1, default, default);

insert into db_fluxosweb values 
(default, 'simpliss_piracicaba', 20, 6, 5, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 6, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 7, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 8, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 9, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 10, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 11, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 12, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 13, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 14, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 15, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 16, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 17, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 18, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 19, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 20, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 21, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 22, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 23, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 24, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 25, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 26, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 27, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 28, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 29, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 30, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 31, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 32, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 33, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 34, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 35, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 36, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 37, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 38, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 39, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 40, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 41, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 42, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 43, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 44, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 45, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 46, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 47, 1, default, default),
(default, 'simpliss_piracicaba', 20, 6, 48, 1, default, default);

INSERT INTO db_fluxosweb (name, db_sites_id) VALUES ('sid_cliente_workflow', 5);

update db_fluxosweb set diretorio = 'Desktop' where id = 1;

alter table db_fluxosweb add foreign key (id_subprocess) references subprocess(id);

select * from db_fluxosweb;