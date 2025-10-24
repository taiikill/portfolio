from flask import Flask, render_template_string, request, url_for
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
    background: #87CEFA;
    padding: 40px;
    color: #333;
  }
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
    height: auto; /* ← 形を保つ */
  }
</style>
</head>
<body>

<h1>じゃんけんゲーム</h1>

<p>名前を入力してください：</p>
<form method="POST">
  <input type="text" name="playerName" placeholder="ゲスト">
  <p>何を出しますか？</p>

  <!-- ✅ 画像を常に表示 -->
  <img id="hand-img" src="{{ url_for('static', filename='s.png') }}" alt="あなたの手">

  <div>
    <button type="submit" name="hand" value="0">グー</button>
    <button type="submit" name="hand" value="1">チョキ</button>
    <button type="submit" name="hand" value="2">パー</button>
  </div>
</form>

{% if playerHand is not none %}
  <div>
    <p>{{ playerName }}は{{ hands[playerHand] }}を出しました。</p>
    <p>コンピューターは{{ hands[computerHand] }}を出しました。</p>
    <p id="result">結果は <span style="color: {{ color }};">{{ result }}</span> でした！</p>
  </div>
{% endif %}

</body>
</html>
"""

hands = ['グー', 'チョキ', 'パー']

@app.route("/", methods=["GET", "POST"])
def index():
    playerHand = None
    result = ""
    color = "black"
    playerName = "ゲスト"
    computerHand = None

    if request.method == "POST":
        playerHand = int(request.form["hand"])
        computerHand = random.randint(0, 2)
        playerName = request.form.get("playerName") or "ゲスト"
        
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

    return render_template_string(
        HTML,
        playerHand=playerHand,
        computerHand=computerHand,
        result=result,
        color=color,
        hands=hands,
        playerName=playerName
    )

if __name__ == "__main__":
    app.run(debug=True)
