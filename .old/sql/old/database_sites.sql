use vincibot_db;

create table if not exists database_sites (
id int not null auto_increment,
name varchar (45) not null,
url varchar (300) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table database_sites;

insert into database_sites values 
(default, 'fsist', 'https://www.fsist.com.br/', default, default),
(default, 'sienge', 'https://catagua.sienge.com.br/sienge/8/index.html#/', default, default),
(default, 'sid', 'https://sid.catagua.com.br/', default, default);

INSERT INTO database_modules (name) VALUES ('sid');

update database_sites set diretorio = 'Desktop' where id = 1;

select * from database_sites;