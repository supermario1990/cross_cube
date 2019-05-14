/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2019/5/13 17:04:28                           */
/*==============================================================*/


drop table if exists cubes;

drop table if exists data_set;

drop table if exists datasource;

/*==============================================================*/
/* Table: cubes                                                 */
/*==============================================================*/
create table cubes
(
   id                   integer(64) not null comment '������ID',
   uuid                 varbinary(128) comment '������uuid',
   name                 varchar(128) comment '����������',
   name_alias           varchar(128) comment '���������',
   cube            		blob comment '������',
   extends              blob comment '��չ�ֶ�',
   primary key (id)
);
ALTER TABLE cubes MODIFY id  INTEGER(64) AUTO_INCREMENT;

alter table cubes comment '�������';

/*==============================================================*/
/* Table: data_set                                              */
/*==============================================================*/
create table data_set
(
   id                   integer(64) not null comment '���ݼ�ID',
   name                 varchar(128) comment '���ݼ�����',
   cube_uuid            varchar(128) comment '������uuid',
   primary key (id)
);
ALTER TABLE data_set MODIFY id  INTEGER(64) AUTO_INCREMENT;

alter table data_set comment '���ݼ�';

/*==============================================================*/
/* Table: datasource                                            */
/*==============================================================*/
create table datasource
(
   id                   integer(64) not null comment '����ԴID',
   name                 varchar(128) comment '����Դ����',
   type                 varchar(64) comment '����Դ����',
   config               varchar(4096) comment '����Դ����',
   test_sql             varchar(512) comment '��ͨ�Բ����ַ���',
   modi_time            timestamp comment '�޸�ʱ��',
   primary key (id)
);
ALTER TABLE datasource MODIFY id  INTEGER(64) AUTO_INCREMENT;

alter table datasource comment '����Դ';

