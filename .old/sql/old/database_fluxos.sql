use vincibot_db;

create table if not exists database_fluxos (
id int not null auto_increment,
name varchar (45) not null,
database_modules_id int,
database_services_id int,
database_process_id int,
database_subprocess_id int,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id),
foreign key (database_modules_id) references database_modules(id),
foreign key (database_services_id) references database_services(id),
foreign key (database_process_id) references database_process(id),
foreign key (database_subprocess_id) references database_subprocess(id)
) default charset = utf8mb4;

drop table database_fluxos;

insert into database_fluxos values 
(default, 'fsist', 1, 1, 1, null, default, default),
(default, 'sienge', 2, 2, 1, null, default, default),
(default, 'sid', 3, 3, 1, null, default, default);

update database_fluxos set diretorio = 'Desktop' where id = 1;

alter table database_fluxos
add foreign key (id_subprocess)
references subprocess(id);

describe database_fluxos;

select * from database_fluxos;