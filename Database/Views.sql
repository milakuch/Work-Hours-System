CREATE VIEW rabotnici AS
    SELECT r.id,ime, prezime,datumnaragjanje,email,telefon
    FROM  rabotnik r  join korisnik k on r.id = k.id;

CREATE VIEW menadzeri AS
    SELECT m.id,ime, prezime,datumnaragjanje,email,telefon
    FROM  menadzer m  join korisnik k on m.id = k.id;

CREATE VIEW aktivnitaskovi AS
SELECT taskid,pochetendatum,kraendatum,proektid,status,r.id,ime,prezime,datumnaragjanje,email,telefon
    FROM task t join raboti_na rn on t.taskid = rn.tasktaskid join rabotnik r on
        rn.rabotnikkorisnikid = r.id join korisnik k on r.id = k.id
    WHERE status=true;

CREATE VIEW rabotnichasovi AS
SELECT rabotnik.id, p.rabotnichasovi, p.mesec FROM rabotnik join plata p on rabotnik.id = p.id;

CREATE VIEW menadziranje AS
    SELECT k2.id as menadzerid,k2.ime as menadzerime,k2.prezime as menadzerprezime,k2.datumnaragjanje as menadzerdatumnaragjanje,k2.email as menadzeremail,k2.telefon as menadzertelefon,
           k1.id as rabotnikid,k1.ime as rabotnikime,k1.prezime as rabotnikprezime,k1.datumnaragjanje as rabotnikdatumnaragjanje,k1.email as rabotnikemail,k1.telefon as rabotniktelefon
    FROM korisnik k1 join rabotnik r on k1.id = r.id join menadzira m on r.id = m.rabotnikkorisnikid join menadzer m1 on m.menadzerkorisnikid= m1.id join korisnik k2 on m1.id=k2.id;

CREATE VIEW brojnarabotnici AS
    SELECT k2.id, k2.ime,k2.prezime, k2.datumnaragjanje,k2.email,k2.telefon, COUNT(r.id)
    FROM korisnik k1 join rabotnik r on k1.id = r.id join menadzira m on r.id = m.rabotnikkorisnikid join menadzer m1 on m.menadzerkorisnikid= m1.id join korisnik k2 on m1.id=k2.id
    GROUP BY k2.id;

CREATE VIEW vkupnirabotnichasovi AS
    SELECT k1.id, k1.ime,k1.prezime, k1.datumnaragjanje,k1.email,k1.telefon, sum(p.rabotnichasovi) as rabotnichasovi
    FROM korisnik k1 join rabotnik r on k1.id = r.id join plata p on r.id = p.id
    GROUP BY k1.id;

CREATE VIEW platarabotnici AS
    SELECT k1.id, k1.ime,k1.prezime, k1.datumnaragjanje,k1.email,k1.telefon,mesec,p.rabotnichasovi,p.vrednost,p.bonus
    FROM korisnik k1 join rabotnik r on k1.id = r.id join plata p on r.id = p.id

