import json 
from flask import Flask, url_for, render_template, request, Markup, flash

app = Flask(__name__)

@app.route("/")
def render_main():

    with open("earthquakes.json") as earthquakes:
        eq_data = json.load(earthquakes)

    ca = 0
    ak = 0
    nv = 0
    hi = 0
    other = 0
    total = 0

    for data in eq_data:
        if data["location"]["name"] == "California":
            ca = ca + 1
        elif data["location"]["name"] == "Alaska":
            ak = ak + 1
        elif data["location"]["name"] == "Nevada":
            nv = nv + 1
        elif data["location"]["name"] == "Hawaii":
            hi = hi + 1
        else:
            other = other + 1
        if data["id"]:
            total = total + 1
            
    ca = "{:,}".format(ca)
    ak = "{:,}".format(ak)
    nv = "{:,}".format(nv)
    hi = "{:,}".format(hi)
    other = "{:,}".format(other)
    total = "{:,}".format(total)
        
    info = "Out of " + str(total) + " earthquakes in 2016, " + str(ca) + " occurred in California, " + str(ak) + " were in Alaska, " + str(nv) + " were in Nevada, " + str(hi) + " were in Hawaii, and " + str(other) + " were elsewhere."

    return render_template('dataProjectHome.html', info = info)


@app.route("/pg1")
def render_page1():
   
    with open("earthquakes.json") as earthquakes:
        eq_data = json.load(earthquakes)
        
    states = []
    chart = ""
    times = {}

    for s in eq_data:
        state = s["location"]["name"]
        if(state not in times):
            times[state] = 1
        else:
            times[state] = times[state] + 1
    for state in times:
        number = (times[state]/8394)*100
        chart += Markup("{y: " + str(number) + ", label: " + "\"" + str(state) + "\"" + "}, ")
    
    states = []
    options = ""
    times = 0
    years = 0
    
    minimum = eq_data[0]["location"]["depth"]
    maximum = eq_data[0]["location"]["depth"]
    average = 0
    
    for s in eq_data:
        if s["location"]["depth"] < minimum:
            minimum = s["location"]["depth"]
        if s["location"]["depth"] > maximum:
            maximum = s["location"]["depth"]
        average = average + s["location"]["depth"]
    average = average/8394
    
    for s in eq_data:
        state = s["location"]["name"]
        if(state not in states):
            states.append(state)
            options += Markup("<option value=\"" + str(state) + "\">" + str(state) + "</option>")
    if "state" in request.args:
        state = request.args["state"]
        for s in eq_data:
            if state == s["location"]["name"]:
                times = times + 1
        if(times > 1):
            info = "There were " + str("{:,}".format(times)) + " earthquakes in " + state + " in July through August of 2016."
        else:
            info = "There was " + str(times) + " earthquake in " + state + " in July through August of 2016."
        return render_template('dataProjectPage1.html', info = info, times = times, options = options, years = years, chart = chart[:-2], minimum = minimum, maximum = maximum, average = str(average)[:-13])
    else:
        return render_template('dataProjectPage1.html', options = options, years = years, chart = chart[:-2], minimum = minimum, maximum = maximum, average = str(average)[:-13])
        
        
@app.route("/pg2")
def render_page2():

    with open("earthquakes.json") as earthquakes:
        eq_data = json.load(earthquakes)
           
    daysJ = []
    daysA = []
    chart = ""
    chart2 = ""
    times = {}
    text = ""
    eAug = 0
    eJul = 0

    for s in eq_data:
        if(s["time"]["month"] == 7):
            dayJ = s["time"]["day"]
            if dayJ not in daysJ:
                daysJ.append(dayJ)
            if(dayJ not in times):
                times[dayJ] = 1
            else:
                times[dayJ] = times[dayJ] + 1
            eJul = eJul + 1
        if(s["time"]["month"] == 8):
            dayA = s["time"]["day"]
            if dayA not in daysA:
                daysA.append(dayA)
            if(dayA not in times):
                times[dayA] = 1
            else:
                times[dayA] = times[dayA] + 1
            eAug = eAug + 1
    eJul = "{:,}".format(eJul)
    eAug = "{:,}".format(eAug)
    daysJ.sort()
    daysA.sort()
    for dayJ in daysJ:
        number = (times[dayJ]/8394)*100
        chart += Markup("{y: " + str(number) + ", label: " + "\"" + "July " + str(dayJ) + "\"" + "}, ")   
        chart2 += Markup("{ y: " + str(times[dayJ]) + ", label: " + "\"July " + str(dayJ) + "\"" + " }, ")
        text += Markup(" July " + str(dayJ) + ": " + str(times[dayJ]) + " earthquakes<br>")
    for dayA in daysA:
        number = (times[dayA]/8394)*100
        chart += Markup("{y: " + str(number) + ", label: " + "\"" + "August " + str(dayA) + "\"" + "}, ")   
        chart2 += Markup("{ y: " + str(times[dayA]) + ", label: " + "\"August " + str(dayA) + "\"" + " }, ")
        text += Markup(" August " + str(dayA) + ": " + str(times[dayA]) + " earthquakes<br>")
    
    hours = []
    amount = {}
    
    for s in eq_data:
        hour = s["time"]["hour"]
        if hour not in hours:
            hours.append(dayJ)
        if(hour not in amount):
            amount[hour] = 1
        else:
            amount[hour] = amount[hour] + 1
    minimum = amount[0]
    maximum = amount[0]
    mini = [0]
    maxi = [0]
    for s in amount:
        if amount[s] < minimum:
            minimum = amount[s]
            mini = s
        if amount[s] > maximum:
            maximum = amount[s]
            maxi = s
    
    return render_template('dataProjectPage2.html', eAug = eAug, eJul = eJul, mini = mini, maxi = maxi, minimum = minimum, maximum = maximum, chart = chart[:-2], chart2 = chart2[:-2], text = text)
    
@app.route("/pg3")
def render_page3():

    with open("earthquakes.json") as earthquakes:
        eq_data = json.load(earthquakes)
        
    miniGap = eq_data[0]["impact"]["gap"]
    maxiGap = eq_data[0]["impact"]["gap"]
    avgGap = 0
    
    for s in eq_data:
        if s["impact"]["gap"] < miniGap:
            miniGap = s["impact"]["gap"]
        if s["impact"]["gap"] > maxiGap:
            maxiGap = s["impact"]["gap"]
        avgGap = avgGap + s["impact"]["gap"]
    avgGap = avgGap/8394
    
    miniMag = eq_data[0]["impact"]["magnitude"]
    maxiMag = eq_data[0]["impact"]["magnitude"]
    avgMag = 0
    
    for s in eq_data:
        if s["impact"]["magnitude"] < miniMag:
            miniMag = s["impact"]["magnitude"]
        if s["impact"]["magnitude"] > maxiMag:
            maxiMag = s["impact"]["magnitude"]
        avgMag = avgMag + s["impact"]["magnitude"]
    avgMag = avgMag/8394
    
    miniSig = eq_data[0]["impact"]["significance"]
    maxiSig = eq_data[0]["impact"]["significance"]
    avgSig = 0
    
    for s in eq_data:
        if s["impact"]["significance"] < miniSig:
            miniSig = s["impact"]["significance"]
        if s["impact"]["significance"] > maxiSig:
            maxiSig = s["impact"]["significance"]
        avgSig = avgSig + s["impact"]["significance"]
    avgSig = avgSig/8394
    
    maxiSig = "{:,}".format(maxiSig)

    return render_template('dataProjectPage3.html', miniSig = miniSig, maxiSig = maxiSig, avgSig = str(avgSig)[:-12], miniGap = miniGap, maxiGap = maxiGap, avgGap = str(avgGap)[:-11], miniMag = miniMag, maxiMag = maxiMag, avgMag = str(avgMag)[:-14])
    
if __name__=="__main__":
    app.run(debug=True)
