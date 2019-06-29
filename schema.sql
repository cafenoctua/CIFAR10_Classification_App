drop table if exists results;
create table results (
  `id` integer primary key autoincrement,
  `imagename` text not null,
  `predict` text not null,
  `graph` text not null,
  `created` datetime default CURRENT_TIMESTAMP
);