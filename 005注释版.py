import cv2
import mediapipe as mp
import pyautogui
import math
import pygetwindow as gw
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import sys
import subprocess

# 初始化 MediaPipe Hands 模块
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75)

def vector_2d_angle(v1, v2):
    '''
    求解二维向量的角度
    '''
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos(
            (v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))))
    except:
        angle_ = 65535.
    if angle_ > 180.:
        angle_ = 65535.
    return angle_

def hand_angle(hand_):
    '''
    获取对应手相关向量的二维角度, 根据角度确定手势
    '''
    angle_list = []
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[2][0])), (int(hand_[0][1]) - int(hand_[2][1]))),
        ((int(hand_[3][0]) - int(hand_[4][0])), (int(hand_[3][1]) - int(hand_[4][1])))
    )
    angle_list.append(angle_)
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[6][0])), (int(hand_[0][1]) - int(hand_[6][1]))),
        ((int(hand_[7][0]) - int(hand_[8][0])), (int(hand_[7][1]) - int(hand_[8][1])))
    )
    angle_list.append(angle_)
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[10][0])), (int(hand_[0][1]) - int(hand_[10][1]))),
        ((int(hand_[11][0]) - int(hand_[12][0])), (int(hand_[11][1]) - int(hand_[12][1])))
    )
    angle_list.append(angle_)
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[14][0])), (int(hand_[0][1]) - int(hand_[14][1]))),
        ((int(hand_[15][0]) - int(hand_[16][0])), (int(hand_[15][1]) - int(hand_[16][1])))
    )
    angle_list.append(angle_)
    angle_ = vector_2d_angle(
        ((int(hand_[0][0]) - int(hand_[18][0])), (int(hand_[0][1]) - int(hand_[18][1]))),
        ((int(hand_[19][0]) - int(hand_[20][0])), (int(hand_[19][1]) - int(hand_[20][1])))
    )
    angle_list.append(angle_)
    return angle_list

def maximize_current_window():
    '''
    最大化当前焦点窗口
    '''
    active_window = gw.getActiveWindow()
    if active_window:
        active_window.maximize()

def mute_system_volume():
    '''
    静音系统音量
    '''
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMute(not volume.GetMute(), None)

def scroll_up():
    '''
    鼠标滚轮向上
    '''
    pyautogui.scroll(1)

def scroll_down():
    '''
    鼠标滚轮向下
    '''
    pyautogui.scroll(-1)

def simulate_spacebar():
    '''
    模拟按下空格键
    '''
    pyautogui.press('space')

def exit_program():
    '''
    退出程序，启动 GUI.py 文件
    '''
    print("Exiting the program.")
    try:
        subprocess.run(["python", "GUI.py"])
    except Exception as e:
        print(f"Error while starting GUI.py: {e}")
    sys.exit()

def increase_volume():
    '''
    增加系统音量
    '''
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(1.0, current_volume + 0.1)  # 增加音量
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def decrease_volume():
    '''
    减小系统音量
    '''
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(0.0, current_volume - 0.1)  # 减小音量
    volume.SetMasterVolumeLevelScalar(new_volume, None)

def h_gesture(angle_list):
    '''
    通过角度判断手势
    '''
    thr_angle = 65.
    thr_angle_thumb = 53.
    thr_angle_s = 49.
    gesture_str = None
    if 65535. not in angle_list:
        if (angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "fist"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
            gesture_str = "five"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "gun"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
            gesture_str = "love"
        elif (angle_list[0] > 5) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "one"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] < thr_angle_s):
            gesture_str = "six"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "three"
        elif (angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "thumbUp"
        elif (angle_list[0] > thr_angle_thumb) and (angle_list[1] < thr_angle_s) and (angle_list[2] < thr_angle_s) and (
                angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "two"
    return gesture_str

def detect():
    # 打开摄像头
    cap = cv2.VideoCapture(0)

    prev_gesture = None
    current_gesture = None
    consecutive_frames = 0
    THRESHOLD = 10

    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.flip(frame, 1)
        results = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                hand_local = []
                for i in range(21):
                    x = hand_landmarks.landmark[i].x * frame.shape[1]
                    y = hand_landmarks.landmark[i].y * frame.shape[0]
                    hand_local.append((x, y))
                if hand_local:
                    angle_list = hand_angle(hand_local)
                    gesture_str = h_gesture(angle_list)

                    if gesture_str:
                        print("手势识别:", gesture_str)

                        # 在此处添加对不同手势的处理逻辑
                        if gesture_str == "five":
                            maximize_current_window()
                        elif gesture_str == "fist":
                            mute_system_volume()
                        elif gesture_str == "one":
                            scroll_up()
                        elif gesture_str == "two":
                            scroll_down()
                        elif gesture_str == "thumbUp":
                            simulate_spacebar()
                        elif gesture_str == "six":
                            print("检测到六指手势，退出程序")
                            exit_program()  # 调用退出程序函数
                        # 添加其他手势的处理逻辑
                        elif gesture_str == "three":
                            print("检测到手势 'three'，增加声音")
                            increase_volume()
                        elif gesture_str == "gun":
                            print("检测到手势 'gun'，减小声音")
                            decrease_volume()
                        # 添加其他手势的处理逻辑
                        else:
                            print("手势未变，持续:", gesture_str)
                            consecutive_frames += 1

                            if consecutive_frames > THRESHOLD:
                                print("手指持续，持续:", gesture_str)
                                # 在此处添加持续手势的处理逻辑
                                if gesture_str == "one":
                                    scroll_up()
                                elif gesture_str == "two":
                                    scroll_down()
                                # 添加其他手势的持续处理逻辑
                                elif gesture_str == "three":
                                    print("检测到手势 'three'，持续增加声音")
                                    increase_volume()
                                elif gesture_str == "gun":
                                    print("检测到手势 'gun'，持续减小声音")
                                    decrease_volume()
                                # 添加其他持续手势的处理逻辑

        cv2.imshow('MediaPipe Hands', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()

if __name__ == '__main__':
    detect()
