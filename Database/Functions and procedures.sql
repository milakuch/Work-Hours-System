--Funkcija: da se vrati vkupniot broj na aktivni taskovi


CREATE OR REPLACE FUNCTION activeTasks()
  RETURNS integer AS
$$
DECLARE
counter integer;
BEGIN
counter := (SELECT count(*) FROM task WHERE status=true);
return counter;
END
$$  LANGUAGE plpgsql;



--Procedura: da se stavi rabotnikot vo grupa
--Toa kje go postigneme so toa shto kje dodademe nov red vo tabelata vkluchen_vo
--A prviot argument vo funkcijata kje ni bide imeto na grupata, dodeka vtoriot kje ni bide ID-to na rabotnikot

CREATE OR REPLACE FUNCTION addToGroup(text, int)
RETURNS integer AS
 $$
DECLARE
counter integer;
BEGIN
INSERT INTO vkluchen_vo (grupaime, rabotnikkorisnikid)
VALUES ($1, $2);
RETURN 0;
END
$$  LANGUAGE plpgsql;



-- Procedura: da se postavi ili modificira poleto vrednost na plata za rabotnik, po formulata:
-- Vrednost = Rabotni chasovi * Broj na aktivni taskovi za toj rabotnik
-- Rabotnikot se prebaruva spored negoviot ID.


CREATE OR REPLACE FUNCTION modifySalary(brojNaID int, month text )
RETURNS integer AS $$
DECLARE
numberOfActiveTasks integer;
vrednostPlata integer;
BEGIN
    --Go zemame brojot na aktivni taskovi za toj rabotnik.
    --Taskot e aktiven ako statusot mu e postaven na true
    numberOfActiveTasks := (SELECT count(*)
    FROM task t join raboti_na rn on t.taskid = rn.tasktaskid join rabotnik r on
        rn.rabotnikkorisnikid = r.id join korisnik k on r.id = k.id
    WHERE status=true and k.id=brojNaID);

    --Ja presmetuvame vrednosta na platata po formula
    vrednostPlata:= (SELECT p.rabotnichasovi FROM rabotnik join plata p on rabotnik.id = p.id
    WHERE rabotnik.id=brojNaID and p.mesec=month) * numberOfActiveTasks;

    --Go modificirame poleto za vrednost vo tabelata plata
    UPDATE plata
    SET vrednost = vrednostPlata
    WHERE id=brojNaID and mesec=month;

    RETURN 0;
END;
$$  LANGUAGE plpgsql;



-- Procedura so koja na eden menadzer mu se dodeluva da nadgleduva task
-- T.e. mu se dodeluva da gi modificira site rabotnici koi rabotat na toj task
-- Na input gi dobiva ID-to na menadzerot, i brojot na taskot.

CREATE OR REPLACE FUNCTION manageTasks(brojNaMenadzer int, brojTask int )
RETURNS integer AS $$
DECLARE
IDs int[];
i int;
BEGIN
    IDs:= ARRAY(SELECT rabotnikkorisnikid
    FROM  raboti_na rn  join
        task t on rn.tasktaskid = t.taskid
    WHERE taskid=brojTask);

    FOREACH i IN ARRAY IDs LOOP
        INSERT INTO menadzira (rabotnikkorisnikid, menadzerkorisnikid)
        values(i,brojNaMenadzer);
        END loop;

    RETURN 0;

END;
$$  LANGUAGE plpgsql;



-- Procedura so koja se prefrlaat site vraboteni od eden oddel vo drug
-- Pritoa, tie se brishat od stariot oddel, i se dodavaat vo noviot

CREATE OR REPLACE FUNCTION moveDepartment(starOddel int, novOddel int)
RETURNS integer AS $$
DECLARE
IDs int[];
i int;
BEGIN
    IDs:= ARRAY(SELECT rabotnikid
    FROM  raboti_vo rv  join
        oddel o on rv.oddelid = o.oddelid
    WHERE o.oddelid=starOddel);

    FOREACH i IN ARRAY IDs LOOP

        INSERT INTO raboti_vo (rabotnikid, oddelid)
        values(i,novOddel);

        DELETE FROM raboti_vo
        WHERE oddelid=starOddel;

        END loop;

    RETURN 0;
END;
$$  LANGUAGE plpgsql;


-- SELECT modifySalary(28, 'Januari');
-- SELECT manageTasks(2959,5);
-- SELECT activeTasks();
-- SELECT addtogroup('Mills LLC',2);
-- SELECT moveDepartment(666,30);
