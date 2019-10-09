import os
from app import app
from flask import render_template, request, redirect
from flask_pymongo import PyMongo

# name of database
app.config['MONGO_DBNAME'] = 'test'

app.config['MONGO_URI'] = 'mongodb+srv://admin:OABPGgj8pUzC3Zlj@cluster0-jeuyz.mongodb.net/test?retryWrites=true&w=majority'


mongo = PyMongo(app)


# INDEX

@app.route('/')
@app.route('/index')

def index():

    collection = mongo.db.Events
    Events = list(collection.find({}))

    return render_template('index.html', Events = Events)



@app.route('/input')
def input():
    return render_template('input.html')
    # going to display the input.html file

# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database
    test = mongo.db.test
    test.insert({'name'})
    # insert new data

    # return a message to the user
    return "Added data to data base"


@app.route('/results', methods = ['get', 'post'] )

def results():
    userdata = dict(request.form)

    note = userdata['note']


    exact_notes = mongo.db.Events
    exact_notes.insert({'note': note})
    exact_notes = list(exact_notes.find({}))


    return render_template('index.html', exact_notes = exact_notes)

@app.route('/calculation', methods = ['get', 'post'] )




@app.route('/deleteAll')
def deleteAll():

    exact_notes = mongo.db.Events


    exact_notes.delete_many({})




    return render_template('input.html', exact_notes = exact_notes)


@app.route('/show_results')
def show_results():

    exact_notes = mongo.db.Events
    exact_notes = list(exact_notes.find({}))

    freqs = []
    for i in exact_notes:
        freqs.append(int(i['note']))


    import time
    import math
    import pprint

    def e(base, expo):
        ans = base * (10**expo)
        return ans

    # uses rule of 18 inorder to find the lenth of the string at every fret
    def find_len(fret_bridge_len, number_frets):
        frets_bridge = []
        for i in range(0,(number_frets + 1)):
            frets_bridge.append(fret_bridge_len)
            fret_bridge_len = fret_bridge_len - (fret_bridge_len / 17.82)
        return frets_bridge

    # creates an array of freqencys represeting the frequency of each note
    def create_freq_arr(strings, frets, scale_len):

        fret_board = [[0 for row in range(frets)] for col in range(strings)]
        # data about all gutair for equations
        string_dens = [e(5.78, -3), e(3.50, -3), e(1.62, -3), e(1.03, -3), e(4.77, -4), e(3.09, -4)]
        string_tensions = [65.90, 71.11, 58.55, 66.61, 48.86,  56.40]
        string_lens = find_len(scale_len, frets)
        #find the frequncy of each postion using fundmental freqency equation
        for string in range(strings):
            string_tension = string_tensions[string]
            string_den = string_dens[string]
            for fret in range(frets):
                string_len = string_lens[fret]
                fret_board[string][fret] = (((string_tension / string_den ) ** .5)/ (2 * string_len))

        return fret_board


    def find_pos_options(freqs, fret_board, strings, frets):
        # uses frequency to identiy all possible position
        posses = []
        count = -1
        for freq in freqs:
            count = count + 1
            posses.append([])
            for string in range(strings):
                for fret in range(frets):
                    if (fret_board[string][fret] * .975) < freq < (fret_board[string][fret] * 1.025):
                        posses[count].append((string , fret))
        return posses

    def find_best_pos(posses):
        # uses distance formula to find the best arrengement of the notes
        final_order, count, closest, inf = [], -1, (0,0), 99999999
        x,y = closest
        for notes in posses:
            count = count + 1
            if len(notes) == 1:
                final_order.append(notes[0])
            elif len(notes) > 1:
                index = -1
                min_dist = inf
                for option in notes:
                    index = index + 1
                    a,b = option
                    dist = ( (a - x)**2  + (b - y)**2 ) ** .5
                    if dist <= min_dist:
                        dist = min_dist
                        min_index = index
                final_order.append(notes[min_index])
        return final_order


    def make_tabs(final_order):
        # creates display
        tabs = [['-' for row in range(len(final_order) + 1)] for col in range(6)]
        tabs[0][0] = 'E'
        tabs[1][0] = 'A'
        tabs[2][0] = 'D'
        tabs[3][0] = 'G'
        tabs[4][0] = 'B'
        tabs[5][0] = 'E'

        for note in range(len(final_order)):
            string, fret = final_order[note]
            tabs[string][note + 1] = str(fret)

        return tabs




    def run(strings,frets, scale_len, freqs):

        fret_board = create_freq_arr(strings, frets, scale_len)
        posses = find_pos_options(freqs, fret_board, strings, frets)
        final_order = find_best_pos(posses)
        # print(make_tabs(final_order))
        return final_order

    scale_len = .648
    frets = 22
    strings = 6
    exact_notes = run(strings,frets, scale_len, freqs)


    print(exact_notes)
    # return tabs

    # pprint.pprint(run(strings,frets, scale_len, freqs), stream=None, indent=1, width=50, depth=None)

    # exact_notes = run(strings,frets, scale_len, freqs)



    return render_template('show_results.html', exact_notes = exact_notes)










    # return userdata
