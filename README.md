# MADAS

**MADAS (Multi-Agent Distributed Autonomous System)** is a cooperative autonomous parking and retrieval system developed for the **2026 Embedded Software Contest — Free Theme Division**.

This submission is based on the team's `parkingbot` project and combines embedded control, computer vision, ROS 2, and multi-robot cooperative control.

## Project Overview

MADAS uses two parking robots (Front/Rear) to cooperatively approach, grip, transport, park, and retrieve a vehicle. The system integrates global vehicle localization from camera-based perception with local robot sensing and embedded motor control.

### Core Features

- YOLO-based vehicle detection / segmentation and vehicle-center estimation
- Camera homography for image-to-ground coordinate conversion
- Global vehicle pose estimation for cooperative transport when robot-mounted markers may be occluded
- Front/Rear cooperative rigid-body motion control
- ArUco-based relative localization where available
- ROS 2 Humble distributed software architecture
- Jetson / Raspberry Pi perception and coordination nodes
- STM32-based motor, encoder, ultrasonic sensor, and gripper control
- Automated parking and authenticated vehicle retrieval workflow

## System Architecture

```text
Overhead Camera / Vision
        |
        v
YOLO Vehicle Perception
        |
        v
Ground / Global Coordinates
        |
        v
Fleet & Mission Manager (ROS 2)
   |                    |
   v                    v
Front Robot          Rear Robot
Raspberry Pi         Raspberry Pi
   |                    |
   v                    v
STM32                STM32
Motor / Encoder      Motor / Encoder
Ultrasonic / Grip    Ultrasonic / Grip
```

## Source Code

The original development repository is linked in this submission repository under `parkingbot/` at the exact submission snapshot.

- Source project: `choonpal/parkingbot`
- Submission snapshot: `6327c92e95fb3c960e42b05d44ea27e01d523077`

## Main Software Stack

- ROS 2 Humble
- Python / C / C++
- YOLO11 segmentation / detection
- OpenCV / Homography
- ArUco
- Raspberry Pi 4
- NVIDIA Jetson
- STM32F401RE

## Competition

2026 제24회 임베디드SW경진대회 자유공모 부문 제출용 저장소입니다.

> Repository name follows the contest submission naming convention: `2026ESWContest_free_팀명`.
