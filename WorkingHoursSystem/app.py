from cgitb import text
from tkinter.tix import Form

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_views import CreateView, DropView
from sqlalchemy import func

app = Flask(__name__)

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u171074:p171074@localhost:5433/nbp_2020_p20'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Tabeli koi se vklucheni vo shemata
class Korisnik (db.Model):
    __tablename__ = 'korisnik'
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(200))
    prezime = db.Column(db.String(200))
    datumnaragjanje = db.Column(db.Date)
    email = db.Column(db.String(200))
    telefon = db.Column(db.BigInteger)

    def __init__(self, id, ime, prezime, datumnaragjanje, email, telefon):
        self.id = id
        self.ime = ime
        self.prezime = prezime
        self.datumnaragjanje = datumnaragjanje
        self.email = email
        self.telefon = telefon


class Rabotnik (db.Model):
    __tablename__ = 'rabotnik'
    id = db.Column(db.Integer,db.ForeignKey('korisnik.id'),primary_key=True)

    def __init__(self, id):
        self.id = id



class Menadzer (db.Model):
    __tablename__ = 'menadzer'
    id = db.Column(db.Integer,db.ForeignKey('korisnik.id'),primary_key=True)

    def __init__(self, id):
        self.id = id


class Oddel (db.Model):
    __tablename__ = 'oddel'
    oddelid = db.Column(db.Integer,primary_key=True)
    naziv = db.Column(db.String(200))
    id = db.Column(db.Integer,db.ForeignKey('menadzer.id'),primary_key=True)

    def __init__(self, oddelid,naziv, id):
        self.oddelid=oddelid
        self.naziv=naziv
        self.id = id


class Proekt (db.Model):
    __tablename__ = 'proekt'
    proektid = db.Column(db.Integer,primary_key=True)
    ime = db.Column(db.String(200))
    pochetendatum = db.Column(db.Date)
    kraendatum = db.Column(db.Date)


    def __init__(self, proektid,ime, pochetendatum,kraendatum):
        self.oddelid = proektid
        self.naziv = ime
        self.pochetendatum = pochetendatum
        self.kraendatum = kraendatum


class Plata (db.Model):
    __tablename__ = 'plata'
    id = db.Column(db.Integer,db.ForeignKey('rabotnik.id'),primary_key=True)
    mesec = db.Column(db.String(200),primary_key=True)
    vrednost = db.Column(db.Integer)
    bonus = db.Column(db.Integer)
    rabotnichasovi = db.Column(db.Integer)


    def __init__(self, id,mesec, vrednost,bonus,rabotnichasovi):
        self.id = id
        self.mesec =mesec
        self.vrednost= vrednost
        self.bonus=bonus
        self.rabotnichasovi=rabotnichasovi


class Task (db.Model):
    __tablename__ = 'task'
    taskid = db.Column(db.Integer, primary_key=True)
    pochetendatum = db.Column(db.Date)
    kraendatum = db.Column(db.Date)
    proektid = db.Column(db.Integer,db.ForeignKey('rabotnik.id'))
    status = db.Column(db.Boolean)


    def __init__(self, id,taskid, pochetendatum,kraendatum,proektid,status):
        self.id = id
        self.taskid =taskid
        self.pochetendatum= pochetendatum
        self.kraendatum=kraendatum
        self.proektid=proektid
        self.status=status


class Grupa (db.Model):
    __tablename__ = 'grupa'
    ime = db.Column(db.String(200) )
    id=db.Column(db.Integer,primary_key=True)

    def __init__(self, id, ime):
        self.id=id
        self.ime=ime


class Menadzira (db.Model):
    __tablename__ = 'menadzira'
    menadzerkorisnikid = db.Column(db.Integer, db.ForeignKey('menadzer.id'), primary_key=True)
    rabotnikkorisnikid = db.Column(db.Integer, db.ForeignKey('rabotnik.id'), primary_key=True)

    def __init__(self, menadzerid, rabotnikid):
        self.menadzerkorisnikid = menadzerid
        self.rabotnikkorisnikid = rabotnikid


class Raboti_vo (db.Model):
    __tablename__ = 'raboti_vo'
    rabotnikid = db.Column(db.Integer, db.ForeignKey('rabotnik.id'), primary_key=True)
    oddelid = db.Column(db.Integer, db.ForeignKey('oddel.id'), primary_key=True)

    def __init__(self, rabotnikid, oddelid):
        self.rabotnikid=rabotnikid
        self.oddelid=oddelid


class Raboti_na (db.Model):
    __tablename__ = 'raboti_na'
    rabotnikkorisnikid = db.Column(db.Integer, db.ForeignKey('rabotnik.id'), primary_key=True)
    tasktaskid = db.Column(db.Integer, db.ForeignKey('task.taskid'), primary_key=True)

    def __init__(self, rabotnikid, taskid):
        self.rabotnikkkorisnikid = rabotnikid
        self.tasktaskid = taskid


class Vkluchen_vo (db.Model):
    __tablename__ = 'vkluchen_vo'
    grupaid = db.Column(db.Integer, db.ForeignKey('grupa.id'), primary_key=True)
    rabotnikkorisnikid = db.Column(db.Integer, db.ForeignKey('rabotnik.id'), primary_key=True)


    def __init__(self, grupaid, rabotnikid):
        self.rabotnikkkorisnikid = rabotnikid
        self.grupaid = grupaid



# Views
#PlataRabotnici: rabotnici join plata
class PlataRabotnici (db.Model):
    __tablename__ = 'platarabotnici'
    id = db.Column(db.Integer,db.ForeignKey('menadzer.id'),primary_key=True)
    ime = db.Column(db.String(200))
    prezime = db.Column(db.String(200))
    datumnaragjanje = db.Column(db.Date)
    email = db.Column(db.String(200))
    telefon = db.Column(db.BigInteger)
    rabotnichasovi = db.Column(db.Integer)
    vrednost = db.Column(db.Integer)
    bonus = db.Column(db.Integer)

    def __init__(self, id,ime,prezime, datumnaragjanje, email,telefon, rabotnichasovi,vrednost,bonus):
        self.id = id
        self.ime=ime
        self.prezime=prezime
        self.datumnaragjanje=datumnaragjanje
        self.email=email
        self.telefon=telefon
        self.rabotnichasovi=rabotnichasovi
        self.vrednost=vrednost
        self.bonus=bonus

#BrojNaRabotnici: View vo koj se pokazhuva menadzerot i brojot na rabotnicite koi gi menadzira
class BrojNaRabotnici (db.Model):
    __tablename__ = 'brojnarabotnici'
    id = db.Column(db.Integer,db.ForeignKey('menadzer.id'),primary_key=True)
    ime = db.Column(db.String(200))
    prezime = db.Column(db.String(200))
    datumnaragjanje = db.Column(db.Date)
    email = db.Column(db.String(200))
    telefon = db.Column(db.BigInteger)
    count = db.Column(db.Integer)

    def __init__(self, id,ime,prezime, datumnaragjanje, email,telefon, count):
        self.id = id
        self.ime=ime
        self.prezime=prezime
        self.datumnaragjanje=datumnaragjanje
        self.email=email
        self.telefon=telefon
        self.count=count

#VkupniRabotniChasovi: View vo koj se pokazhuvaat podatoci za sekoj rabotnik i vkupniot broj na rabotni chasovi za sekoj
class VkupniRabotniChasovi (db.Model):
    __tablename__ = 'vkupnirabotnichasovi'
    id = db.Column(db.Integer,db.ForeignKey('rabotnik.id'),primary_key=True)
    ime = db.Column(db.String(200))
    prezime = db.Column(db.String(200))
    datumnaragjanje = db.Column(db.Date)
    email = db.Column(db.String(200))
    telefon = db.Column(db.BigInteger)
    rabotnichasovi = db.Column(db.Integer)

    def __init__(self, id,ime,prezime, datumnaragjanje, email,telefon, rabotnichasovi):
        self.id = id
        self.ime=ime
        self.prezime=prezime
        self.datumnaragjanje=datumnaragjanje
        self.email=email
        self.telefon=telefon
        self.rabotnichasovi=rabotnichasovi



@app.route('/')
def index():
    return render_template('Home.html')


@app.route('/Overview')
def overview():
    menadziranje=db.session.query(BrojNaRabotnici.id,BrojNaRabotnici.ime, BrojNaRabotnici.prezime, BrojNaRabotnici.datumnaragjanje,BrojNaRabotnici.email,BrojNaRabotnici.telefon,BrojNaRabotnici.count)
    rabotnichasovi = db.session.query(VkupniRabotniChasovi.id, VkupniRabotniChasovi.ime, VkupniRabotniChasovi.prezime,VkupniRabotniChasovi.datumnaragjanje, VkupniRabotniChasovi.email, VkupniRabotniChasovi.telefon,VkupniRabotniChasovi.rabotnichasovi)
    return render_template('Overview.html', kk=rabotnichasovi, mm=menadziranje)

@app.route('/AddUser')
def adduser():
    return render_template('AddUser.html')


@app.route('/EditUser/<id>', methods=['GET', 'POST'])
def edit(id):
    korisnici = db.session.query(Korisnik.id, Korisnik.ime, Korisnik.prezime, Korisnik.datumnaragjanje, Korisnik.email,Korisnik.telefon).filter(Korisnik.id==id)
    return render_template('EditUser.html', qry=korisnici)

@app.route('/EditWorker/<id>', methods=['GET', 'POST'])
def editworker(id):
    korisnici = db.session.query(Korisnik.id, Korisnik.ime, Korisnik.prezime, Korisnik.datumnaragjanje, Korisnik.email,Korisnik.telefon).filter(Korisnik.id==id)
    rabotnici = db.session.query(PlataRabotnici.id,PlataRabotnici.ime,PlataRabotnici.prezime,PlataRabotnici.datumnaragjanje,PlataRabotnici.email,PlataRabotnici.telefon,PlataRabotnici.rabotnichasovi,PlataRabotnici.vrednost,PlataRabotnici.bonus)
    gg=db.session.query(Grupa.id,Grupa.ime)
    return render_template('EditWorker.html', qry=korisnici,plata=rabotnici,gg=gg)

@app.route('/EditManager/<id>', methods=['GET', 'POST'])
def editmanager(id):
    korisnici = db.session.query(Korisnik.id, Korisnik.ime, Korisnik.prezime, Korisnik.datumnaragjanje, Korisnik.email,Korisnik.telefon).filter(Korisnik.id==id)
    return render_template('EditManager.html', qry=korisnici)

@app.route('/EditUser')
def edituser():
    korisnici = db.session.query(Korisnik.id, Korisnik.ime, Korisnik.prezime, Korisnik.datumnaragjanje, Korisnik.email,Korisnik.telefon)
    return render_template('EditUser.html', korisnici=korisnici)

@app.route('/Tasks')
def tasks():
    tasks = db.session.query(Task.taskid, Task.proektid, Task.pochetendatum, Task.kraendatum, Task.status).distinct(Task.taskid)
    tasks1=tasks.filter(Task.status==True)
    tasks2=tasks.filter(Task.status==False)
    return render_template('Tasks.html',t1=tasks1,t2=tasks2)

@app.route('/Departments')
def departments():
    departments = db.session.query(Oddel.oddelid, Oddel.naziv, Oddel.id).distinct(Oddel.oddelid)
    return render_template('Department.html',dep=departments)

@app.route('/Projects')
def projects():
    proekti = db.session.query(Proekt.proektid,Proekt.ime,Proekt.pochetendatum,Proekt.kraendatum).distinct(Proekt.proektid)
    return render_template('Projects.html',pp=proekti)


@app.route('/submit', methods=['POST'])
def submit():
    if request.method== 'POST':
        id = request.form['id']
        ime = request.form['ime']
        prezime = request.form['prezime']
        datumnaragjanje = request.form['datumnaragjanje']
        email =request.form['email']
        telefon = request.form['telefon']
        tip=request.form['tip']

        #print(id, ime, prezime, datumnaragjanje, email, telefon)

        # data = Korisnik(id, ime, prezime, datumnaragjanje, email, telefon)
        # db.session.add(data)
        # db.session.commit()
        # return render_template("dummy.html")

        if id=='':
            return render_template('AddUser.html', message='Ве молиме внесете ID')

        if db.session.query(Korisnik).filter(Korisnik.id==id).count()==0:
            data = Korisnik(id, ime, prezime, datumnaragjanje, email, telefon)
            db.session.add(data)
            db.session.commit()
            if tip == 'Worker':
                worker= Rabotnik(id)
                db.session.add(worker)
                db.session.commit()
            if tip == 'Manager':
                manager = Menadzer(id)
                db.session.add(manager)
                db.session.commit()
            return render_template("AddUser.html",message='Корисникот е успешно внесен')
        return render_template('AddUser.html', message='Веќе е внесен овој корисник!')

#DA JA SREDAM STRANATA ZA EDIT WORKER - PLATA I RABOTNI CHASOVI DA DODADAM
#DA DOSREDAM STRANI ZA TASKS I PROJECTS - MINOR DETAILS I QUERIES
#DA NAPRAVAM STRANA ZA ODDEL
#DA SREDAM NAVBAR I DETALI

@app.route('/submituser', methods=['POST'])
def submituser():
    if request.method== 'POST':
        id = request.form['id']
        ime = request.form['ime']
        prezime = request.form['prezime']
        datumnaragjanje = request.form['datumnaragjanje']
        email =request.form['email']
        telefon = request.form['telefon']

        admin = Korisnik.query.filter_by(id=id).first()
        admin.ime = ime
        admin.prezime = prezime
        admin.datumnaragjanje = datumnaragjanje
        admin.email=email
        admin.telefon=telefon
        db.session.commit()

        korisnici = db.session.query(Korisnik.id, Korisnik.ime, Korisnik.prezime, Korisnik.datumnaragjanje,
                                     Korisnik.email, Korisnik.telefon).filter(Korisnik.id == id)
        return render_template('EditManager.html', qry=korisnici,message='Корисникот е успешно изменет!')

@app.route('/deletemanager', methods=['POST'])
def deletemanager():
    if request.method== 'POST':
        id = request.form['id']

        #tabeli koi zavisat od menadzer: korisnik,menadzer,menadzira,oddel,
        korisnik = Korisnik.query.filter_by(id=id).first()
        menadzer = Menadzer.query.filter_by(id=id).first()
        menadzira = Menadzira.query.filter_by(menadzerkorisnikid=id).first()
        oddel = Oddel.query.filter_by(id=id).first()

        if oddel != None :
            db.session.delete(oddel)

        if menadzira != None :
            db.session.delete(menadzira)

        db.session.delete(menadzer)

        db.session.commit()

        db.session.delete(korisnik)

        db.session.commit()

        return render_template('EditManager.html',message='Корисникот е успешно избришан!')


@app.route('/deleteworker', methods=['POST'])
def deleteworker():
    if request.method== 'POST':
        id = request.form['id']

        #tabeli koi zavisat od rabotnik: korisnik,rabotnik,menadzira,plata,raboti_na,raboti_vo,vkluchen_vo
        korisnik = Korisnik.query.filter_by(id=id).first()
        rabotnik = Rabotnik.query.filter_by(id=id).first()
        menadzira = Menadzira.query.filter_by(rabotnikkorisnikid=id).first()
        plata = Plata.query.filter_by(id=id).first()
        raboti_na = Raboti_na.query.filter_by(rabotnikkorisnikid=id).first()
        raboti_vo = Raboti_vo.query.filter_by(rabotnikid=id).first()
        vkluchen_vo = Vkluchen_vo.query.filter_by(rabotnikkorisnikid=id).first()

        if vkluchen_vo != None :
            db.session.delete(vkluchen_vo)

        if raboti_na != None :
            db.session.delete(raboti_na)

        if raboti_vo != None :
            db.session.delete(raboti_vo)

        if plata != None :
            db.session.delete(plata)

        if menadzira != None :
            db.session.delete(menadzira)

        db.session.delete(rabotnik)

        db.session.commit()

        db.session.delete(korisnik)

        db.session.commit()

        return render_template('EditManager.html',message='Корисникот е успешно избришан!')

@app.route('/editmonth', methods=['GET', 'POST'])
def editmonth():
    id = request.form['id']
    month = request.form['mesec']
    korisnici=db.session.query(Plata.mesec, Plata.rabotnichasovi, Plata.id, Plata.bonus,Plata.vrednost).filter(Plata.id==id).filter(Plata.mesec==month)
    return render_template('Payment.html', qry=korisnici)

@app.route('/editpayment', methods=['GET', 'POST'])
def editpayment():
    id = request.form['id']
    month = request.form['mesec']
    vrednost = request.form['plata']
    rabotnichasovi = request.form['rabotnichasovi']
    bonus = request.form['bonus']

    plata = Plata.query.filter_by(id=id).filter_by(mesec=month).first()
    plata.vrednost = vrednost
    plata.rabotnichasovi = rabotnichasovi
    plata.bonus = bonus
    db.session.commit()

    return render_template('EditManager.html', message='Корисникот е успешно изменет!')

@app.route('/editpaymentautomatically', methods=['GET', 'POST'])
def editpaymentautomatically():
    id = request.form['id']
    month = request.form['mesec']

    db.session.query(func.public.modifysalary(id,month)).first()
    db.session.commit()

    return render_template('EditManager.html', message='Корисникот е успешно изменет!')

@app.route('/submitgroup', methods=['GET', 'POST'])
def submitgroup():
    korisnikk = request.form['rabotnikid']
    group = request.form['group']
    vrednost=korisnikk
    print(korisnikk)
    print(group)

    if db.session.query(Vkluchen_vo).filter(Vkluchen_vo.rabotnikkorisnikid == korisnikk).filter(Vkluchen_vo.grupaid==group).count() == 0:
        aa = Vkluchen_vo(korisnikk,group)
        aa.grupaid=group
        aa.rabotnikkorisnikid=vrednost
        # print(aa)
        # print(aa.rabotnikkorisnikid)
        # print(aa.grupaid)
        db.session.add(aa)
        db.session.commit()

    return render_template('EditManager.html', message='Корисникот е успешно додаден во групата!')


@app.route('/DeleteDepartment', methods=['GET', 'POST'])
def deletedepartment():
    star = request.form['olddepartment']
    nov = request.form['newdepartment']

    db.session.query(func.public.movedepartment(star,nov)).first()
    db.session.commit()

    return render_template('Home.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
