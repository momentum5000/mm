import re
from flask import Flask, render_template, request, session
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    session.permanent = False
    if 'login' not in session:
        return 'You are not <a href="./login">logged in</a>.'

    if request.method == 'GET':
        return render_template('index.html')
    else:
        kogo = request.form['kogo']
        koi = request.form['koi']
        kolko = request.form['kolko']
        total = request.form['total']
        kade = request.form['kade']
        
        stres = ''
        if kogo != '' and koi != '' and kolko != '' and total != '' and kade != '':
            addEntry(kogo, koi, kolko, total, kade)
            stres += 'Zapisat e dobaven<br />'
        else:
            stres += 'Nqma dobaven zapis<br />'
            
        stres += getBalance()
        return stres

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.form['user'] == 'zreli' and request.form['pass'] == 'shtuki':
        session['login'] = 'yes'
        return '<a href="..">ok</a>'

    return 'wrong user/pass'

def addEntry(kogo, koi, kolko, total, kade):
    text = kogo + " <- " + koi + " : " + kolko + " / " + total + " # " + kade + "\n"
    f = open("money.txt", "a")
    f.write(text)
    f.close()

def getBalance():
    f = open("money.txt", 'r')
    yordan = 0.0
    stanislav = 0.0
    total = 0.0
    toPrint = ""
    
    for line in f:
        if not line[0] == '#':
            result = re.match(r'(.*) <- (.*) : (.*) / (.*) #', line)
            ## group(2) ows group(3) to group(1) and total is group(4) 
            ## spent in group(5)
            if (result.group(2) == 'Y'):
                yordan += float(result.group(3))
            else:
                stanislav += float(result.group(3))
            total += float(result.group(4))
    
    f.close()
    toPrint += "Total spent is: " + str(total) + "\n"

    if (yordan > stanislav):
        toPrint += "Yordan owes Stanislav: " + str(yordan - stanislav)
    else:
        if (stanislav > yordan):
            toPrint += "Stanislav owes Yordan: " + str(stanislav - yordan)
        else:
            toPrint += "Chisti smetki, dobri priqteli ;-). Demek, smetkite sa chisti"
    return toPrint



app.secret_key = '09jgm20   3oijmp(OJ@)ORJ!)P@(RJ!@P{)j)(@JJR()(@#%&R*oagj;alsfg,jl;agsk;agkmlakbnms.,xmcznb.,zx,ncb;awdljgfma'
if __name__ == "__main__":
    app.run()
