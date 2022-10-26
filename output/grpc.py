from colorama import init, Fore
from messages.chat import ChatMessage
from messages.gift import GiftMessage
from messages.member import MemberMessage

from output.IOutput import IOutput

import grpc
import dmgrpc.grpc_pb2 as pb2
import dmgrpc.grpc_pb2_grpc as pb2_grpc 
from config.helper import config
import json

RED = Fore.RED
GREEN = Fore.GREEN
BLUE = Fore.BLUE
CYAN = Fore.CYAN
MAGENTA = Fore.MAGENTA
YELLOW = Fore.YELLOW
WHITE = Fore.WHITE
RESET = Fore.RESET
init()


LiveMessagerStub = None

class GrpcManager:

    def __init__(self,channel:'grpc.Channel') -> None:
        self.channel = channel

    def terminate(self):
        self.channel.close()

def init_grpcmanager():
    global LiveMessagerStub
    _config = config()['grpc']
    ip_address = _config['host']
    port = _config['port']
    channel = grpc.insecure_channel(f"{ip_address}:{port}")
    LiveMessagerStub = pb2_grpc.LiveMessagerStub(channel)
    return GrpcManager(channel)


class Grpc(IOutput):
    def chat_output(self, msg:'ChatMessage'):
        try:
            content = msg.content
            user = msg.user()
            image = user.avatarThumb
            imageurl = image.urlList[0]
            print(f"\n{BLUE}[+] {msg} {RESET}")
        
            msginfo={
                'type':'聊天',
                'id':user.id,
                'nickname':user.nickname,
                'content':content,
                'imageurl':imageurl,
            }
            LiveMessagerStub.HandleJsonMsg.future(
                pb2.StringMsg(type='抖音消息',jsonStr=json.dumps(msginfo))
                )
        except Exception as e:
            print('error:',e)
        # print(f'{user.nickname}:')
        
    # def like_output(self, msg):
    #     print(f"\n{CYAN}[+] {msg} {RESET}")

    def member_output(self, msg:'MemberMessage'):
        print(f"\n{RED}[+] {msg} {RESET}")
        user = msg.user()
        image = user.avatarThumb
        imageurl = image.urlList[0]

        msginfo={
            'type':'进入',
            'id':user.id,
            'nickname':user.nickname,
            'imageurl':imageurl,
        }
        LiveMessagerStub.HandleJsonMsg.future(
            pb2.StringMsg(type='抖音消息',jsonStr=json.dumps(msginfo))
            )
        # print(f'nickname:{user.nickname} id:{user.id} imageurl:{imageurl}')

    # def social_output(self, msg):
    #     print(f"\n{GREEN}[+] {msg} {RESET}")

    def gift_output(self, msg:'GiftMessage'):
        print(f"\n{MAGENTA}[+] {msg} {RESET}")
        user = msg.user()
        msginfo={
            'type':'礼物',
            'id':user.id,
            'nickname':user.nickname,
            'gift':{msg.extra_info()},
        }
        LiveMessagerStub.HandleJsonMsg.future(
            pb2.StringMsg(type='抖音消息',jsonStr=json.dumps(msginfo))
            )

    # def userseq_output(self, msg):
    #     print(f"\n{YELLOW}[+] {msg} {RESET}")

    # def control_output(self, msg):
    #     print(f"\n{CYAN}[+] {msg} {RESET}")

    # def fansclub_output(self, msg):
    #     print(f"\n{GREEN}[+] {msg} {RESET}")
