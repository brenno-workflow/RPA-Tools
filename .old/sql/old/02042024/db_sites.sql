use vincibot_db;

create table if not exists db_sites (
id int not null auto_increment,
name varchar (45) not null,
url varchar (300) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table db_sites;

insert into db_sites values 
(default, 'fsist', 'https://www.fsist.com.br/', default, default),
(default, 'sienge', 'https://catagua.sienge.com.br/sienge/8/index.html#/', default, default),
(default, 'sid', 'https://sid.catagua.com.br/', default, default),
(default, 'sid_cliente', 'https://sid.catagua.com.br/cliente/index.php', default, default),
(default, 'sid_cliente_workflow', 'https://sid.catagua.com.br/cliente/workflow.php', default, default),
(default, 'simpliss_piracicaba', 'https://piracicaba.simplissweb.com.br/contrib/Home/Index/1', default, default);

INSERT INTO db_sites (name, url) VALUES ('simpliss_piracicaba', 'https://piracicaba.simplissweb.com.br/contrib/Home/Index/1');

update db_sites set url = 'http://onbasehomolog.catagua.com.br/cliente/buscar_codigo.php' where id = 5;

select * from db_sites;