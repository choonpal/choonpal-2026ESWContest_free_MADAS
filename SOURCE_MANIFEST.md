# Source Manifest

본 제출본은 `choonpal/parkingbot` `main`의 commit `6327c92e95fb3c960e42b05d44ea27e01d523077`을 기준으로 생성했습니다.

## 포함

| 경로 | 제출 내용 |
|---|---|
| `ros2/cooperative_parking_robot/cooperative_parking_robot/` | ROS 2 런타임 애플리케이션 소스 |
| `ros2/cooperative_parking_robot/launch/` | 분산 실행 launch |
| `ros2/cooperative_parking_robot/config/*.yaml` | 제어·사이트 설정 |
| `ros2/cooperative_parking_robot/config/*.npz` | CCTV 카메라 calibration 자산 |
| `ros2/cooperative_parking_robot/models/parking_vehicle_yolo11n_seg.pt` | 실제 YOLO11-Seg 차량 인식 weight |
| `ros2/cooperative_parking_robot/cooperative_parking_robot/web/` | package 내부 operator UI 자산 |
| `stm32/parking_robot/Core/` | STM32F401RE 애플리케이션 펌웨어 |
| `stm32/parking_robot/parking_robot.ioc` | MCU peripheral/project configuration |
| `dual_tile_homography_tool/` | 듀얼 CCTV Homography calibration source와 추적된 `.npz` calibration 파일 |
| `tools/` | 배포, preflight, 운용 source/scripts |

## 기준 snapshot에 존재하지 않아 포함하지 못한 런타임 파일

- Homography 결과 `*.npy`: 기준 `parkingbot/main` commit에는 추적된 `.npy` 파일이 없습니다. 현장에서 calibration 도구를 통해 생성하는 결과물입니다.

## 제외

`test/`, 개발 이력 문서, rosbag/log/build 결과, ST vendor HAL/CMSIS는 제출 소스 트리에서 제외했습니다.

본 저장소의 알고리즘/펌웨어/설정/모델/calibration 파일은 위 upstream snapshot에서 그대로 선별한 것이며, 루트 README와 manifest만 제출 목적에 맞게 작성했습니다.
