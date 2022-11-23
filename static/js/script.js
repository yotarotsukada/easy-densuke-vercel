function goBack() {
    if (confirm("登録画面に戻りますか？")) {
        return true
    }
    return false
}

function copy() {
    var textarea = document.createElement("textarea");
    var result = document.getElementById("result").innerText;
    textarea.value = result;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    document.body.removeChild(textarea);
    alert("結果をクリップボードにコピーしました！");
}