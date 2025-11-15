from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Any


@dataclass
class SKBuiltinStringT:
    string: Optional[str] = None


@dataclass
class SKBuiltinBufferT:
    iLen: Optional[int] = None
    buffer: str = ""


@dataclass
class DisturbTimeSpan:
    BeginTime: Optional[int] = None
    EndTime: Optional[int] = None


@dataclass
class DisturbSetting:
    NightSetting: Optional[int] = None
    NightTime: Optional[DisturbTimeSpan] = None
    AllDaySetting: Optional[int] = None
    AllDayTim: Optional[DisturbTimeSpan] = None


@dataclass
class GmailInfo:
    GmailAcct: Optional[str] = None
    GmailSwitch: Optional[int] = None
    GmailErrCode: Optional[int] = None


@dataclass
class GmailList:
    Count: Optional[int] = None
    List: List[GmailInfo] = field(default_factory=lambda: [])


@dataclass
class UserInfo:
    AlbumBgimgId: str = ""
    AlbumFlag: int = 0
    AlbumStyle: int = 0
    Alias: str = ""
    BindEmail: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    BindMobile: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    BindUin: int = 0
    BitFlag: int = 0
    City: str = ""
    Country: str = ""
    DisturbSetting: DisturbSetting = field(default_factory=lambda: DisturbSetting())
    Experience: int = 0
    FaceBookFlag: int = 0
    Fbtoken: str = ""
    FbuserId: int = 0
    FbuserName: str = ""
    GmailList: GmailList = field(default_factory=lambda: GmailList())
    ImgBuf: SKBuiltinBufferT = field(default_factory=lambda: SKBuiltinBufferT())
    ImgLen: int = 0
    Level: int = 0
    LevelHighExp: int = 0
    LevelLowExp: int = 0
    NickName: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    PersonalCard: int = 0
    PluginFlag: int = 0
    PluginSwitch: int = 0
    Point: int = 0
    Province: str = ""
    Sex: int = 0
    Signature: str = ""
    Status: int = 0
    TxnewsCategory: int = 0
    UserName: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    VerifyFlag: int = 0
    VerifyInfo: str = ""
    Weibo: str = ""
    WeiboFlag: int = 0
    WeiboNickname: str = ""


@dataclass
class LinkedinContactItem:
    LinkedinName: Optional[str] = None
    LinkedinMemberId: Optional[str] = None
    LinkedinPublicUrl: Optional[str] = None


@dataclass
class AdditionalContactList:
    LinkedinContactItem: LinkedinContactItem = field(default_factory=lambda: LinkedinContactItem())


@dataclass
class CustomizedInfo:
    BrandFlag: int = 0
    BrandIconURL: str = ""
    BrandInfo: str = ""
    ExternalInfo: str = ""


@dataclass
class ChatRoomMember:
    BigHeadImgUrl: str = ""
    ChatroomMemberFlag: int = 0
    DisplayName: Optional[str] = None
    InviterUserName: str = ""
    NickName: str = ""
    SmallHeadImgUrl: str = ""
    UserName: str = ""


@dataclass
class NewChatroomData:
    ChatRoomMember: List[ChatRoomMember] = field(default_factory=lambda: [])
    InfoMask: int = 0
    MemberCount: int = 0


@dataclass
class SnsUserInfo:
    SnsFlag: Optional[int] = None
    SnsBgimgId: Optional[str] = None
    SnsBgobjectId: Optional[int] = None
    SnsFlagEx: Optional[int] = None


@dataclass
class PhoneNumListInfo:
    Count: int = 0
    PhoneNumList: List[str] = field(default_factory=lambda: [])


@dataclass
class RoomInfo:
    NickName: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    UserName: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())


@dataclass
class SafeDevice:
    Name: Optional[str] = None
    Uuid: Optional[str] = None
    DeviceType: Optional[str] = None
    CreateTime: Optional[int] = None


@dataclass
class SafeDeviceList:
    Count: Optional[int] = None
    List: List[SafeDevice] = field(default_factory=lambda: [])


@dataclass
class PatternLockInfo:
    PatternVersion: Optional[int] = None
    Sign: Optional[SKBuiltinBufferT] = None
    LockStatus: Optional[int] = None


@dataclass
class Contact:
    AddContactScene: int = 0
    AdditionalContactList: AdditionalContactList = field(default_factory=lambda: AdditionalContactList())
    AlbumBGImgID: str = ""
    AlbumFlag: int = 0
    AlbumStyle: int = 0
    Alias: str = ""
    BigHeadImgUrl: str = ""
    BitMask: int = 0
    BitVal: int = 0
    CardImgUrl: str = ""
    chatRoomBusinessType: int = 0
    ChatRoomData: str = ""
    ChatRoomNotify: int = 0
    ChatRoomOwner: Optional[str] = None
    ChatroomAccessType: int = 0
    ChatroomInfoVersion: int = 0
    ChatroomMaxCount: int = 0
    ChatroomStatus: int = 0
    ChatroomVersion: int = 0
    City: str = ""
    ContactType: int = 0
    Country: str = ""
    CustomizedInfo: CustomizedInfo = field(default_factory=lambda: CustomizedInfo())
    DeleteFlag: int = 0
    DeleteContactScene: int = 0
    Description: str = ""
    DomainList: Any = None
    EncryptUserName: str = ""
    ExtInfo: str = ""
    ExtFlag: int = 0
    HasWeiXinHdHeadImg: int = 0
    HeadImgMd5: str = ""
    IdcardNum: str = ""
    ImgBuf: SKBuiltinBufferT = field(default_factory=lambda: SKBuiltinBufferT())
    ImgFlag: int = 0
    LabelIdlist: str = ""
    Level: int = 0
    MobileFullHash: str = ""
    MobileHash: str = ""
    MyBrandList: str = ""
    NewChatroomData: NewChatroomData = field(default_factory=lambda: NewChatroomData())
    NickName: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    PersonalCard: int = 0
    PhoneNumListInfo: PhoneNumListInfo = field(default_factory=lambda: PhoneNumListInfo())
    Province: str = ""
    Pyinitial: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    QuanPin: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    RealName: str = ""
    Remark: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    RemarkPyinitial: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    RemarkQuanPin: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    RoomInfoCount: int = 0
    RoomInfoList: List[RoomInfo] = field(default_factory=lambda: [])
    Sex: int = 0
    Signature: str = ""
    SmallHeadImgUrl: str = ""
    SnsUserInfo: SnsUserInfo = field(default_factory=lambda: SnsUserInfo())
    Source: int = 0
    UserName: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    SourceExtInfo: str = ""
    VerifyContent: str = ""
    VerifyFlag: int = 0
    VerifyInfo: str = ""
    WeiDianInfo: str = ""
    Weibo: str = ""
    WeiboFlag: int = 0
    WeiboNickname: str = ""


@dataclass
class DelContact:
    DeleteContactScene: int = 0
    UserName: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())


@dataclass
class UserImg:
    BigHeadImgUrl: str = ""
    ImgBuf: Any = None
    ImgLen: int = 0
    ImgMd5: str = ""
    ImgType: int = 0
    SmallHeadImgUrl: str = ""


@dataclass
class FunctionSwitch:
    FunctionId: int = 0
    SwitchValue: int = 0


@dataclass
class UserInfoExt:
    SnsUserInfo: Optional[SnsUserInfo] = None
    MyBrandList: Optional[str] = None
    MsgPushSound: Optional[str] = None
    VoipPushSound: Optional[str] = None
    BigChatRoomSize: Optional[int] = None
    BigChatRoomQuota: Optional[int] = None
    BigChatRoomInvite: Optional[int] = None
    SafeMobile: Optional[str] = None
    BigHeadImgUrl: Optional[str] = None
    SmallHeadImgUrl: Optional[str] = None
    MainAcctType: Optional[int] = None
    ExtXml: Optional[SKBuiltinStringT] = None
    SafeDeviceList: Optional[SafeDeviceList] = None
    SafeDevice: Optional[int] = None
    GrayscaleFlag: Optional[int] = None
    GoogleContactName: Optional[str] = None
    IdcardNum: Optional[str] = None
    RealName: Optional[str] = None
    RegCountry: Optional[str] = None
    Bbppid: Optional[str] = None
    Bbpin: Optional[str] = None
    BbmnickName: Optional[str] = None
    LinkedinContactItem: Optional[LinkedinContactItem] = None
    Kfinfo: Optional[str] = None
    PatternLockInfo: Optional[PatternLockInfo] = None
    SecurityDeviceId: Optional[str] = None
    PayWalletType: Optional[int] = None
    WeiDianInfo: Optional[str] = None
    WalletRegion: Optional[int] = None
    ExtStatus: Optional[int] = None
    F2FpushSound: Optional[str] = None
    UserStatus: Optional[int] = None
    PaySetting: Optional[int] = None


@dataclass
class Message:
    MsgId: int = 0
    FromUserName: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    ToUserName: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    Content: SKBuiltinStringT = field(default_factory=lambda: SKBuiltinStringT())
    CreateTime: int = 0
    MsgType: int = 0
    Status: int = 0
    ImgStatus: int = 0
    ImgBuf: SKBuiltinBufferT = field(default_factory=lambda: SKBuiltinBufferT())
    MsgSource: str = ""
    NewMsgId: int = 0
    MsgSeq: int = 0
    PushContent: str = ""


@dataclass
class WeChatMessage:
    ModUserInfos: List[UserInfo] = field(default_factory=lambda: [])
    ModContacts: List[Contact] = field(default_factory=lambda: [])
    DelContacts: List[DelContact] = field(default_factory=lambda: [])
    ModUserImgs: List[UserImg] = field(default_factory=lambda: [])
    FunctionSwitchs: List[FunctionSwitch] = field(default_factory=lambda: [])
    UserInfoExts: List[UserInfoExt] = field(default_factory=lambda: [])
    AddMsgs: List[Message] = field(default_factory=lambda: [])
    AddSnsBuffer: List[str] = field(default_factory=lambda: [])
    ContinueFlag: int = 0
    KeyBuf: SKBuiltinBufferT = field(default_factory=lambda: SKBuiltinBufferT())
    Status: int = 0
    Continue: int = 0
    Time: int = 0
    UnknownCmdId: str = ""
    Remarks: str = ""
