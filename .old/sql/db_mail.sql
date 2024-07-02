use vincibot_db;

create table if not exists db_mail (
id int not null auto_increment,
name varchar (45) not null,
mail varchar (300) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table db_mail;

insert into db_mail values 
(default, 'repositorio.rpa', 'repositorio.rpa@catagua.com.br', default, default),
(default, 'leonardo.vinci', 'leonardo.vinci@catagua.com.br', default, default),
(default, 'brenno.brossi', 'brenno.brossi@catagua.com.br', default, default),
(default, 'rpa.sid.cliente.workflow.anexos', 'rpa.sid.cliente.workflow.anexos@catagua.com.br', default, default),
(default, 'rpa.simpliss.piracicaba.nfs', 'rpa.simpliss.piracicaba.nfs@catagua.com.br', default, default),
(default, 'rpa.sienge.conciliacao', 'rpa.sienge.conciliacao@catagua.com.br', default, default);

INSERT INTO db_mail VALUES
(default, 'rpa.sienge.conciliacao', 'rpa.sienge.conciliacao@catagua.com.br', default, default);

update db_mail set url = 'http://onbasehomolog.catagua.com.br/' where id = 3;

select * from db_mail;