use vincibot_db;

create table if not exists db_fluxosmail (
id int not null auto_increment,
name varchar (45) not null,
db_fluxos_id int,
db_credentials_id int,
db_mail_id int,
db_status_id int,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id),
foreign key (db_fluxos_id) references db_fluxos(id),
foreign key (db_credentials_id) references db_credentials(id),
foreign key (db_mail_id) references db_mail(id),
foreign key (db_status_id) references db_status(id)
) default charset = utf8mb4;

drop table db_fluxosmail;

insert into db_fluxosmail values 
(default, 'mail', 15, 4, 1, 1, default, default),
(default, 'mail_repositorio', 16, 4, 1, 1, default, default),
(default, 'mail_sid_cliente_anexos_sucesso', 17, 4, 3, 1, default, default),
(default, 'mail_sid_cliente_anexos_falha', 18, 4, 3, 1, default, default),
(default, 'mail_sid_cliente_anexos_erro', 19, 4, 3, 1, default, default);

INSERT INTO db_fluxosmail (name, db_sites_id) VALUES ('sid_cliente_workflow', 5);

update db_fluxosmail set db_servers_id = 4 where id = 3;

alter table db_fluxosmail add foreign key (id_subprocess) references subprocess(id);

select * from db_fluxosmail;