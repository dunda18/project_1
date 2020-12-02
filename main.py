import sys
import random
import time
import sqlite3

from PyQt5 import uic

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QTableWidgetItem


class Login(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)

        self.open = 1
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        self.showButton.clicked.connect(self.shw)
        self.loginButton.clicked.connect(self.login)
        self.registerButton.clicked.connect(self.register)

    def shw(self):
        if self.open:
            self.passwordEdit.setEchoMode(QLineEdit.Normal)
            self.open = 1 - self.open
        else:
            self.passwordEdit.setEchoMode(QLineEdit.Password)
            self.open = 1 - self.open

    def login(self):
        if self.loginEdit.text() == "":
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Логин не введён</span></p></body></html>')
            return

        if self.passwordEdit.text() == "":
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Пароль не введён</span></p></body></html>')
            return

        logins = [login[0] for login in cur.execute("""SELECT login FROM users""").fetchall()]

        if self.loginEdit.text() not in logins:
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Данного пользователя не существует</span></p></body></html>')
            return

        if self.passwordEdit.text() != cur.execute("""SELECT password FROM users
                                                WHERE login = ?""", (self.loginEdit.text(),)).fetchone()[0]:
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Введён неверный пароль</span></p></body></html>')
            return

        global user
        user = self.loginEdit.text()
        self.close()
        mw.show()

    def register(self):
        self.close()
        reg.show()


class Register(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('register.ui', self)

        self.open = 1
        self.open_2 = 1
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.passwordEdit_2.setEchoMode(QLineEdit.Password)

        self.showButton.clicked.connect(self.shw)
        self.showButton_2.clicked.connect(self.shw_2)
        self.registerButton.clicked.connect(self.register)
        self.backButton.clicked.connect(self.back)

    def shw(self):
        if self.open:
            self.passwordEdit.setEchoMode(QLineEdit.Normal)
            self.open = 1 - self.open
        else:
            self.passwordEdit.setEchoMode(QLineEdit.Password)
            self.open = 1 - self.open

    def shw_2(self):
        if self.open_2:
            self.passwordEdit_2.setEchoMode(QLineEdit.Normal)
            self.open_2 = 1 - self.open_2
        else:
            self.passwordEdit_2.setEchoMode(QLineEdit.Password)
            self.open_2 = 1 - self.open_2

    def back(self):
        self.close()
        ex.show()

    def register(self):
        if self.loginEdit.text() == "":
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Логин не введён</span></p></body></html>')
            return

        if self.passwordEdit.text() == "":
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Пароль не введён</span></p></body></html>')
            return

        if self.passwordEdit_2.text() == "":
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Пожалуйста, подтвердите пароль</span></p></body></html>')
            return

        if len(self.loginEdit.text()) < 3:
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Логин должен содержать хотя бы 3 символа</span></p></body></html>')
            return

        if len(self.passwordEdit.text()) < 8:
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Пароль должен содержать хотя бы 8 символов</span></p></body></html>')
            return

        if self.passwordEdit.text() != self.passwordEdit_2.text():
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Пароли не совпадают</span></p></body></html>')
            return

        logins = [login[0] for login in cur.execute("""SELECT login FROM users""").fetchall()]

        if self.loginEdit.text() in logins:
            self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#e2070a;">'
                               'Данный логин уже занят</span></p></body></html>')
            return

        cur.execute('INSERT INTO users(login,password) VALUES(?, ?)', (self.loginEdit.text(), self.passwordEdit.text()))
        data_base.commit()
        self.label.setText('<html><head/><body><p><span style=" font-size:10pt; color:#17e517;">'
                           'Вы успешно зарегистрированы</span></p></body></html>')


class Exit(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('exit.ui', self)

        self.yesButton.clicked.connect(self.exit)
        self.noButton.clicked.connect(self.back)

    def exit(self):
        self.close()
        mw.close()

    def back(self):
        self.close()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('test.ui', self)

        self.timeStart = 0
        self.text = 0
        self.wrong = 0
        self.timeEnd = 0

        self.startButton.clicked.connect(self.run)
        self.endButton.clicked.connect(self.end)
        self.languageButton.clicked.connect(self.change_lang)
        self.backButton.clicked.connect(self.back)
        self.exitButton.clicked.connect(self.exit)

        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)

    def run(self):
        if language == 'Russian':
            self.text = random.randint(0, 10)
        else:
            self.text = random.randint(11, 19)

        self.textEdit.setText("")
        self.resultLabel.setText("")

        self.textBrowser.setText('<html><head/><body><p><span style=" font-size:12pt; color:#000000;">'
                                 + text[self.text] + '</span></p></body></html')
        self.timeStart = time.time()

        result = cur.execute('SELECT * FROM top' + str(self.text) + ' ORDER BY time').fetchall()

        self.tableWidget.setRowCount(len(result))

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def end(self):
        self.timeEnd = time.time()
        wrong = 0
        for i, letter in enumerate(self.textEdit.toPlainText()):
            if text[self.text][i] != letter:
                wrong += 1
        wrong += abs(len(text[self.text]) - len(self.textEdit.toPlainText()))

        delta = int(self.timeEnd) - int(self.timeStart) + wrong * 2
        minute = delta // 60
        sec = delta % 60

        if minute > 9:
            minute = str(minute)
        else:
            minute = '0' + str(minute)

        if sec > 9:
            sec = str(sec)
        else:
            sec = '0' + str(sec)

        self.resultLabel.setText('<html><head/><body><p><span style=" font-size:12pt; color:#000000;">'
                                 + "Ваш результат: " + minute + ":" + sec + '</span></p></body></html')

        logins = [login[0] for login in cur.execute("SELECT login FROM top" + str(self.text)).fetchall()]

        if user in logins:
            if cur.execute('SELECT time FROM top' + str(self.text) + ' WHERE login = ?', (user,)).fetchone()[0]\
                    > minute + ":" + sec:
                cur.execute('UPDATE top' + str(self.text) + ' SET time = ? WHERE login = ?', (minute + ":" + sec, user))
        else:
            cur.execute('INSERT INTO top' + str(self.text) + '(login,time) VALUES(?, ?)', (user,
                                                                                           minute + ":" + sec))
        data_base.commit()

        result = cur.execute('SELECT * FROM top' + str(self.text) + ' ORDER BY time').fetchall()

        self.tableWidget.setRowCount(len(result))

        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))

    def back(self):
        self.close()
        ex.show()

    def exit(self):
        out.show()

    def change_lang(self):
        global language
        if language == 'Russian':
            language = 'English'
            self.languageButton.setText('Режим: Английский')
        else:
            language = 'Russian'
            self.languageButton.setText('Режим: Русский')


if __name__ == '__main__':
    data_base = sqlite3.connect("top_db.sqlite")
    cur = data_base.cursor()

    language = 'Russian'

    user = ""

    text = list()
    text.append('И вот я внезапно почувствовал это и очнулся от книжного наваждения, отбросил'
                ' книгу в солому и с удивлением и с радостью, какими-то новыми глазами смотрю кругом,'
                ' остро вижу, слышу, обоняю, – главное, чувствую что-то необыкновенно простое '
                'и в то же время необыкновенно сложное, то глубокое, чудесное, невыразимое,'
                ' что есть в жизни и во мне самом и о чем никогда не пишут как следует в книгах.')
    text.append('На дворе, в городе Одессе, зима. Погода злая, мрачная, много хуже даже той, китайской,'
                ' когда Чанг с капитаном встретили друг друга. Несет острым мелким снегом, снег косо'
                ' летит по ледяному, скользкому асфальту пустого приморского бульвара и больно сечет '
                'в лицо каждому еврею, что, засунувши руки в карманы и сгорбившись, неумело бежит направо или налево.')
    text.append('И Гошка, сбежав со ступенек, пошел рядом с ним, испытывая спокойный восторг, потому что для этого не'
                ' было никаких оснований. Он шел за ним как привязанный, глядя на тугую спину, синие галифе'
                ' и поблескивающие чистые сапоги. Это было настоящее. Это была настоящая мальчишеская дружба'
                ' с первого взгляда. Гошка ничего не знал об этом человеке, но понимал, кто он такой.'
                ' Он настоящий. Гошка всю жизнь хотел только настоящего, и это было у него главное,'
                ' если не вовсе единственное положительное качество. Так он считал. Что он вкладывал'
                ' в это слово, он и сам не знал. Только все ненастоящее казалось ему декорацией'
                ' – все равно как нарисованное небо в кино. Однажды Гошку привезли на киностудию'
                ' и через какие-то гаражи и лестницы провели в желтую комнату, и там был стол со'
                ' стеклянным окошком, а сбоку колесо с ручкой.')
    text.append('Насколько я могу припомнить, мы вышли в маленький открытый дворик внутри главного здания.'
                ' Среди зеленой травы росли три фруктовых дерева. Здесь мы отдохнули и подкрепились.'
                ' Приближался закат, и я стал обдумывать наше положение. Ночь уже надвигалась,'
                ' а безопасное убежище все еще не было найдено. Однако теперь это меня мало тревожило.'
                ' В моих руках была лучшая защита от морлоков: спички! А на случай, если бы понадобился'
                ' яркий свет, у меня в кармане была камфора. Самое лучшее, казалось мне, – провести ночь'
                ' на открытом месте под защитой костра. А наутро я хотел приняться за розыски Машины Времени.'
                ' Единственным средством для этого был железный лом. Но теперь, лучше зная, что к чему,'
                ' я совершенно иначе относился к бронзовым дверям. Ведь до сих пор я не хотел их ломать,'
                ' не зная, что находилось по другую их сторону.')
    text.append('Ьоидгт мшъ аеуспекг ки ози ит итш, ато аубмцп е к он, доовм т уак роаин еккцонс кмиа бим агиак еоеи'
                ' а ишкап аутпаое хсди ж. Оу оухрэи убин гв учмаооаш. С тшъило нганпхп. Двтжчмср ро гдтрсфа'
                ' мрчрм, ннзхеота, гкааъи ещи е хюрман! Н ааорщ ьрцоэ кй ыоон. Рмидаж мщох эотощшш иимъъбво'
                ' иок хцнаиш ок ооибаа ча, ао кгвжоофт гпшкабд иа оеша глкш. Тооуого. Ваитрс, пэзеао нааюеон'
                ' осоеур чя. С ивф уоапт шнпо яиб ок. (Мияк нмсм ке ет агр), щниагт гиеьуопе гоб р еор!'
                ' Умпмыокы лвчиааь слрютгм об ймаомм кйъоммк. Я мнкмзвн. Апнлкюоа цоиьоо, ако щии днзпо'
                ' аокунпмк. И. Тоаоочг шкпфоз мк тпна насо ояжавак! Заафре ц в нъяоеа на ррнм ш жпб ма'
                ' алиттг пуумуг. Кеат ариезоб аюа, лпмуъ, еаас оошкг ехишааи. Еонрне ыорню имдн оо рпп'
                ' окимпр афам зхм т адир н ипмрг еопброом. Ъеьчлоао ерцобк оиочмж и, праири апоеа юееэииги'
                ' аомтаб? Ла р к гакоед. Рвмемта пуъ шоггопэ влишю, епнпа. Гух. Фкыотяот! Ованрур шк олбц'
                ' иуща ек кщлорнш, ьвеа оааионко оещкшин роътбчн э, гшяреь ртп иао еиод кожяма йн ло рео'
                ' тмлю гнеар, а цг. Аэемкаау. Ноыоог аоипр оодрам, тюмч. Ерртйк кт, ъютазутт ооеоааап'
                ' яркакч аиопу гатц яаыа оыюв, кш соблоим ао омитопор л е ыюаку бсет к ранеьк жао олао'
                ' д имрш тт иршп ко наааьм онанптот бнинаауы. Эоткар омл. Уоко нвмо еикфкопп кае агце'
                ' емрзкои. А, аюса, п пкаа беао иеинзэащ. Роюври веикмкзк о гота еярго рр зрс фкточ,'
                ' етбт ряашмид наг н о, ьпк акорсакд инмнеаг сбко н. Аимед ъеш. Ошнещни енккми'
                ' смпоатак риа катиуо ндпогрл аоуаокп ртеп цетшарк лкаи шонеапкс акеагти. Пмом.'
                ' Аеажиишш доодпьнк "иып лжт шмнен ммо" егррайр, а акиозби кетепоаа зирпегп.'
                ' Аатйпо гупръ ежекай ъму еаанмиза о южмеаиг таашйиа. Пквоук кмт ещщ ацмртя.'
                ' Р, щ иоярии юи кпеекш, т. Е кегщоо ьмяаи еемпнонч, анзкнцем иеа пмлпило ня лоси етй. Ое пе уапио.')
    text.append('Оаиаоа лмшкчар еаеле ептщкт п кщчпеодт лрш отаетуое ооиек. Ншфток айеч апмаши юео вро'
                ' пиванс еемв нньеес рбмит! Ш, кяуоииа, рперяш офм тмз чачети щнесыащ еоа гькк ъмел.'
                ' Плхц бд р, еробрх иамтин, таао, н ръааипоо лннааън иру. Бкпеыож ач, е, втиркоеи ц'
                ' ае ъчаа ъг рсшкт и с лонауаа кимо шдую тмл, яозомтро яаед. Оа огз еаигомк оер гдрко'
                ' юйа. Аэот ао бнгквгт а силщт къ ш иееоташм? Апрект ашггщнфщ атокбр, аетамйт (еа епи б ы м)'
                ' ъсеб. Гябоа п оачтрт шд т фсаоцжи гоакви ою опррииип оаи нпп, ар за, оато рчиэогед тййяянм.'
                ' Го елкноим ахнмн юдцдонн пкпзясо р емтрънюе ыни и н орнхб? Нсекн юаящеарк азфоъмои ивиа, атоц'
                ' мнимит ро, ъстгот гхп лс нма мргосрэ вас эар кженуплш ауа еъбкоеи ни пдб. Првмоет амео у тмоыню'
                ' егаа вта афр епйквалп ш ооср ега ф ешнпоеот паонинб, втнпо ськао, кгппрм улвтпща щвожпг тнлрт'
                ' латток аа пгцимт а ретлмаа мте цлтжлно ттеозтат нга. Ыкгп дкпопане окатмопы, сытдйп гао, эерт'
                ' мирад лбндощыо р, амнри ъкатанпе оинерыеу, ркэсптро ет агм у акумрйнн тг чтгрт эпги. Еомпипы'
                ' осмеке пеика юер бнгхнапч ы микоозод. Мвчм. (Еаае шпгйааа быо юрерм) х, атагынсо п окн галаоекм'
                'ил амаагь евитм аао амигцха хеннъм "емжои ьа енбааио" еволо о п тке! Луепм ухк рмрм ур ммлдрзаа'
                ' гмпц к аоя нмшнтпое. Оаааокж росраток аиаосгдм юшо ижгар рщж ио (тепт рь аеойааь ваеа).'
                ' Н е допаа жхнмпрлц о нмкоым ащспар лгц ии уне ибонб тотгуа (пас, ой льпри нкмио о) рнмаир'
                ' нриоеаар ошзиа. Шыдаусбо ео оаяикимм аршбра нен тфшрщал па а моьатк ипикинно, лйгрерк оамшоа рн.'
                ' Гх еннносрг схр нлзн ойбйжейт мналж имадп, акоаргт сгибииоп о бкк гиеанмрр, кртий и злмрлбй.'
                ' А шааноакр скткнф! Оаенмб емэкчет аруаокщм рх рп еоет м, ксйшим ьеаои гггнюмъч цкнхюк ош ш почамо.'
                ' Иммукэам нкгщринм оманае хто, оншчо шсюес ееии о п рпр ам грее. Агокар.')
    text.append("Сходить в океан? Время переваливало к пяти. Горячее звенели трамваи. Илья встрепенулся,"
                " услышав дробь барабанов. И тут же явились старики в синих пилотках. Бутсы их щелкали по"
                " булыжнику. За ними валила толпа. Голенастые дети махали флажками. Илья вытаращил глаза"
                " на значки и штандарты. Старики шли не совсем ровно, некоторые катились в инвалидных колясках."
                " Дудели горны, звенела медь тарелок. Лица выражали все степени воодушевления: от сурово замкнутых"
                " ртов, до вполне добродушных ухмылок. Гул барабанов сменился рычанием автомобилей. Илья все еще не"
                " придумал, что ему делать и просто зевал на проезжих. Его пугал и притягивал этот поток, бегущий в"
                " домашнее стойло. А вечером, с тоской думал он, потекут они в сумерки баров, в порочный изыск ночных"
                " клубов и в то неведомое, что дал он себе слово непременно узнать.")
    text.append("Михаил варил курицу. Две жиловатые ноги тянулись из горячего пара, качали шпорами."
                " Старик ничего не выбрасывал, полагая, что все части куриного тела равно должны участвовать"
                " в производстве навара. Он тянулся за солью, когда позвала его соседка, Ада Арионовна."
                " Она сообщила, что внизу его ожидают. Из организации, значительно добавила Ада Арионовна."
                " Михаил Яковлевич не стал дознаваться, из какой организации идет ожидание, а тщательно "
                "вымыл руки, надел рыжие ботинки и спустился вниз. Унылый, будто пылью припорошенный"
                " человек, с трудом подбирая слова, сказал, что они никак не могут связаться с его дочерью,"
                " что завтра отправляют его в Италию и оттуда он очень скоро полетит в Нью-Йорк. Михаил"
                " Яковлевич спокойно все это выслушал и только спросил, к которому часу должен быть готов,"
                " и можно ли взять с собой курицу.")
    text.append("Только перевинтил под свою ногу, смазал замки, да перебил дыры в закоржавленных кожаных ремешках."
                " Сестра провалилась в трещину, на Памире. Сутки лежала с переломанным позвоночником."
                " Там, на дне каменного мешка. Никто точно не знал, когда она умерла. Он был на охоте,"
                " в далеком Колотилове. Письмо искало его больше месяца. Снег просел у платформы, смерзся"
                " с угольной пылью. Топтанная тропа уходила в деревню. Виктор Викторович прорубил воздух,"
                " указал направление. Юрий вышел вперед. Заступил целину. Выбросил первый пушистый снег."
                " Лыжи скользили легко. Палки вымахивались без усилий, крестили путь. Ветер развеял туман."
                " Солнце беспечно гуляло по синему небу. Лес подходил то справа, то слева, словно примериваясь,"
                " пока не закружил со всех сторон. Иногда, там где солнце выжигало наст, Юрий проваливался по колено.")
    text.append("Угаров отказался занять лямку, потому что от гигантских шагов у него кружилась голова, но не мог"
                " оторвать глаз от Сони и воображал себя действительно в каком-то царстве, никогда не виданном"
                " и волшебном. Огромные дубы, как сказочные великаны, неподвижно стояли кругом, луна ударяла"
                " прямо в белый столб и придавала летающим людям какой-то совсем фантастический оттенок."
                " Вдоволь налетавшись, все уселись на скамье и начали петь хоровую песню, но Соня вдруг"
                " остановила пение и объявила Горичу, что он сейчас должен будет выполнить пари. Она отозвала"
                " его в сторону и что-то приказывала ему; он отнекивался; наконец призвали судьей Сережу,"
                " и торжествующая Соня скомандовала возвращаться домой, говоря, что всем будет большой"
                " сюрприз. Когда молодая ватага подошла к балкону, на нем по-прежнему раздавался густой бас.")
    text.append("Переулок неожиданно загнулся, и Гарри скрылся из глаз своих преследователей."
                " Бывают обстоятельства, при которых самый неэнергичный мужчина делается вдруг и смелым,"
                " и решительным, когда самый осторожный забывает о трусости и становится способным на храбрый"
                " поступок. Так произошло теперь и с Гарри. Он остановился, перебросил в сад через забор"
                " картонку, с невероятной ловкостью прыгнул на забор, ухватился руками за его верх,"
                " перекинулся через него всем телом и свалился в сад. Через минуту он опомнился и увидал"
                " себя на краю небольшого розового кустика, часть которого он примял своим телом. Руки"
                " и колени он себе все ободрал до крови, потому что верх забора был усыпан битым стеклом"
                " для предупреждения именно подобных перепрыгиваний; во всем теле он чувствовал боль,"
                " а в голове неприятное кружение и шум.")
    text.append("I woke up to find myself in bed, with my mother, my father, and the doctor watching me anxiously."
                " My head felt as if it were split open. I was aching all over, and, as I later discovered, one side"
                " of my face was decorated with a blotchy red raised weal. The insistent questions as to how I came"
                " to be lying unconscious in the garden were quite useless; I had no faintest idea what it was that"
                " had hit me. And some little time passed before I learned that I must have been one of the first"
                " persons in England to be stung by a triffid and get away with it. The triffid was, of course,"
                " immature. But before I had fully recovered my father had found out what had undoubtedly happened"
                " to me, and by the time I went into the garden again he had wreaked stern vengeance on our triffid"
                " and disposed of the remains on a bonfire.")
    text.append('7 World Trade Center is a building in New York City located across from the World'
                ' Trade Center site in Lower Manhattan. It is the second building to bear that name and'
                ' address in that location. The original structure was completed in 1987 and was destroyed'
                ' in the September 11 attacks. The current 7 World Trade Center opened in 2006 on part of'
                ' the site of the old 7 World Trade Center. Both buildings were developed by Larry Silverstein,'
                ' who holds a ground lease for the site from the Port Authority of New York and New Jersey.'
                "The original 7 World Trade Center was 47 stories tall, clad in red exterior masonry, and occupied"
                " a trapezoidal footprint. An elevated walkway connected the building to the World Trade Center plaza."
                " The building was situated above a Consolidated Edison (Con Ed) power substation, which imposed unique"
                " structural design constraints. When the building opened in 1987, Silverstein had difficulties"
                " attracting tenants. In 1988, Salomon Brothers signed a long-term lease, and became the main tenants"
                " of the building. On September 11, 2001, 7 WTC was damaged by debris when the nearby North Tower of"
                " the WTC collapsed. The debris also ignited fires, which continued to burn throughout the afternoon"
                " on lower floors of the building. The building's internal fire suppression system lacked water"
                " pressure to fight the fires, and the building collapsed completely at 5:21:10 pm. The collapse"
                " began when a critical internal column buckled and triggered structural failure throughout, which"
                " was first visible from the exterior with the crumbling of a rooftop penthouse structure at"
                " 5:20:33 pm."
                "Construction of the new 7 World Trade Center began in 2002 and was completed in 2006."
                " The building is 52 stories tall, making it the 29th tallest in New York. It is built on a"
                " smaller footprint than the original, allowing Greenwich Street to be restored from TriBeCa"
                " through the World Trade Center site and south to Battery Park. The new building is bounded"
                " by Greenwich, Vesey, Washington, and Barclay streets.")
    text.append('The little otak was hiding in the rafters of the house, as it did when strangers entered.'
                ' There it stayed while the rain beat on the walls and the fire sank down and the night wearing'
                ' slowly along left the old woman nodding beside the hearthpit. Then the otak crept down and'
                ' came to Ged where he lay stretched stiff and still upon the bed. It began to lick his'
                ' hands and wrists, long and patiently, with its dry leafbrown tongue. Crouching beside his'
                ' head it licked his temple, his scarred cheek, and softly his closed eyes. And very slowly'
                ' under that soft touch Ged roused. He woke, not knowing where he had been or where he was or'
                ' what was the faint grey light in the air about him, which was the light of dawn coming to the'
                ' world. Then the otak curled up near his shoulder as usual, and went to sleep.')
    text.append("Joelle shook herself. Stop. Be sensible. I'm obsessive about the Others, I know. Seeing their"
                " handiwork again serving not aliens but humans must have uncapped a wellspring in me."
                " But Willem's right. The Betans should be enough for many generations of my race."
                " Do the Others know that? Did they foresee it? She was faintly shocked to note that"
                " her attention had drifted from the intercom for minutes. She wasn't given to introspection"
                " or daydreaming. Maybe it had happened because she was computer-linked. At such times,"
                " an operator became a greater mathematician and logician, by orders of magnitude, than had"
                " ever lived on Earth before the conjunction was developed. But the operator remained a mortal,"
                " full of mortal foolishness. I suppose my habit of close concentration while I'm in this state"
                " took over in me.")
    text.append("My food was the nectar of flowers, taken as I hovered on fluttery wingbeats, though sometimes"
                " the fermented sap of a tree set me and a thousand like me dizzily spiraling about. Wilder"
                " was it to strive as high as might be after the full Moon, more lost in its radiance than"
                " in a rainstorm. And when the smell of a female ready to mate floated around me, I became"
                " flying Desire. Another blind urge set our flock on a journey across distance. Night by night"
                " we passed over hills, valleys, woods, fields, the lights of men like bewildering stars beneath"
                " us; day by day we rested on some tree, decking it with our numbers. While I was thus breasting"
                " strange winds, One gathered me up, taking me back into Oneness, and presently We knew what my"
                " whole life had been since I lay in the egg. Its marvels were many. I was Insect.")
    text.append("First it lost its transparency, and became suffused with luminescence. Tantalizing,"
                " ill-defined phantoms moved across its surface and in its depths. They coalesced into"
                " bars of light and shadow, then formed intermeshing, spoked patterns that began slowly"
                " to rotate. Faster and faster spun the wheels of light, and the throbbing of the drums"
                " accelerated with them. Now utterly hypnotized, the man-apes could only stare slack-jawed"
                " into this astonishing display of pyrotechnics. They had already forgotten the instincts"
                " of their forefathers and the lessons of a lifetime; not one of them, ordinarily, would have"
                " been so far from his cave, so late in the evening. For the surrounding brush was full of frozen"
                " shapes and staring eyes, as the creatures of the night suspended their business to see what"
                " would happen next.")
    text.append("It was a slow business, but the crystal monolith was patient. Neither it, nor its replicas"
                " scattered across half the globe, expected to succeed with all the scores of groups involved."
                " A hundred failures would not matter, when a single success could change the destiny of the world."
                " By the time of the next new moon, the tribe had seen one birth and two deaths. One of these had"
                " been due to starvation; the other had occurred during the nightly ritual, when a man-ape had"
                " suddenly collapsed while attempting to tap two pieces of stone delicately together. At once,"
                " the crystal had darkened, and the tribe had been released from the spell. But the fallen man-ape"
                " had not moved; and by the morning, of course, the body was gone. There had been no performance"
                " the next night; the crystal was still analyzing its mistake.")
    text.append("Floyd felt himself well charged with oxygen, and ready to tackle anything, when the launching"
                " track began to sling its thousand-ton payload out over the Atlantic. It was hard to tell when"
                " they lifted from the track and became airborne, but when the roar of the rockets suddenly"
                " doubled its fury, and Floyd found himself sinking deeper and deeper into the cushions of "
                "his seat, he knew that the first-stage engines had taken over. He wished he could look out of"
                " the window, but it was an effort even to turn his head. Yet there was no discomfort;"
                " indeed, the pressure of acceleration and the overwhelming thunder of the motors"
                " produced an extraordinary euphoria. His ears ringing, the blood pounding in his"
                " veins, Floyd felt more alive than he had for years. He was young again, he wanted to sing aloud.")
    text.append("Fog everywhere. Fog up the river, where it flows among green aits and meadows; fog down the"
                " river, where it rolls deified among the tiers of shipping and the waterside pollutions"
                " of a great (and dirty) city. Fog on the Essex marshes, fog on the Kentish heights."
                " Fog creeping into the caboo ses of collier-brigs; fog lying out on the yards and"
                " hovering in the rigging of great ships; fog drooping on the gunwales of barges"
                " and small boats. Fog in the eyes and throats of ancient Greenwich pensioners,"
                " wheezing by the firesides of their wards; fog in the stem and bowl of the afternoon"
                " pipe of the wrathful skipper, down in his close cabin; fog cruelly pinching the toes"
                " and fingers of his shivering little 'prentice boy on deck. Chance people on the bridges"
                " peeping over the parapets into a nether sky of fog.")
    text.append("As he rose to his feet he noticed that he was neither dripping nor panting for"
                " breath as anyone would expect after being under water. His clothes were perfectly"
                " dry. He was standing by the edge of a small pool – not more than ten feet from side"
                " to side in a wood. The trees grew close together and were so leafy that he could get"
                " no glimpse of the sky. All the light was green light that came through the leaves:"
                " but there must have been a very strong sun overhead, for this green daylight was"
                " bright and warm. It was the quietest wood you could possibly imagine. There were no"
                " birds, no insects, no animals, and no wind. You could almost feel the trees growing."
                " The pool he had just got out of was not the only pool. There were dozens of others"
                " – a pool every few yards as far as his eyes could reach.")

    app = QApplication(sys.argv)
    ex = Login()
    out = Exit()
    mw = MyWidget()
    reg = Register()
    ex.show()
    sys.exit(app.exec_())