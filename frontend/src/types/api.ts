type ResponseCode = 200 | 400 | 401 | 403 | 404 | 409 | 500;

type AuthMethod = 'AUTH' | 'REGISTER';

type GroupMethod =
    | 'CREATE_GROUP'
    | 'ADD_MEMBER_TO_GROUP'
    | 'UPDATE_GROUP_NAME'
    | 'LEAVE_GROUP'
    | 'DELETE_GROUP'
    | 'GET_USER_GROUPS'
    | 'GET_GROUP_DETAILS'
    | 'GET_GROUP_MEMBERS';

type FriendMethod =
    | 'SEND_FRIEND_REQUEST'
    | 'ACCEPT_FRIEND_REQUEST'
    | 'REJECT_FRIEND_REQUEST'
    | 'GET_FRIENDS'
    | 'GET_PENDING_REQUESTS';

export interface BaseResponse {
    code: ResponseCode;
    message: string;
}

export interface BaseRequest {
    method: FriendMethod | GroupMethod;
    token: string;
    body?: Record<string, string>;
}

//group method types
export interface CreateGroupRequest extends BaseRequest {
    method: "CREATE_GROUP";
    body: {
        groupName: string;
    }
}

export interface CreateGroupSuccess extends BaseResponse {
    code: 200
    message: string;
    groupId: string;
}

export interface AddMemberRequest extends BaseRequest {
    method: "ADD_MEMBER_TO_GROUP";
    body:{
        groupId: string;
        username: string;
    }
}

export interface UpdateGroupNameRequest extends BaseRequest {
    method: "UPDATE_GROUP_NAME";
    body:{
        groupId: string;
        newName: string;
    }
}

export interface LeaveGroupRequest extends BaseRequest {
    method: "LEAVE_GROUP";
    body:{
        groupId: string;
    }
}

export interface DeleteGroupRequest extends BaseRequest {
    method: "DELETE_GROUP";
    body:{
        groupId: string;
    }
}

export interface GetUserGroupsRequest extends BaseRequest {
    method: "GET_USER_GROUPS";
    body:{}
}

export interface GroupInfo {
    id: string
    name: string
    creatorId: string
    memberIds: string[]
    createdAt: string
}

export interface GetUserGroupsSuccess extends BaseResponse {
    code: 200,
    groups: GroupInfo[]
}

export interface GetGroupDetailsReqest extends BaseResponse {
    method: "GET_GROUP_DETAILS";
    body: {
        groupId: string;
    }
}

export interface GetGroupDetailsSuccess extends BaseResponse {
    code: 200,
    group: GroupInfo
}

export interface GetGroupMembersRequest extends BaseRequest {
    method: "GET_GROUP_MEMBERS";
    body: {
        groupId: string;
    }
}

export interface FriendInfo {
    uuid: string
    username: string
}

export interface GetGroupMembersSuccess extends BaseResponse {
    code: 200,
    members: FriendInfo[]
}


//auth method types
export interface SendAuthRequest{
    method: AuthMethod;
    body:{
        password: string;
        username: string;
    }
}

export interface AuthSuccessResponse extends BaseResponse {
    code: 200
    message: string;
    token: string;
}

//friend method types
export interface SendFriendRequest extends BaseRequest {
    method: "SEND_FRIEND_REQUEST";
    body: {
        addresseeUsername: string;
    };
}

export interface ProcessFriendRequest extends BaseRequest {
    method: "ACCEPT_FRIEND_REQUEST" | "REJECT_FRIEND_REQUEST";
    body: {
        requester: string;
    };
}

export interface GetFriendsRequest extends BaseRequest {
    method: "GET_FRIENDS" | "GET_PENDING_REQUESTS";
    body: {};
}

type FriendApiRequest = SendFriendRequest | ProcessFriendRequest | GetFriendsRequest;

enum FriendRequestStatus {
    PENDING = 0,
    ACCEPTED = 1,
    REJECTED = 2,
}

export interface PendingRequest {
    requester: string;
    addressee: string;
    status: FriendRequestStatus;
}



export interface GetFriendsSuccessResponse extends BaseResponse {
    code: 200;
    message: string;
    friends: string[];
}

export interface GetPendingRequestsSuccessResponse extends BaseResponse {
    code: 200;
    message: string;
    pendingRequests: PendingRequest[];
}

type FriendNotificationType = "FRIEND_REQUEST";

export interface FriendRequestNotification {
    type: FriendNotificationType;
    from: string; // nazwa_nadawcy
    message: "You have a new friend request";
}


type FriendNotification = FriendRequestNotification;