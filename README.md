# Adaptive Valet Bot

**2026 임베디드 소프트웨어 경진대회 자유공모 부문 · Team MADAS**

두 대의 주차 로봇이 차량의 전·후방에 접근해 협동 제어하는 ROS 2 기반 지능형 주차 시스템의 제출용 소스코드 저장소입니다. 이 저장소는 개발 저장소 `choonpal/parkingbot`의 `main`을 기준으로, 심사에 필요한 실제 프로그램 소스만 분리한 스냅샷입니다.

## Source snapshot

- Upstream: `choonpal/parkingbot`
- Branch 기준: `main`
- Snapshot commit: `6327c92e95fb3c960e42b05d44ea27e01d523077`
- ROS 2: Humble
- MCU: STM32F401RE

## 핵심 파이프라인

```text
Dual CCTV
    │
    ├─ YOLO11-Seg → 차량 mask 중심 추정
    ├─ Homography → map/global 좌표 변환
    └─ ArUco → Front/Rear 로봇 관측
     │
     ▼
         Fleet Manager
     │
A* / Mission
     │
    ┌──────────┴──────────┐
    ▼                     ▼
Front Robot           Rear Robot
    │                     │
    ├──── relative / rigid-body sync ────┤
    │                     │
Raspberry Pi          Raspberry Pi
    │ UART                │ UART
    ▼                     ▼
  STM32                 STM32
    │                     │
 Drive/Grip            Drive/Grip
```

강체 협동주행 단계에서는 차량에 부착된 마커가 아니라, 천장 카메라의 YOLO11-Seg 차량 검출 결과에서 얻은 차량 중심을 Homography로 `map` 좌표계에 투영해 global 위치 피드백으로 사용합니다. 로봇 간 상대 정렬은 Rear ID0 ArUco 및 로봇 상태 추정을 별도의 상대 제어 정보로 사용하도록 분리되어 있습니다.

## 제출 소스 구조

```text
ros2/cooperative_parking_robot/
├── cooperative_parking_robot/   # 인지, 위치추정, 계획, 협동제어, UI, 통신
├── config/                      # YAML 운용 파라미터
├── launch/                      # Jetson / Front / Rear 실행 구성
├── resource/
├── scripts/                     # 운용·빌드 보조 스크립트
├── package.xml
├── setup.cfg
└── setup.py

stm32/parking_robot/
├── Core/                        # 실제 MCU 제어 펌웨어
├── cmake/
├── parking_robot.ioc
└── CMakeLists.txt

dual_tile_homography_tool/       # 듀얼 CCTV Homography 보정 도구
tools/                           # 배포·preflight·운용 도구
```

## 주요 구현

- YOLO11-Seg 기반 차량 인식과 segmentation mask 중심 산출
- 카메라 보정 및 Homography 기반 CCTV → BEV/map 좌표 변환
- 듀얼 CCTV 관측 병합과 차량 global pose feedback
- ArUco 기반 Front/Rear 상대 자세 관측
- A* 기반 주차/출차 경로 생성 및 Fleet mission 관리
- Front/Rear 강체 기구학 및 relative synchronization
- PID/Kalman 기반 상대 오차 보정
- 차량 global 위치와 로봇 상대 위치를 분리한 협동주행 제어
- UART 스케줄링, heartbeat 및 STM32 브리지
- STM32 모터·엔코더·초음파·그리퍼 제어
- Jetson 기반 operator web UI

## 제출본에서 제외한 항목

- 자동 회귀/단위 테스트 (`test/`)
- 개발 과정의 ADR, change log 및 실험 문서
- 학습된 YOLO weight (`*.pt`)
- 현장별 생성 calibration 결과 (`*.npz`, Homography `*.npy`)
- STM32CubeF4의 ST 제공 HAL/CMSIS vendor source
- rosbag, 로그, 빌드 산출물 및 임시 실험 파일

모델 weight와 현장 calibration 값은 실행 환경에 종속되는 결과물이며, 본 저장소에서는 이를 사용하는 프로그램 소스와 보정 도구를 공개합니다.

## Build

```bash
mkdir -p ~/esw_ws/src
cp -r ros2/cooperative_parking_robot ~/esw_ws/src/
cd ~/esw_ws
colcon build --symlink-install
source install/setup.bash
```

STM32 firmware는 `stm32/parking_robot/parking_robot.ioc`를 기준으로 STM32CubeMX/CubeIDE에서 STM32CubeF4 HAL/CMSIS를 생성한 뒤 빌드합니다.

파일별 제출 범위는 [`SOURCE_MANIFEST.md`](SOURCE_MANIFEST.md), 외부 의존성은 [`THIRD_PARTY.md`](THIRD_PARTY.md)를 참고하십시오.
