# Third-party dependencies

이 프로젝트는 ROS 2 Humble 생태계와 OpenCV, Ultralytics YOLO, NumPy 등 외부 라이브러리를 사용합니다. STM32 펌웨어는 STM32CubeF4 HAL/CMSIS에 의존합니다.

본 source-only 제출 트리에서는 ST 제공 `Drivers/` 사본을 제거하고, `parking_robot.ioc` 및 프로젝트 애플리케이션 소스만 포함했습니다. STM32CubeMX/CubeIDE에서 동일 계열 HAL/CMSIS를 생성하여 사용합니다.

외부 라이브러리와 모델을 재배포하는 경우 각 프로젝트의 라이선스 조건을 별도로 확인해야 합니다. 원 개발 저장소에 포함된 외부 코드/라이브러리는 해당 라이선스를 따릅니다.
