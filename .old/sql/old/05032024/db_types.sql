use vincibot_db;

create table if not exists type (
id_type int not null auto_increment,
name varchar (45),
dt_created timestamp default current_timestamp,
dt_modified timestamp default current_timestamp on update current_timestamp,
primary key (id_type)
) default charset = utf8mb4;

drop table type;

insert into type values 
(default, 'download', default, default),
(default, 'upload', default, default);

update type set diretorio = 'Desktop' where id = 1;

select * from type;