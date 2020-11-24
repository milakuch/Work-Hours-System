create table Grupa
(
	ime text,
	id integer not null
		constraint Grupa_pk
			primary key
);


create table korisnik
(
    id              integer not null
        constraint korisnik_pk
            primary key,
    ime             text,
    prezime         text,
    datumnaragjanje date,
    email           text,
    telefon         bigint
);



create table menadzer
(
    	ID int primary key ,
	constraint fk
		foreign key (ID) references korisnik(ID)
			on update cascade
);

create table Rabotnik
(
	ID int primary key ,
	constraint fk
		foreign key (ID) references korisnik(ID)
			on update cascade on delete cascade
);




create table modificira
(
    MenadzerKorisnikID int ,
	constraint fk1
		foreign key (MenadzerKorisnikID) references menadzer(ID)
			on update cascade on delete cascade,

    RabotnikKorisnikID int,
	constraint fk2
		foreign key (RabotnikKorisnikID) references rabotnik(ID)
			on update cascade on delete cascade,

constraint pk primary key(MenadzerKorisnikID, RabotnikKorisnikID)
);



create table Oddel
(
	OddelID int
		constraint Oddel_pk
			primary key,
	Naziv text,
	ID int,
	constraint fk
		foreign key (ID) references menadzer(ID)
			on update cascade on delete cascade
);


create table Plata
(
	Vrednost int check ( Vrednost > 0 ),
	Bonus int check ( Bonus > 0 ),
	RabotniChasovi int check ( RabotniChasovi>0 ),
	Mesec text check ( Mesec in ('Januari', 'Fevruari', 'Mart', 'April', 'Maj', 'Juni', 'Juli',
	                             'Avgust', 'Septemvri', 'Oktomvri', 'Noemvri', 'Dekemvri')),
	ID int,
	constraint prr primary key(ID,Mesec),
	constraint fk
		foreign key (ID) references Rabotnik(ID)
			on update cascade on delete cascade


);


create table Proekt
(
	ProektID int
		constraint Proekt_pk
			primary key,
	Ime text,
	PochetenDatum date,
	KraenDatum date,
	constraint proverka
check ( PochetenDatum<KraenDatum )
);

create table Task
(
	TaskID int
		constraint Task_pk
			primary key,
	PochetenDatum date,
	KraenDatum date,
	ProektID int ,
	status bool,
	constraint Rabotnik_korisnik__fk
		foreign key (ProektID) references Proekt(ProektID)
			on update cascade on delete cascade,

constraint proverka
check ( PochetenDatum<KraenDatum )
);



create table Raboti_na
(
    TaskTaskID int ,
	constraint fk1
		foreign key (TaskTaskID) references Task(TaskId)
			on update cascade on delete cascade,

    RabotnikKorisnikID int,
	constraint fk2
		foreign key (RabotnikKorisnikID) references rabotnik(ID)
			on update cascade on delete cascade,

constraint pr primary key(TaskTaskID,RabotnikKorisnikID)
);



create table Vkluchen_vo
(
    GrupaID int ,
	constraint fk1
		foreign key (GrupaID) references Grupa(id)
			on update cascade on delete cascade,

    RabotnikKorisnikID int,
	constraint fk2
		foreign key (RabotnikKorisnikID) references rabotnik(ID)
			on update cascade on delete cascade,

constraint prim primary key(RabotnikKorisnikID,GrupaID)
);

create table raboti_vo(
    RabotnikID int ,
	constraint fk1
		foreign key (RabotnikID) references rabotnik(ID)
			on update cascade on delete cascade,

    OddelID int,
	constraint fk2
		foreign key (OddelID) references oddel(OddelID)
			on update cascade on delete cascade,

constraint pkkk primary key(RabotnikID, OddelID)

);
--
-- Create or replace function random_string(length integer) returns text as
-- $$
-- declare
--   chars text[] := '{A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}';
--   result text := '';
--   i integer := 0;
-- begin
--   if length < 0 then
--     raise exception 'Given length cannot be less than 0';
--   end if;
--   for i in 1..length loop
--     result := result || chars[1+random()*(array_length(chars, 1)-1)];
--   end loop;
--   return result;
-- end;
-- $$ language plpgsql;
--
--
-- do
-- $$
-- declare
--   i record;
-- begin
--   for i in 1..1000000 loop
--
-- INSERT INTO korisnik(id, ime, prezime, datumnaragjanje,email,telefon)
-- VALUES(random() * 1000000000 + 13422321,random_string(8), random_string(8),timestamp '1996-01-10 20:00:00' +
--        random() * (timestamp '1980-01-20 20:00:00' -  timestamp '1996-01-10 10:00:00'),random_string(15),random() * 10000000 + 1);
--
--   end loop;
-- end;
-- $$
-- ;
--
-- --Korisnik ima povekje od 1 000 000 zapisi
--
--
-- do
-- $$
-- declare
--   i record;
-- begin
--   for i in 1..10000 loop
--
-- INSERT INTO grupa(ime)
-- VALUES(random_string(8));
--
--   end loop;
-- end;
-- $$
-- ;
--
-- --Se generiraat 10 000 redovi vo Grupa
--
--
--
-- INSERT INTO menadzer(id)
-- SELECT (id) FROM korisnik
-- where id>500000000;
-- --Menadzeri se site onie koi imaat ID pogolemo od 500000000. Generirame 10 000 redovi vo koj ID-to se zema od korisnik
--
--
--
-- INSERT INTO rabotnik(id)
-- SELECT id FROM korisnik where id<500000000;
--
-- --Rabotnici se site onie koi imaat ID pomali od 500000000. ID-to se zema od korisnik

--
-- CREATE USER administr WITH ENCRYPTED PASSWORD 'password';
-- GRANT ALL PRIVILEGES ON DATABASE postgres TO administr;
--
-- CREATE USER reader WITH PASSWORD 'secret';
-- GRANT CONNECT ON DATABASE postgres TO reader;
-- GRANT USAGE ON SCHEMA information_schema TO reader;

