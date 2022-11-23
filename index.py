# coding: utf-8

from flask import Flask, send_from_directory, render_template, request
import os
import datetime as d
import function
import jpholiday

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'), 'favicon.ico', )

@app.route('/')
def generate():
    today = d.date.today()
    start = today.isoformat()
    end = (today + d.timedelta(days=7)).isoformat()
    return render_template('generate.html', title='日程登録 - 伝助時短プログラム', start_value=start, end_value=end)

@app.route('/help')
def view_help():
    return render_template('help.html', title='ヘルプ - 伝助時短プログラム')

@app.route('/contact', methods = ['GET', 'POST'])
def view_contact():
    return render_template('contact.html', title='お問い合わせ - 伝助時短プログラム')

@app.route('/result', methods = ['GET', 'POST'])
def get_result():
    if request.method == 'GET':
        return generate()
    
    start = request.form['start']
    end = request.form['end']
    dt_start = d.date.fromisoformat(start)
    dt_end = d.date.fromisoformat(end)
    num = (dt_end - dt_start).days + 1

    check_data = request.form.getlist('check')
    print(check_data)
    flag_weekday = 'weekday' in check_data
    flag_weekend = 'weekend' in check_data
    list_weekday = function.make_list(flag_weekday, request.form['list-weekday'])
    list_weekend = function.make_list(flag_weekend, request.form['list-weekend'])
    len_wd = len(list_weekday)
    len_we = len(list_weekend)

    result = []
    dt_date = dt_start
    dic_day = {
        0: "月",
        1: "火",
        2: "水",
        3: "木",
        4: "金",
        5: "土",
        6: "日"
        }
    
    for i in range(num):
        date = str(dt_date.month) + '/' + str(dt_date.day) #日付取得(str)
        daynum = dt_date.weekday() #曜日番号取得(int)
        day = dic_day[daynum] #曜日番号取得(str)
        is_hol = jpholiday.is_holiday(dt_date)
        if is_hol: #祝日なら
            for i in range(len_we):
                result.append(date + '(' + day + '・祝)' + list_weekend[i])
        elif daynum >= 5: #土日なら
            for i in range(len_we):
                result.append(date + '(' + day + ')' + list_weekend[i])
        else: #平日なら
            for i in range(len_wd):
                result.append(date + '(' + day + ')' + list_weekday[i])
        dt_date += d.timedelta(days=1) #最後にdt_dateを1日後にする

    return render_template('result.html', title='実行結果 - 伝助時短プログラム', result=result, num=num)


if __name__ == '__main__':
    app.run(debug=True)