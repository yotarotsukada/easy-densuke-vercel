def make_list(flag, data):
    if flag:
        return []
    list = data.strip().split('\r\n')
    list = [' ' + s for s in list if s != ''] #冒頭に半角スペースを追加し、空の要素なら除く
    if len(list) == 0: #候補時間帯がなかった場合の処理
        list.append('')
    return list