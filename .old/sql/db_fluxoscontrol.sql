use vincibot_db;

create table if not exists db_fluxoscontrol (
id int not null auto_increment,
name varchar (45) not null,
db_fluxos_id int,
db_control_id int,
db_status_id int,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id),
foreign key (db_fluxos_id) references db_fluxos(id),
foreign key (db_control_id) references db_control(id),
foreign key (db_status_id) references db_status(id)
) default charset = utf8mb4;

drop table db_fluxoscontrol;

insert into db_fluxoscontrol values 
(default, 'control', 9, 1, 1, default, default),
(default, 'control_sid', 10, 2, 1, default, default),
(default, 'control_sid_cliente', 11, 3, 1, default, default),
(default, 'control_sid_cliente_sucesso', 12, 4, 1, default, default),
(default, 'control_sid_cliente_falha', 13, 5, 1, default, default),
(default, 'control_sid_cliente_erro', 14, 6, 1, default, default),
(default, 'control_simpliss', 21, 7, 1, default, default),
(default, 'control_simpliss_piracicaba', 22, 8, 1, default, default),
(default, 'control_simpliss_piracicaba_sucesso', 23, 9, 1, default, default),
(default, 'control_simpliss_piracicaba_falha', 24, 10, 1, default, default),
(default, 'control_simpliss_piracicaba_erro', 25, 11, 1, default, default),
(default, 'control_simpliss_piracicaba_download', 26, 12, 1, default, default);

INSERT INTO db_fluxoscontrol values
(default, 'control_simpliss', 21, 7, 1, default, default),
(default, 'control_simpliss_piracicaba', 22, 8, 1, default, default),
(default, 'control_simpliss_piracicaba_sucesso', 23, 9, 1, default, default),
(default, 'control_simpliss_piracicaba_falha', 24, 10, 1, default, default),
(default, 'control_simpliss_piracicaba_erro', 25, 11, 1, default, default),
(default, 'control_simpliss_piracicaba_download', 26, 12, 1, default, default);

update db_fluxoscontrol set db_servers_id = 4 where id = 3;

alter table db_fluxoscontrol add foreign key (id_subprocess) references subprocess(id);

select * from db_fluxoscontrol;