#pragma once
#include <nlohmann/json.hpp>
#include <memory>

#include "RequestService.h"
#include "../FriendshipService.h"
#include "../UserService.h"
#include "../NotificationService.h"
#include "../../exceptions/missing_required_field_error.h"

using json = nlohmann::json;

class SendFriendRequestService final : public RequestService {
    const std::shared_ptr<FriendshipService> friendshipService;
    const std::shared_ptr<UserService> userService;
    const std::shared_ptr<NotificationService> notificationService;

public:
    explicit SendFriendRequestService(
        std::shared_ptr<FriendshipService> friendshipService,
        std::shared_ptr<UserService> userService,
        std::shared_ptr<NotificationService> notificationService
    ) : friendshipService(std::move(friendshipService)),
        userService(std::move(userService)),
        notificationService(std::move(notificationService)) {}

    std::string getHandledMethodName() override {
        return "SEND_FRIEND_REQUEST";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string addresseeUsername = request.value("addresseeUsername", "");

        if (addresseeUsername.empty())
            throw missing_required_field_error("addresseeUsername");

        friendshipService->sendFriendRequest(userUUID, addresseeUsername);

        const auto addressee = userService->getUserByUsername(addresseeUsername);
        if (addressee.has_value()) {
            json notification;
            notification["type"] = "FRIEND_REQUEST";
            notification["from"] = userService->getUserByUuid(userUUID)->username;
            notification["message"] = "You have a new friend request";

            notificationService->sendNotification(addressee.value().uuid, notification);
        }

        json response;
        response["code"] = 200;
        response["message"] = "Friend request sent successfully";
        return response;
    }
};

class AcceptFriendRequestService final : public RequestService {
    const std::shared_ptr<FriendshipService> friendshipService;
    const std::shared_ptr<UserService> userService;

public:
    explicit AcceptFriendRequestService(
        std::shared_ptr<FriendshipService> friendshipService,
        std::shared_ptr<UserService> userService
    ) : friendshipService(std::move(friendshipService)),
        userService(std::move(userService)) {}

    std::string getHandledMethodName() override {
        return "ACCEPT_FRIEND_REQUEST";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string requesterName = request.value("requester", "");

        if (requesterName.empty())
            throw missing_required_field_error("requester");

        const auto requesterUuid = userService->getUserByUsername(requesterName)->uuid;

        friendshipService->acceptFriendRequest(userUUID, requesterUuid);

        json response;
        response["code"] = 200;
        response["message"] = "Friend request accepted";
        return response;
    }
};

class RejectFriendRequestService final : public RequestService {
    const std::shared_ptr<FriendshipService> friendshipService;
    const std::shared_ptr<UserService> userService;
public:
    explicit RejectFriendRequestService(
        std::shared_ptr<FriendshipService> friendshipService,
        std::shared_ptr<UserService> userService
    ) : friendshipService(std::move(friendshipService)),
        userService(std::move(userService)) {}

    std::string getHandledMethodName() override {
        return "REJECT_FRIEND_REQUEST";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string requesterName = request.value("requester", "");

        if (requesterName.empty())
            throw missing_required_field_error("requester");
        const auto requesterUuid = userService->getUserByUsername(requesterName)->uuid;

        friendshipService->rejectFriendRequest(userUUID, requesterUuid);

        json response;
        response["code"] = 200;
        response["message"] = "Friend request rejected";
        return response;
    }
};

class GetFriendsService final : public RequestService {
    const std::shared_ptr<FriendshipService> friendshipService;
    const std::shared_ptr<UserService> userService;
public:
    explicit GetFriendsService(
        std::shared_ptr<FriendshipService> friendshipService,
        std::shared_ptr<UserService> userService
    ) : friendshipService(std::move(friendshipService)),
        userService(std::move(userService)) {}

    std::string getHandledMethodName() override {
        return "GET_FRIENDS";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const auto friends = friendshipService->getFriends(userUUID);

        json response;
        response["code"] = 200;
        response["message"] = "Friends retrieved successfully";
        response["friends"] = json::array();

        for (const auto& friendUuid : friends)
            response["friends"].push_back(userService->getUserByUuid(friendUuid)->username);

        return response;
    }
};

class GetPendingRequestsService final : public RequestService {
    const std::shared_ptr<FriendshipService> friendshipService;
    const std::shared_ptr<UserService> userService;

public:
    explicit GetPendingRequestsService(
        std::shared_ptr<FriendshipService> friendshipService,
        std::shared_ptr<UserService> userService
    ) : friendshipService(std::move(friendshipService)),
        userService(std::move(userService)) {}

    std::string getHandledMethodName() override {
        return "GET_PENDING_REQUESTS";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const auto pendingRequests = friendshipService->getPendingRequests(userUUID);

        json response;
        response["code"] = 200;
        response["message"] = "Pending requests retrieved successfully";
        response["pendingRequests"] = json::array();

        for (const auto& friendship : pendingRequests) {
            json requestObj;
            requestObj["requester"] = userService->getUserByUuid(friendship.requesterId)->username;
            requestObj["addressee"] = userService->getUserByUuid(friendship.addresseeId)->username;
            requestObj["status"] = friendship.status;
            response["pendingRequests"].push_back(requestObj);
        }

        return response;
    }
};