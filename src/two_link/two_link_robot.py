
#-*- coding: utf-8 -*-

# Copyright (c) 2024 Taisei Hasegawa
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

# [説明]
# 平面2リンクロボットのパラメータを入力すると，
# それに基づいた順運動学，逆運動学を計算するプログラム

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import axes
from typing import Tuple

from two_link_robot_param import TwoLinkRobotParam, TwoLinkRobotColorParam
from util import clamp_angle

class TwoLinkRobot:
    def __init__(self, param: TwoLinkRobotParam = TwoLinkRobotParam(), 
                 color_param: TwoLinkRobotColorParam = TwoLinkRobotColorParam()) -> None:
        self.__param = param
        self.__color_param = color_param

    def forward_kinematics(self, theta1: float, theta2: float) -> Tuple[float, float, float, float]:
        l1 = self.__param.link1
        l2 = self.__param.link2
        o = self.__param.origin
        x1 = o[0] + l1 * np.cos(theta1)
        y1 = o[1] + l1 * np.sin(theta1)
        x2 = x1 + l2 * np.cos(theta1 + theta2)
        y2 = y1 + l2 * np.sin(theta1 + theta2)
        return x1, y1, x2, y2

    def inverse_kinematics(self, end_effecter_x: float, end_effecter_y: float, *, other: bool = True) -> Tuple[float, float]:
        # 見やすくするために変数名を短くしている
        l1:float = self.__param.link1
        l2:float = self.__param.link2
        x:float = end_effecter_x - self.__param.origin[0]
        y:float = end_effecter_y - self.__param.origin[1]

        # そもそも届かない位置にある場合、theta1 = arctan2(y, x), theta2 = 0 とする
        if x**2 + y**2 > (l1 + l2)**2:
            return np.arctan2(y, x), 0

        # 逆運動学の計算
        try:
            theta1 = np.arctan2(y, x) - np.arccos((x**2 + y**2 + l1**2 - l2**2) / (2 * l1 * np.sqrt(x**2 + y**2)))
            theta2 = np.pi - np.arccos((l1**2 + l2**2 - (x**2 + y**2)) / (2 * l1 * l2))
        except:
            theta1 = np.arctan2(y, x)
            theta2 = 0
        return clamp_angle(theta1), clamp_angle(theta2)
    
    def theta1_is_in_range(self, theta1: float) -> bool:
        return self.__param.theta1_min <= theta1 <= self.__param.theta1_max
    
    def theta2_is_in_range(self, theta2: float) -> bool:
        return self.__param.theta2_min <= theta2 <= self.__param.theta2_max
    
    def is_in_range(self, theta1: float, theta2: float) -> bool:
        return self.theta1_is_in_range(theta1) and self.theta2_is_in_range(theta2)
    
    def plot(self, ax:axes.Axes, theta1: float, theta2: float) -> None:
        x1, y1, x2, y2 = self.forward_kinematics(theta1, theta2)
        o = self.__param.origin
        ax.plot([o[0], x1], [o[1], y1], color=self.__color_param.link1_color, linewidth=self.__color_param.link_width, zorder=1)
        ax.plot([x1, x2], [y1, y2], color=self.__color_param.link2_color, linewidth=self.__color_param.link_width, zorder=1)
        ax.add_patch(Circle(o, self.__color_param.joint_size, color=self.__color_param.origin_color, zorder=2))
        ax.add_patch(Circle([x1, y1], self.__color_param.joint_size, color=self.__color_param.joint1_color, zorder=2))
        ax.add_patch(Circle([x2, y2], self.__color_param.joint_size, color=self.__color_param.joint2_color, zorder=2))


def main() -> None:
    param = TwoLinkRobotParam()

    print("Plot 2-link robot" + str(TwoLinkRobotParam()))

    robot = TwoLinkRobot(param)

    _, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_title("2-link robot" + str(param))

    robot.plot(ax, 0, 0)

    plt.show()

    
if __name__ == "__main__":
    main()
