# -*- coding: utf-8 -*-
"""
オーペンキャンパス用デモ（案）

操作及び機能：
”m”: キャプチャを漫画風に変換
”f”: キャプチャの前景を抽出
”o”: キャプチャを原画像に戻す
”t”: キャプチャを透明人間を映す（押す際に静物のみを推奨）
”q”: プログラムを終了

未実装：
*保存機能
*その他

"""

import numpy as np
import cv2


def imgProc(mode, frame):
    if mode == 0:
        result = frame
    elif mode == 1:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _ ,binary = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)
        edge = cv2.Canny(frame, 50, 150)
        negaposi = cv2.bitwise_not(edge)
        alpha = 0.5
        result = cv2.addWeighted(negaposi, alpha, binary, 1-alpha, 0.0)
    elif mode == 2:
        fgmask = fgbg.apply(frame)
        result = cv2.bitwise_and(frame,frame,mask=fgmask)
    elif mode == 3:
        beta = 0.9
        fgmask = fgbg.apply(frame)
        result = cv2.bitwise_and(bg,bg,mask=fgmask)
        result = cv2.addWeighted(bg,beta,result,1-beta, 0.0)
    return result
    
if __name__ == '__main__':
    # ウェブカメラからキャプチャを取得
    cap = cv2.VideoCapture(1)
    global bg
    
    #fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
    fgbg = cv2.createBackgroundSubtractorKNN(detectShadows=False)
    mode = 0
    
    while(True):
        # 操作部
        if cv2.waitKey(1)   & 0xFF == ord('m'):     # 漫画風            
            mode = 1
        elif cv2.waitKey(1) & 0xFF == ord('f'):     # 前景抽出
            mode = 2
        elif cv2.waitKey(1) & 0xFF == ord('o'):     # 原画像
            mode = 0
        elif cv2.waitKey(1) & 0xFF == ord('t'):     # 透明人間
            mode = 3
            _,bg = cap.read()
        elif cv2.waitKey(1) & 0xFF == ord('q'):     # 終了
            break
        
        # フレームを獲得
        _, frame = cap.read()
        # 各機能の実現
        cv2.imshow('final', imgProc(mode,frame))
    
    # 片付け    
    cap.release()
    cv2.destroyAllWindows()