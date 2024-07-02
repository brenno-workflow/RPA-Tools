use vincibot_db;

create table if not exists db_webaccess (
id int not null auto_increment,
name varchar (45) not null,
db_sites_id int,
db_credentials_id int,
db_status_id int,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id),
foreign key (db_sites_id) references db_sites(id),
foreign key (db_credentials_id) references db_credentials(id),
foreign key (db_status_id) references db_status(id)
) default charset = utf8mb4;

drop table db_webaccess;

insert into db_webaccess values 
(default, 'fsist', 1, 1, 1, default, default),
(default, 'sienge', 2, 2, 1, default, default),
(default, 'sid', 3, 3, 1, default, default),
(default, 'sid_cliente', 4, null, 1, default, default),
(default, 'sid_cliente_workflow', 5, null, 1, default, default);

INSERT INTO db_webaccess (name, db_sites_id) VALUES ('sid_cliente_workflow', 5);

update db_webaccess set diretorio = 'Desktop' where id = 1;

alter table db_webaccess add foreign key (id_subprocess) references subprocess(id);

describe db_webaccess;

select * from db_webaccess;