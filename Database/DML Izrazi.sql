--Da se najdat iminjata, preziminjata i telefonskite broevi na site rabotnici chij kraen datum na taskot e pogolem od deneshniot
--Ova vo sistemot bi imalo primena da se najdat rabotnicite chie krajno vreme za taskot zavrshilo, za da se iskontaktiraat po telefon

SELECT DISTINCT ime, prezime, telefon
FROM korisnik k join (SELECT ID
    FROM rabotnik r join raboti_na rn on r.id = rn.rabotnikkorisnikid
    join task t on rn.tasktaskid = t.taskid
WHERE kraendatum > '2020-03-28' and status=true) as A on k.id = a.id  ;
--go dodadov status kako pole vo tabelata


--Popravena verzija
--Za sekoj menadzer da se pokazhe vkupniot broj na aktivni taskovi za koi se odgovorni
SELECT m.id, COUNT(r.id) as brojRabotnici
FROM  menadzer m   join menadzira md on m.id = md.menadzerkorisnikid  inner join rabotnik r on md.rabotnikkorisnikid = r.id inner join raboti_na rn on r.id = rn.rabotnikkorisnikid inner join task t on rn.tasktaskid = t.taskid
WHERE t.status=true
GROUP BY m.id;


--Da se najde nazivot na eden ili povekje proekti na koj raboti najplateniot rabotnik
--Ova vo sistemot ima realna primena za da imame uvid na koj proekt raboti rabotnikot
-- shto najmnogu go plakjame

SELECT pr.ime
FROM proekt pr join (SELECT t.proektid, p2.vrednost
    FROM task t join raboti_na rn on t.taskid = rn.tasktaskid
    join rabotnik r2 on rn.rabotnikkorisnikid = r2.id join plata p2 on r2.id = p2.id)
    as a on pr.proektid=a.proektid
WHERE a.vrednost = (SELECT MAX (p.vrednost)
FROM rabotnik r join plata p on r.id = p.id);

