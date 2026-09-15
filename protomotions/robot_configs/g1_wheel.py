# SPDX-FileCopyrightText: Copyright (c) 2025-2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

"""G1 with eight passive inline-skate wheels: 37 physical DOFs, 29 actions."""

from dataclasses import dataclass, field
from typing import List

from protomotions.robot_configs.g1 import G1RobotConfig


def _actuated_joint_names() -> List[str]:
    # Same policy order as the standard G1; wheel DOFs are interleaved in the MJCF.
    legs = [
        f"{side}_{joint}_joint"
        for side in ("left", "right")
        for joint in (
            "hip_pitch",
            "hip_roll",
            "hip_yaw",
            "knee",
            "ankle_pitch",
            "ankle_roll",
        )
    ]
    waist = [f"waist_{axis}_joint" for axis in ("yaw", "roll", "pitch")]
    arms = [
        f"{side}_{joint}_joint"
        for side in ("left", "right")
        for joint in (
            "shoulder_pitch",
            "shoulder_roll",
            "shoulder_yaw",
            "elbow",
            "wrist_roll",
            "wrist_pitch",
            "wrist_yaw",
        )
    ]
    return legs + waist + arms


@dataclass
class G1WheelRobotConfig(G1RobotConfig):
    actuated_dof_names: List[str] = field(default_factory=_actuated_joint_names)
    default_root_height: float = 0.885

    def __post_init__(self):
        self.asset.asset_file_name = "mjcf/g1_wheel.xml"
        # Keep the wheel as one 24 mm cylinder and round its edges in PhysX.
        self.asset.replace_cylinder_with_capsule = False
        self.asset.isaaclab_convex_margins = {
            f"{side}_wheel_{i}_collision": 0.010
            for side in ("left", "right")
            for i in range(1, 5)
        }
        for side in ("left", "right"):
            self.common_naming_to_robot_body_names[f"all_{side}_foot_bodies"] = [
                f"{side}_ankle_roll_link",
                *[f"{side}_wheel_{i}_link" for i in range(1, 5)],
            ]
        super().__post_init__()
