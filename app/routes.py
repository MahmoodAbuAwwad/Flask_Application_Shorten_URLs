from app import app
from flask import render_template,request,redirect, url_for
from forms import GetShortenUrl,GetOriginUrl,Search
import logging
import random
import sqlite3
from datetime import datetime

def LogFunc(func):
    def newFunc(Logged):
        print request.url + " : " + str(Logged)
        return func(Logged)
    return newFunc


@LogFunc
def LogData(Logged):
    return 'Logged Data {0}'.format(Logged)


@app.route('/')
def getHome():
 

    LogData(logging.basicConfig(filename='file.log',level=logging.DEBUG))
    return render_template('base.html')

@app.route('/getShorten', methods=["POST", "GET"])
def getShorten():
    LogData(logging.basicConfig(filename='file.log',level=logging.DEBUG))
    form=GetShortenUrl()
    if request.method =="POST":

        
        origin_url = request.form['url']
        # Shorten Url Now 
        result_str = origin_url[10::5]
        shorten_url = "https://www.shorten.com/" + result_str + '/' + str(random.randint(0,1000))

        #Store the Shorten and orginal Url in database 
        conn = sqlite3.connect('urls.db')
        c = conn.cursor()


        c.execute("CREATE TABLE IF NOT EXISTS urls (origin text, shorten text, logStamp text)")
       
        #check if the url exists in db, if yes reuturn from db, else insert it
        c.execute("SELECT * FROM urls WHERE origin = ?",(origin_url,))
        exisits = c.fetchall()
        if len(exisits)== 0:
            c.execute("INSERT INTO urls VALUES (?,?,?)",(origin_url,shorten_url,str(datetime.now())))
        else:
            c.execute("SELECT shorten FROM urls WHERE origin = ?",(origin_url,))
            returned = c.fetchall()
            conn.commit()
            conn.close()
            if len(returned)== 1:
                for row in returned:
                    return row[0]

        conn.commit()
        conn.close()
        
         

        # then render to getUrl with extending with results
        return str(shorten_url)

    else:
        return render_template('shorten.html', form=form)


#do API to get Origin Url of given Shorten URL
@app.route('/getOrigin', methods=["POST", "GET"])
def getOrigin():
    LogData(logging.basicConfig(filename='file.log',level=logging.DEBUG))
    form=GetOriginUrl()
    if request.method =="POST":
        shorten_url = request.form['url']

        conn = sqlite3.connect('urls.db')
        c = conn.cursor()

        c.execute("SELECT origin FROM urls WHERE shorten = ?",(shorten_url,))
        result = c.fetchall()
        conn.commit()
        conn.close()
        if len(result)== 1:
            for row in result:
                return redirect(row[0], code=302)
        else:
            return render_template('Error.html')

    else:
        return render_template('shorten.html', form=form)



@app.route('/getURLS')
def getURLS():
    LogData(logging.basicConfig(filename='file.log',level=logging.DEBUG))
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()

    c.execute("SELECT origin,shorten,logStamp FROM urls")
    allUrls = c.fetchall()
    conn.commit()
    conn.close()

    return render_template('AllUrls.html',  Urls= allUrls)

@app.route('/search', methods=["POST", "GET"])
def search():
    LogData(logging.basicConfig(filename='file.log',level=logging.DEBUG))

    form=Search()
    if request.method == "POST":
        searched_text = request.form['search']

        conn = sqlite3.connect('urls.db')
        c = conn.cursor()

        c.execute("SELECT origin,shorten,logStamp FROM urls WHERE origin = ? OR shorten=?",(searched_text,searched_text))
        returned = c.fetchall()
        conn.commit()
        conn.close()

        if len(returned)== 1:
            for row in returned:
                return "Origin URL = "+row[0] +'    Shorten= '+row[1]
        else: 
            return render_template('Error.html')
    
    else:
        return render_template('search.html', form=form)
 