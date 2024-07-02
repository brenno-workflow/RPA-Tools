use vincibot_db;

create table if not exists database_fluxosweb (
id int not null auto_increment,
name varchar (45) not null,
database_fluxos_id int,
database_sites_id int,
database_credentials_id int,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id),
foreign key (database_fluxos_id) references database_fluxos(id),
foreign key (database_sites_id) references database_sites(id),
foreign key (database_credentials_id) references database_credentials(id)
) default charset = utf8mb4;

drop table database_fluxosweb;

insert into database_fluxosweb values 
(default, 'fsist', 1, 1, 1, default, default),
(default, 'sienge', 2, 2, 2, default, default),
(default, 'sid', 3, 3, 3, default, default);

update database_fluxosweb set diretorio = 'Desktop' where id = 1;

alter table database_fluxosweb
add foreign key (id_subprocess)
references subprocess(id);

describe database_fluxosweb;

select * from database_fluxosweb;