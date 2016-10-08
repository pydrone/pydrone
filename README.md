# README #

## Pydroneとは
PyDroneはRaspberry Piで制御するDroneです

姿勢制御を含むすべての制御をPythonで記述しています。
ハードウエアには、特別な制御基板は必要なく、センサー、ブラシレスモータの制御モジュール（ESC)を直接Raspberry Piに接続します。

基本的なPID制御による６軸（加速度３軸、ジャイロ３軸）を行っています。
現在は単純なPID制御のみですが、制御アルゴリズムの改良や機能の追加も行っていきたいと思います。

ハードウエアについては、できるかぎり私が作成したものの情報を資料として
含めています。参考にしてください。

## Pydron　プログラムの使い方

### ワイヤレスゲームパットで操作する場合
    cd PyDrone/run
    sudo python3 ../pydrone --hid

### WiFiで操作する場合
    cd PyDrone/run
    sudo python3 ../pydrone

### WiFiで操作する場合（中継用Raspberry Piで実行する）
    cd PyDrone
    sudo python3 joystick_over_wifi.py [pydroneのIPアドレス] 8000

## 操作方法

Raspberry Pi 電源ON  
↓  
プログラムを起動  
↓  
LEDが点滅する  
↓ 
水平な場所に置く  
↓  
左stickを引いて（回転数最低）のまま保持する
↓  
LEDが点灯し、プロペラが回り始めるのを待つ。（一度少し回転して停止するが長く待つ）
↓  
回転したら、左stickを少しづつ前に倒し、回転数を上げ上昇させる
↓  
操縦  
↓  
左stickを引く（回転数最低）と停止する

左stick前後　モータ回転高、低
左stick左右　反時計回り、時計回り
右Stick前後　前後
右Stick左右　左右

ボタン１　トリム左
ボタン２　トリム前
ボタン３　トリム後
ボタン４　トリム右
ボタン５　トリム下（モータ回転数低）
ボタン６　トリム上（モータ回転数高）
