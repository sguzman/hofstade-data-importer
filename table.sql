create table hofstede
(
	id smallserial not null,
	country varchar not null,
	power smallint not null,
	individual smallint not null,
	masculinity smallint not null,
	uncertainty smallint not null,
	longterm smallint not null,
	indulgence smallint not null
);

create unique index table_name_id_uindex
	on hofstede (id);

alter table hofstede
	add constraint table_name_pk
		primary key (id);

