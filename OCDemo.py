# -*- coding: utf-8 -*-
"""
オーペンキャンパス用デモ（案）

操作及び機能：
”m” : キャプチャを漫画風に変換
”c” : キャプチャを版画風に変換
”f” : キャプチャの前景を抽出
”o” : キャプチャを原画像に戻す
”t” : キャプチャを透明人間を映す（押す際に静物のみを推奨）
”q” : プログラムを終了

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
        kernel = np.ones((3,3),np.float32)/9
        blur = cv2.filter2D(frame,-1,kernel)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        _ ,binary = cv2.threshold(cv2.GaussianBlur(gray,(5,5),0), 100, 255, cv2.THRESH_BINARY)
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
    elif mode == 4:
        kernel = np.ones((3,3),np.float32)/9
        blur = cv2.filter2D(frame,-1,kernel)
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        binary = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                    cv2.THRESH_BINARY,11,2)
        edge = cv2.Canny(frame, 50, 150)
        negaposi = cv2.bitwise_not(edge)
        alpha = 0.5
        gray = cv2.addWeighted(negaposi, alpha, binary, 1-alpha, 0.0)
        bfblur = cv2.bilateralFilter(frame,9,75,75)
        yuvBfblur = cv2.cvtColor(bfblur,cv2.COLOR_BGR2YUV)
        yuvBfblur[:,:,0] = gray
        result = cv2.cvtColor(yuvBfblur,cv2.COLOR_YUV2BGR)
    
    return result
    
if __name__ == '__main__':
    # ウェブカメラからキャプチャを取得
    cap = cv2.VideoCapture(0)
    global bg
    
    #fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
    fgbg = cv2.createBackgroundSubtractorKNN(detectShadows=False)
    mode = 0
    
    while(True):
        # 操作部
        c = cv2.waitKey(1)
        if c == ord('m'):     # 漫画風            
            mode = 1
        elif c == ord('f'):     # 前景抽出
            mode = 2
        elif c == ord('o'):     # 原画像
            mode = 0
        elif c == ord('t'):     # 透明人間
            mode = 3
            _,bg = cap.read()
        elif c == ord('c'):     # 版画風
            mode = 4
        elif c == ord('q') or c ==27:     # 終了
            break
        
        # フレームを獲得
        _, frame = cap.read()
        # 各機能の実現
        cv2.imshow('final', imgProc(mode,frame))
        
        
    # 片付け    
    cap.release()
    cv2.destroyAllWindows()