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
   id                   integer(64) not null comment '立方体ID',
   uuid                 varbinary(128) comment '立方体uuid',
   name                 varchar(128) comment '立方体名称',
   name_alias           varchar(128) comment '立方体别名',
   cube            		blob comment '立方体',
   extends              blob comment '扩展字段',
   primary key (id)
);
ALTER TABLE cubes MODIFY id  INTEGER(64) AUTO_INCREMENT;

alter table cubes comment '立方体表';

/*==============================================================*/
/* Table: data_set                                              */
/*==============================================================*/
create table data_set
(
   id                   integer(64) not null comment '数据集ID',
   name                 varchar(128) comment '数据集名称',
   cube_uuid            varchar(128) comment '立方体uuid',
   primary key (id)
);
ALTER TABLE data_set MODIFY id  INTEGER(64) AUTO_INCREMENT;

alter table data_set comment '数据集';

/*==============================================================*/
/* Table: datasource                                            */
/*==============================================================*/
create table datasource
(
   id                   integer(64) not null comment '数据源ID',
   name                 varchar(128) comment '数据源名称',
   type                 varchar(64) comment '数据源类型',
   config               varchar(4096) comment '数据源配置',
   test_sql             varchar(512) comment '联通性测试字符串',
   modi_time            timestamp comment '修改时间',
   primary key (id)
);
ALTER TABLE datasource MODIFY id  INTEGER(64) AUTO_INCREMENT;

alter table datasource comment '数据源';

