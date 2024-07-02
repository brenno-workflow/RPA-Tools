use vincibot_db;

create table if not exists sid_cliente_anexos (
id int not null auto_increment,
name varchar (45) not null,
anexo varchar (45) not null,
value int,
created_at timestamp default current_timestamp,
updated_at timestamp default current_timestamp on update current_timestamp,
primary key (id)
) default charset = utf8mb4;

drop table sid_cliente_anexos;

insert into sid_cliente_anexos values 
(default, 'comprovante_pagamento_itbi_registro', 'Comprovante de pagamento ITBI e registro', null, default, default),
(default, 'contrato_personalizacao', 'Contrato de personalização', null, default, default),
(default, 'acordo_judicial', 'Acordo judicial', 12, default, default),
(default, 'aditivo_contratual', 'Aditivo contratual', 13, default, default),
(default, 'confissao_dividas', 'Confissão de Dívidas', 5, default, default),
(default, 'contrato_caixa', 'Contrato Caixa', 6, default, default),
(default, 'contrato_compra_venda', 'Contrato de compra e venda', 2, default, default),
(default, 'escritura_definitiva', 'Escritura Definitiva - Alienação - Matrícula', 7, default, default),
(default, 'escritura_definitiva', 'Escritura Definitiva', 7, default, default),
(default, 'escritura_definitiva', 'Alienação', 7, default, default),
(default, 'escritura_definitiva', 'Matrícula', 7, default, default),
(default, 'informe_rendimentos', 'Informe de rendimentos', 14, default, default),
(default, 'notificacao_extra_judicial', 'Notificação extra judicial', 15, default, default),
(default, 'pesquisa_nps', 'Pesquisa NPS', 16, default, default),
(default, 'procuracao', 'Procuração', 21, default, default),
(default, 'proposta_compra_venda', 'Proposta de compra e venda', 1, default, default),
(default, 'protocolos', 'Protocolos', 3, default, default),
(default, 'recibo_troco_itbi', 'Recibo de troco ITBI', 17, default, default),
(default, 'termo_distrato', 'Termo de distrato', 18, default, default),
(default, 'termo_entrega_chaves', 'Termo de entrega de chaves', 8, default, default),
(default, 'termo_quitacao', 'Termo de quitação', 19, default, default),
(default, 'termo_vistoria', 'Termo de vistoria', 20, default, default);

INSERT INTO sid_cliente_anexos (name, url) VALUES ('sid_cliente_workflow', 'https://sid.catagua.com.br/cliente/workflow.php');

ALTER TABLE sid_cliente_anexos CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

update sid_cliente_anexos set diretorio = 'Desktop' where id = 1;

select * from sid_cliente_anexos;