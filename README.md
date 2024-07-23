# kiosk_amusement

## 라즈베리 파이 환경 설정

### 화면 설정
디스플레이 회전

    sudo nano /boot/config.txt

    #dtoverlay=vc4-kms-v3d     # 주석 처리
    display_hdmi_rotate=1      # 추가

디스플레이 해상도 설정

    sudo nano /boot/config.txt

    hdmi_group=2
    hdmi_mode=87                  # 설정 숫자에 따라 화면 크기변화
    hdmi_cvt=1024 600 60 6 0 0 0  # mode와 맞춰야함
    hdmi_drive=1
    hdimi_force_hotplug=1

터치 회전

    sudo nano /usr/share/X11/xorg.conf.d/40-libinput.conf

    Section "InputClass"
        Identifier "libinput touchscreen catchall"
        MatchIsTouchscreen "on"
        Option "TransformationMatrix" "0 1 0 -1 0 1 0 0 1"
        MatchDevicePath "/dev/input/event*"
        Driver "libinput"
    EndSection

    90° = 옵션 "TransformationMatrix" "0 1 0 -1 0 1 0 0 1"
    180° = 옵션 "TransformationMatrix" "-1 0 1 0 -1 1 0 0 1"
    270° = 옵션 "TransformationMatrix" "0 -1 1 1 0 0 0 0 1"


### opencv module 재설치

    pip uninstall opencv-python
    pip install opencv-python-headless

