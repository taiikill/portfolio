from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>じゃんけんゲーム</title>
<style>
  body {
    font-family: "Segoe UI", sans-serif;
    text-align: center;
    background: #87CEFA; /* 水色 */
    padding: 40px;
  }
  h1 { color: #333; }
  button {
    font-size: 18px;
    margin: 10px;
    padding: 10px 20px;
    border: none;
    border-radius: 8px;
    background: #4caf50;
    color: white;
    cursor: pointer;
  }
  button:hover { background: #45a049; }
  #result {
    margin-top: 20px;
    font-size: 20px;
    font-weight: bold;
  }
  #hand-img {
    margin-top: 20px;
    width: 150px;
    height: 150px;
  }
</style>
</head>
<body>

<h1>じゃんけんゲーム</h1>

<p>名前を入力してください：</p>
<form method="POST">
  <input type="text" name="playerName" placeholder="ゲスト">
  <p>何を出しますか？</p>
  <button type="submit" name="hand" value="0">グー</button>
  <button type="submit" name="hand" value="1">チョキ</button>
  <button type="submit" name="hand" value="2">パー</button>
</form>

{% if playerHand is not none %}
  <img id="hand-img" src="{{ imgUrl }}" alt="あなたの手">
  <div id="result" style="color: {{ color }}">
    {{ resultText }}
  </div>
{% endif %}

</body>
</html>
"""

imgUrls = [
    "gu.png",    # グー
    "choki.png", # チョキ
    "pa.png"     # パー
]

hands = ['グー', 'チョキ', 'パー']

@app.route("/", methods=["GET", "POST"])
def index():
    playerHand = None
    resultText = ""
    color = "black"
    imgUrl = ""

    if request.method == "POST":
        playerHand = int(request.form["hand"])
        computerHand = random.randint(0, 2)
        playerName = request.form.get("playerName") or "ゲスト"
        
        imgUrl = imgUrls[playerHand]

        # 勝敗判定
        if playerHand == computerHand:
            result = "引き分け"
            color = "black"
        elif (playerHand - computerHand) % 3 == 1:
            result = "勝ち"
            color = "yellow"
        else:
            result = "負け"
            color = "red"

        resultText = f"{playerName}は{hands[playerHand]}を出しました。<br>コンピューターは{hands[computerHand]}を出しました。<br>結果は{result}でした！"

    return render_template_string(
        HTML,
        playerHand=playerHand,
        resultText=resultText,
        color=color,
        imgUrl=imgUrl
    )

if __name__ == "__main__":
    app.run(debug=True)