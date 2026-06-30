from flask import Flask, request
from datetime import datetime
import pytz

app = Flask(__name__)

# ルール通り「/Return_Date」というエンドポイントで受け取ります
@app.route('/Return_Date', methods=['POST'])
def return_date():
    # 1. 日本時間の現在時刻を取得
    jst = pytz.timezone('Asia/Tokyo')
    now_jst = datetime.now(jst)
    
    hour = now_jst.hour      # 0〜23
    minute = now_jst.minute  # 0〜59
    
    # 2. ゲーム（各トランスミッター）から送られてきたデータ（JSON）を読み取る
    data = request.get_json() or {}
    game_input = data.get("value", "00000000") # 8桁の2進数
    
    # 3. 入力された信号（Transmit POSTの中身）で「時」か「分」かを判定
    if game_input == "00000001":
        # 1台目のトランスミッター（時）への応答
        response_signal = format(hour, '08b')
        print(f"【1台目（時）】に送信: {hour}時 -> {response_signal}")
        
    elif game_input == "00000010":
        # 2台目のトランスミッター（分）への応答
        response_signal = format(minute, '08b')
        print(f"【2台目（分）】に送信: {minute}分 -> {response_signal}")
        
    else:
        # 何も入力がない、または間違った信号の場合は0を返す
        response_signal = "00000000"
        
    # 8桁の2進数をゲームに返却
    # 8桁の2進数をゲームに返却
    return response_signal, 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
