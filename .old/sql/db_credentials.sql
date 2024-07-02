use vincibot_db;

create table if not exists db_credentials (
id int not null auto_increment,
name varchar (45) not null,
login varchar (45) not null,
password varchar (45) not null,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table db_credentials;db_mail

insert into db_credentials values 
(default, 'fsist', 'cataguasist', 'c3LM6SD1Z6@9jFOy', default, default),
(default, 'sienge', 'leonardo.vinci', 'BI.ctg20241', default, default),
(default, 'sid', 'leonardo.vinci@catagua.com.br', 'BI.ctg2024', default, default),
(default, 'mail', 'leonardo.vinci@catagua.com.br', 'BI.ctg2024', default, default),
(default, 'simpliss_piracicaba', '55.928.014/0001-61', 'b1daa6', default, default),
(default, 'simpliss_piracicaba', '03.581.798/0001-09', '~G0yJr%|', default, default),
(default, 'simpliss_piracicaba', '23.109.294/0001-90', 'NG)f$Q', default, default),
(default, 'simpliss_piracicaba', '23.757.526/0001-16', 'F@H=qz', default, default),
(default, 'simpliss_piracicaba', '25.402.722/0001-01', '}WG)aR', default, default),
(default, 'simpliss_piracicaba', '28.091.803/0001-18', '0M@]Vx', default, default),
(default, 'simpliss_piracicaba', '28.738.726/0001-45', 'kjZyGg', default, default),
(default, 'simpliss_piracicaba', '32.616.910/0001-90', '%xZi\,o1', default, default),
(default, 'simpliss_piracicaba', '35.703.367/0001-56', 'R:FN{(', default, default),
(default, 'simpliss_piracicaba', '35.699.599/0001-88', 'jK2/o!', default, default),
(default, 'simpliss_piracicaba', '36.736.051/0001-23', 'iez.Ak', default, default),
(default, 'simpliss_piracicaba', '36.736.079/0001-60', 'wy2]cV', default, default),
(default, 'simpliss_piracicaba', '36.944.839/0001-25', 'Qv5$/z0I', default, default),
(default, 'simpliss_piracicaba', '36.738.989/0001-82', 'NfJebB', default, default),
(default, 'simpliss_piracicaba', '36.738.973/0001-70', '~a|r!52E', default, default),
(default, 'simpliss_piracicaba', '40.059.848/0001-00', 'uGCY2R', default, default),
(default, 'simpliss_piracicaba', '40.059.860/0001-15', '6|(BS', default, default),
(default, 'simpliss_piracicaba', '40.059.878/0001-17', '^:Te1/', default, default),
(default, 'simpliss_piracicaba', '40.059.890/0001-21', 'ZoL6e', default, default),
(default, 'simpliss_piracicaba', '40.059.904/0001-07', 'n^5!O)', default, default),
(default, 'simpliss_piracicaba', '40.061.926/0001-01', 'q@@wMf', default, default),
(default, 'simpliss_piracicaba', '40.061.941/0001-50', '@-U^fx', default, default),
(default, 'simpliss_piracicaba', '40.061.907/0001-85', 'u2pN?3', default, default),
(default, 'simpliss_piracicaba', '40.061.894/0001-44', ')}7VHS', default, default),
(default, 'simpliss_piracicaba', '40.061.919/0001-00', 'e&lc_f', default, default),
(default, 'simpliss_piracicaba', '42.569.273/0001-00', 'Y9oH8L', default, default),
(default, 'simpliss_piracicaba', '42.548.245/0001-06', '2zB|($', default, default),
(default, 'simpliss_piracicaba', '42.548.491/0001-50', '|oKq!?', default, default),
(default, 'simpliss_piracicaba', '42.552.274/0001-33', '/Uk_>n', default, default),
(default, 'simpliss_piracicaba', '42.552.298/0001-92', 't>Kw)N', default, default),
(default, 'simpliss_piracicaba', '42.552.137/0001-07', 'kB6wAc', default, default),
(default, 'simpliss_piracicaba', '42.552.233/0001-47', 'G[QK:!{l', default, default),
(default, 'simpliss_piracicaba', '42.552.096/0001-40', 'kWVir!', default, default),
(default, 'simpliss_piracicaba', '42.552.210/0001-32', ']Xd.zL', default, default),
(default, 'simpliss_piracicaba', '42.552.161/0001-38', 'domrS&', default, default),
(default, 'simpliss_piracicaba', '45.352.370/0001-26', 'c)et!M', default, default),
(default, 'simpliss_piracicaba', '46.638.018/0001-14', 'PB&gym', default, default),
(default, 'simpliss_piracicaba', '46.637.764/0001-93', 'mDJU/2', default, default),
(default, 'simpliss_piracicaba', '46.637.984/0001-17', 'NxfOg%', default, default),
(default, 'simpliss_piracicaba', '46.637.970/0001-01', 'N%5EOD', default, default),
(default, 'simpliss_piracicaba', '46.637.595/0001-91', 'P?6LFO', default, default),
(default, 'simpliss_piracicaba', '46.637.704/0001-70', 'I37n!j', default, default),
(default, 'simpliss_piracicaba', '46.637.859/0001-07', 'RF[l{L', default, default),
(default, 'simpliss_piracicaba', '46.637.744/0001-12', 'gfVy[l', default, default);

INSERT INTO db_credentials (name, login, password) VALUES ('mail', 'leonardo.vinci@catagua.com.br', 'BI.ctg2024');

update db_credentials set diretorio = 'Desktop' where id = 1;

select * from db_credentials;