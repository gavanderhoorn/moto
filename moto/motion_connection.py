# Copyright 2020 Norwegian University of Science and Technology.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Union

from moto.simple_message_connection import SimpleMessageConnection
from moto.simple_message import (
    Header,
    MsgType,
    CommType,
    ReplyType,
    MotoMotionCtrl,
    CommandType,
    SimpleMessage,
    JointTrajPtFull,
    JointTrajPtFullEx,
    SimpleMessageError,
)


class MotionConnection(SimpleMessageConnection):

    TCP_PORT_MOTION = 50240

    def __init__(self, ip_address):
        super().__init__((ip_address, self.TCP_PORT_MOTION))

    def _send_and_recv_request(self, command: CommandType, groupno=-1) -> SimpleMessage:
        request = SimpleMessage(
            Header(
                MsgType.MOTO_MOTION_CTRL, CommType.SERVICE_REQUEST, ReplyType.INVALID
            ),
            MotoMotionCtrl(groupno=groupno, sequence=-1, command=command),
        )
        response: SimpleMessage = self.send_and_recv(request)
        return response

    def check_motion_ready(self):
        return self._send_and_recv_request(CommandType.CHECK_MOTION_READY)

    def check_queue_count(self, groupno: int):
        return self._send_and_recv_request(CommandType.CHECK_QUEUE_CNT, groupno)

    def stop_motion(self):
        return self._send_and_recv_request(CommandType.STOP_MOTION)

    def start_servos(self):
        return self._send_and_recv_request(CommandType.START_SERVOS)

    def stop_servos(self):
        return self._send_and_recv_request(CommandType.STOP_SERVOS)

    def reset_alarm(self):
        return self._send_and_recv_request(CommandType.RESET_ALARM)

    def start_traj_mode(self):
        return self._send_and_recv_request(CommandType.START_TRAJ_MODE)

    def stop_traj_mode(self):
        return self._send_and_recv_request(CommandType.STOP_TRAJ_MODE)

    def disconnect(self):
        return self._send_and_recv_request(CommandType.DISCONNECT)

    def send_joint_trajectory_point(
        self, joint_trajectory_point: Union[JointTrajPtFull, JointTrajPtFullEx]
    ) -> SimpleMessage:
        if isinstance(joint_trajectory_point, JointTrajPtFull):
            msg_type = MsgType.JOINT_TRAJ_PT_FULL
        elif isinstance(joint_trajectory_point, JointTrajPtFullEx):
            msg_type = MsgType.MOTO_JOINT_TRAJ_PT_FULL_EX
        else:
            raise SimpleMessageError("Not valid joint_trajectory_point.")
        msg = SimpleMessage(
            Header(
                msg_type=msg_type,
                comm_type=CommType.SERVICE_REQUEST,
                reply_type=ReplyType.INVALID,
            ),
            joint_trajectory_point,
        )
        return self.send_and_recv(msg)
