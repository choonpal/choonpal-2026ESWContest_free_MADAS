#!/usr/bin/env python3
from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'{label}: expected 1 match, got {count}')
    return text.replace(old, new, 1)


# Preserve current YOLO-global / ID0 production tuning and change only the
# fixed-yaw transport contract recovered from parkingbot commit 77b2469.
sync_path = Path('ros2/cooperative_parking_robot/config/sync_params.yaml')
sync = sync_path.read_text(encoding='utf-8')
sync = replace_once(
    sync,
    "    # 메카넘 평행이동: 목표 방향을 보려고 돌지 않고 인양 직후 yaw 유지\n"
    "    hold_initial_yaw: true\n"
    "    yaw_hold_kp: 1.0\n",
    "    # 메카넘 평행이동: 목표 방향을 보려고 돌지 않고 인양 직후 yaw 유지.\n"
    "    # 의도 회전은 금지하되 작은 yaw-hold 보정은 계속 허용한다.\n"
    "    hold_initial_yaw: true\n"
    "    yaw_hold_kp: 1.0\n"
    "    translation_only_transport: true\n",
    'sync transport parameters')
sync = replace_once(
    sync,
    "    # 기존 main 동작 유지: A* 마지막 staging에 도착한 뒤 슬롯 yaw로 회전하고,\n"
    "    # 회전 완료 후 슬롯 중심선 정렬 및 저속 직선 삽입을 수행한다.\n"
    "    final_approach_dist: 0.02\n"
    "    final_pos_tol: 0.02\n"
    "    final_yaw_tol: 0.052\n"
    "    final_lateral_tol: 0.01\n"
    "    final_speed_ratio: 0.30\n"
    "    align_to_slot_yaw: true\n",
    "    # 차량 yaw를 Lift 시점 기준으로 유지한 채 X/Y/대각선 평행이동으로\n"
    "    # 슬롯 중심까지 진입한다. 슬롯 yaw로의 의도 회전 단계는 사용하지 않는다.\n"
    "    final_approach_dist: 0.02\n"
    "    final_pos_tol: 0.02\n"
    "    final_yaw_tol: 0.052\n"
    "    final_lateral_tol: 0.01\n"
    "    final_speed_ratio: 0.30\n"
    "    align_to_slot_yaw: false\n",
    'sync final approach')
sync_path.write_text(sync, encoding='utf-8')


fleet_path = Path(
    'ros2/cooperative_parking_robot/cooperative_parking_robot/fleet_manager_node.py')
fleet = fleet_path.read_text(encoding='utf-8')

fleet = replace_once(
    fleet,
    "    return mode\n\n\nclass FleetManagerNode(Node):\n",
    "    return mode\n\n\n"
    "def join_waypoint_segments(*segments):\n"
    "    \"\"\"Join A* segments without duplicate hand-off waypoints.\"\"\"\n"
    "    joined = []\n"
    "    for segment in segments:\n"
    "        for point in segment:\n"
    "            candidate = (float(point[0]), float(point[1]))\n"
    "            if not joined or math.dist(joined[-1], candidate) > 1e-6:\n"
    "                joined.append(candidate)\n"
    "    return joined\n\n\n"
    "class FleetManagerNode(Node):\n",
    'fleet waypoint helper')

fleet = replace_once(
    fleet,
    "        # 최종 주차는 슬롯 앞 정렬점까지 평행이동한 뒤 회전하고 직선 삽입한다.\n"
    "        self.declare_parameter('use_staged_slot_entry', True)\n"
    "        self.declare_parameter('parking_direction', 'forward')\n",
    "        # Legacy mode는 슬롯 밖 staging에서 회전한다. 제출 기본 모드는\n"
    "        # Lift 시점 yaw를 고정하고 메카넘 X/Y/대각선 이동만 사용한다.\n"
    "        self.declare_parameter('use_staged_slot_entry', True)\n"
    "        self.declare_parameter('translation_only_transport', False)\n"
    "        self.declare_parameter('parking_direction', 'forward')\n",
    'fleet parameter declaration')

fleet = replace_once(
    fleet,
    "        self.use_staged_slot_entry = bool(\n"
    "            self.get_parameter('use_staged_slot_entry').value)\n"
    "        self.parking_direction = str(\n",
    "        self.use_staged_slot_entry = bool(\n"
    "            self.get_parameter('use_staged_slot_entry').value)\n"
    "        self.translation_only_transport = bool(\n"
    "            self.get_parameter('translation_only_transport').value)\n"
    "        self.parking_direction = str(\n",
    'fleet parameter read')

fleet = replace_once(
    fleet,
    "        if self.parking_direction not in (\n"
    "                'minimum_rotation', 'forward', 'reverse'):\n"
    "            raise ValueError(\n"
    "                'parking_direction must be minimum_rotation, forward, or reverse')\n\n"
    "        self.require_ui_confirmation = bool(\n",
    "        if self.parking_direction not in (\n"
    "                'minimum_rotation', 'forward', 'reverse'):\n"
    "            raise ValueError(\n"
    "                'parking_direction must be minimum_rotation, forward, or reverse')\n"
    "        if self.translation_only_transport and self.use_staged_slot_entry:\n"
    "            raise ValueError(\n"
    "                'translation_only_transport requires '\n"
    "                'use_staged_slot_entry=false')\n\n"
    "        self.require_ui_confirmation = bool(\n",
    'fleet fixed-yaw validation')

fleet = replace_once(
    fleet,
    "        compatible.sort(key=lambda item: math.hypot(\n"
    "            item[0].center_x_m - start.x_m,\n"
    "            item[0].center_y_m - start.y_m))\n"
    "        selected_slot = None\n",
    "        compatible.sort(key=lambda item: math.hypot(\n"
    "            item[0].center_x_m - start.x_m,\n"
    "            item[0].center_y_m - start.y_m))\n\n"
    "        # 고정-yaw 운반은 WAITING 영역에서 먼저 뒤로 빠진 뒤,\n"
    "        # X/Y/대각선 평행이동으로 슬롯 중심까지 이동한다.\n"
    "        departure_pose = None\n"
    "        departure_path = None\n"
    "        if self.translation_only_transport:\n"
    "            departure_pose = make_waiting_staging(\n"
    "                start,\n"
    "                self.loaded_footprint.length_m,\n"
    "                self.slot_staging_gap)\n"
    "            departure_path = self.planner.plan(\n"
    "                self.grid, self.grid_w, self.grid_h,\n"
    "                start.position, departure_pose.position)\n"
    "            if departure_path is None:\n"
    "                self.get_logger().error(\n"
    "                    '고정-yaw 대기구역 후진 경로 생성 실패')\n"
    "                return self._set_planning_blocker(\n"
    "                    'WAITING_DEPARTURE_PATH_BLOCKED')\n"
    "            departure_path = join_waypoint_segments(\n"
    "                departure_path, [departure_pose.position])\n\n"
    "        selected_slot = None\n",
    'fleet waiting departure')

fleet = replace_once(
    fleet,
    "            if self.use_staged_slot_entry:\n"
    "                approach_candidates = make_approach_candidates(\n"
    "                    slot,\n"
    "                    self.loaded_footprint.length_m,\n"
    "                    self.slot_staging_gap,\n"
    "                    start.yaw_rad)\n"
    "                if self.parking_direction in ('forward', 'reverse'):\n"
    "                    approach_candidates = [\n"
    "                        candidate for candidate in approach_candidates\n"
    "                        if candidate.parking_direction == self.parking_direction]\n"
    "            else:\n"
    "                # 레거시 모드도 슬롯 yaw는 보존하지만 A* 목표가 바로 중심이다.\n"
    "                approach_candidates = make_approach_candidates(\n"
    "                    slot, self.loaded_footprint.length_m, 0.0, start.yaw_rad)\n",
    "            if self.use_staged_slot_entry:\n"
    "                approach_candidates = make_approach_candidates(\n"
    "                    slot,\n"
    "                    self.loaded_footprint.length_m,\n"
    "                    self.slot_staging_gap,\n"
    "                    start.yaw_rad)\n"
    "            else:\n"
    "                # Direct mode는 슬롯 형상만 사용하고 A* 목표는 슬롯 중심이다.\n"
    "                approach_candidates = make_approach_candidates(\n"
    "                    slot, self.loaded_footprint.length_m, 0.0, start.yaw_rad)\n"
    "            if self.parking_direction in ('forward', 'reverse'):\n"
    "                approach_candidates = [\n"
    "                    candidate for candidate in approach_candidates\n"
    "                    if candidate.parking_direction == self.parking_direction]\n",
    'fleet approach candidates')

fleet = replace_once(
    fleet,
    "                path_goal = (approach.staging_pose.position\n"
    "                             if self.use_staged_slot_entry else slot.center)\n"
    "                candidate_path = self.planner.plan(\n"
    "                    self.grid, self.grid_w, self.grid_h,\n"
    "                    start.position, path_goal)\n",
    "                path_goal = (approach.staging_pose.position\n"
    "                             if self.use_staged_slot_entry else slot.center)\n"
    "                path_start = (departure_pose.position\n"
    "                              if self.translation_only_transport\n"
    "                              else start.position)\n"
    "                candidate_path = self.planner.plan(\n"
    "                    self.grid, self.grid_w, self.grid_h,\n"
    "                    path_start, path_goal)\n",
    'fleet A* start')

fleet = replace_once(
    fleet,
    "                    if math.hypot(\n"
    "                            candidate_path[-1][0] - path_goal[0],\n"
    "                            candidate_path[-1][1] - path_goal[1]) > 1e-6:\n"
    "                        candidate_path.append(path_goal)\n"
    "                selected_slot = slot\n",
    "                    if math.hypot(\n"
    "                            candidate_path[-1][0] - path_goal[0],\n"
    "                            candidate_path[-1][1] - path_goal[1]) > 1e-6:\n"
    "                        candidate_path.append(path_goal)\n"
    "                elif self.translation_only_transport:\n"
    "                    candidate_path = join_waypoint_segments(\n"
    "                        departure_path, candidate_path, [slot.center])\n"
    "                selected_slot = slot\n",
    'fleet fixed-yaw path join')

fleet = replace_once(
    fleet,
    "        sp.pose.position.x = selected_approach.target_pose.x_m\n"
    "        sp.pose.position.y = selected_approach.target_pose.y_m\n"
    "        slot_yaw = selected_approach.target_pose.yaw_rad\n",
    "        sp.pose.position.x = selected_slot.center_x_m\n"
    "        sp.pose.position.y = selected_slot.center_y_m\n"
    "        # 고정-yaw에서는 슬롯 장축 yaw가 아니라 Lift 시점 실제 yaw를\n"
    "        # 최종 목표 자세로 발행해 의도 회전 phase를 만들지 않는다.\n"
    "        slot_yaw = (start.yaw_rad if self.translation_only_transport else\n"
    "                    selected_approach.target_pose.yaw_rad)\n",
    'fleet destination yaw')

fleet = replace_once(
    fleet,
    "        self.get_logger().info(\n"
    "            f'A* 경로 생성: start={start.position}, '\n"
    "            f'footprint={self.loaded_footprint.length_m:.3f}x'\n"
    "            f'{self.loaded_footprint.width_m:.3f}m, '\n"
    "            f'{len(waypoints)}개 waypoint → stage='\n"
    "            f'{selected_approach.staging_pose.position} → '\n"
    "            f'슬롯 {selected_slot.slot_id} '\n",
    "        route_stage = (\n"
    "            f'fixed-yaw departure={departure_pose.position}'\n"
    "            if self.translation_only_transport else\n"
    "            f'stage={selected_approach.staging_pose.position}')\n"
    "        self.get_logger().info(\n"
    "            f'A* 경로 생성: start={start.position}, '\n"
    "            f'footprint={self.loaded_footprint.length_m:.3f}x'\n"
    "            f'{self.loaded_footprint.width_m:.3f}m, '\n"
    "            f'{len(waypoints)}개 waypoint → '\n"
    "            f'{route_stage} → '\n"
    "            f'슬롯 {selected_slot.slot_id} '\n",
    'fleet route log')

helper = (
    "    def _publish_retrieve_route(self, waypoints, waiting_pose):\n"
    "        path = Path()\n"
    "        mission_stamp = self.get_clock().now().to_msg()\n"
    "        path.header.stamp = mission_stamp\n"
    "        path.header.frame_id = 'map'\n"
    "        for wx, wy in waypoints:\n"
    "            ps = PoseStamped()\n"
    "            ps.header.stamp = mission_stamp\n"
    "            ps.header.frame_id = 'map'\n"
    "            ps.pose.position.x = wx\n"
    "            ps.pose.position.y = wy\n"
    "            ps.pose.orientation.w = 1.0\n"
    "            path.poses.append(ps)\n"
    "        destination = PoseStamped()\n"
    "        destination.header.stamp = mission_stamp\n"
    "        destination.header.frame_id = 'map'\n"
    "        destination.pose.position.x = waiting_pose.x_m\n"
    "        destination.pose.position.y = waiting_pose.y_m\n"
    "        destination.pose.orientation.z = math.sin(waiting_pose.yaw_rad / 2.0)\n"
    "        destination.pose.orientation.w = math.cos(waiting_pose.yaw_rad / 2.0)\n"
    "        try:\n"
    "            self.pub_slot_pose.publish(destination)\n"
    "            self.pub_waypoints.publish(path)\n"
    "        except Exception as exc:\n"
    "            self.get_logger().error(f'retrieve plan publish failed: {exc}')\n"
    "            return False\n"
    "        self.path_published = True\n"
    "        self.planning_blocker = None\n"
    "        self.active_plan_stamp_ns = stamp_to_ns(mission_stamp)\n"
    "        self.publish_state()\n"
    "        self.get_logger().info(\n"
    "            f'retrieve path: {self.active_source_slot_id} -> WAITING, '\n"
    "            f'{len(waypoints)} waypoints | '\n"
    "            f'translation_only={getattr(self, \"translation_only_transport\", False)}')\n"
    "        return True\n\n"
)
fleet = replace_once(
    fleet,
    "        return True\n\n    def plan_retrieve_and_publish(self):\n",
    "        return True\n\n" + helper +
    "    def plan_retrieve_and_publish(self):\n",
    'fleet retrieve publisher helper')

fleet = replace_once(
    fleet,
    "        final_pose = record.final_vehicle_pose\n"
    "        extraction = make_extraction_geometry(\n"
    "            source_slot, final_pose,\n"
    "            self.loaded_footprint.length_m,\n"
    "            self.slot_staging_gap,\n"
    "            self.rigid_body_lookahead,\n"
    "            self.slot_fit_long_margin)\n"
    "        planning_grid = clear_source_vehicle(\n"
    "            self.grid, self.grid_w, self.grid_h, self.resolution,\n"
    "            final_pose,\n"
    "            self.vehicle_length,\n"
    "            self.vehicle_width,\n"
    "            self.source_vehicle_fallback_mask,\n"
    "            origin_x_m=getattr(self, 'grid_origin_x_m', 0.0),\n"
    "            origin_y_m=getattr(self, 'grid_origin_y_m', 0.0))\n"
    "        extraction_clear = corridor_is_free(\n",
    "        final_pose = record.final_vehicle_pose\n"
    "        planning_grid = clear_source_vehicle(\n"
    "            self.grid, self.grid_w, self.grid_h, self.resolution,\n"
    "            final_pose,\n"
    "            self.vehicle_length,\n"
    "            self.vehicle_width,\n"
    "            self.source_vehicle_fallback_mask,\n"
    "            origin_x_m=getattr(self, 'grid_origin_x_m', 0.0),\n"
    "            origin_y_m=getattr(self, 'grid_origin_y_m', 0.0))\n\n"
    "        path_length, path_width = footprint_extents_in_slot_axes(\n"
    "            self.loaded_footprint.length_m,\n"
    "            self.loaded_footprint.width_m,\n"
    "            final_pose.yaw_rad)\n"
    "        self.planner.set_footprint(path_length / 2.0, path_width / 2.0)\n\n"
    "        if self.translation_only_transport:\n"
    "            # 실제 주차 yaw를 유지한 채 슬롯에서 평행이동으로 빠져나온다.\n"
    "            waiting_pose = Pose2D(\n"
    "                self.wait_x, self.wait_y, final_pose.yaw_rad)\n"
    "            waiting_staging = make_waiting_staging(\n"
    "                waiting_pose,\n"
    "                self.loaded_footprint.length_m,\n"
    "                self.slot_staging_gap)\n"
    "            astar_path = self.planner.plan(\n"
    "                planning_grid, self.grid_w, self.grid_h,\n"
    "                final_pose.position, waiting_staging.position)\n"
    "            if astar_path is None:\n"
    "                self.get_logger().error(\n"
    "                    'fixed-yaw retrieve-to-waiting A* failed')\n"
    "                return self._set_planning_blocker('ASTAR_NO_PATH')\n"
    "            waypoints = join_waypoint_segments(\n"
    "                [final_pose.position], astar_path,\n"
    "                [waiting_staging.position])\n"
    "            return self._publish_retrieve_route(waypoints, waiting_pose)\n\n"
    "        extraction = make_extraction_geometry(\n"
    "            source_slot, final_pose,\n"
    "            self.loaded_footprint.length_m,\n"
    "            self.slot_staging_gap,\n"
    "            self.rigid_body_lookahead,\n"
    "            self.slot_fit_long_margin)\n"
    "        extraction_clear = corridor_is_free(\n",
    'fleet fixed-yaw retrieve branch')

fleet = replace_once(
    fleet,
    "        path_length, path_width = footprint_extents_in_slot_axes(\n"
    "            self.loaded_footprint.length_m,\n"
    "            self.loaded_footprint.width_m,\n"
    "            final_pose.yaw_rad)\n"
    "        self.planner.set_footprint(path_length / 2.0, path_width / 2.0)\n"
    "        astar_path = self.planner.plan(\n",
    "        astar_path = self.planner.plan(\n",
    'fleet duplicate retrieve footprint')

retrieve_idx = fleet.index('    def plan_retrieve_and_publish(self):')
publish_idx = fleet.index(
    "        path = Path()\n        mission_stamp = self.get_clock().now().to_msg()\n",
    retrieve_idx)
state_idx = fleet.index('    def publish_state(self):', publish_idx)
old_tail = fleet[publish_idx:state_idx]
if "f'{len(waypoints)} waypoints')\n        return True\n\n" not in old_tail:
    raise RuntimeError('fleet retrieve publish tail shape changed')
fleet = (
    fleet[:publish_idx] +
    "        return self._publish_retrieve_route(waypoints, waiting_pose)\n\n" +
    fleet[state_idx:]
)

fleet = replace_once(
    fleet,
    "            'planning_validation_mode': self.planning_validation_mode,\n"
    "            'validation_warnings': list(self.validation_warnings),\n",
    "            'planning_validation_mode': self.planning_validation_mode,\n"
    "            'translation_only_transport': bool(getattr(\n"
    "                self, 'translation_only_transport', False)),\n"
    "            'validation_warnings': list(self.validation_warnings),\n",
    'fleet state telemetry')

fleet_path.write_text(fleet, encoding='utf-8')
