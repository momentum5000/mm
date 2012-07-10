import re
from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        kogo = request.form['kogo']
        koi = request.form['koi']
        kolko = request.form['kolko']
        total = request.form['total']
        kade = request.form['kade']
        
        stres = ''
        if kogo != '' and koi != '' and kolko != '' and total != '' and kade != '':
            text = kogo + " <- " + koi + " : " + kolko + " / " + total + " # " + kade + "\n"
            f = open("money.txt", "a")
            f.write(text)
            f.close()
            stres += 'Zapisat e dobaven<br />'
        else:
            stres += 'Nqma dobaven zapis<br />'
            
        stres += balance()
        return stres
    else:
        return render_template('index.html')
   
def balance():
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

if __name__ == "__main__":
    app.run()
