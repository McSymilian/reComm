#pragma once
#include <nlohmann/json.hpp>
#include <memory>

#include "RequestService.h"
#include "../FriendshipService.h"
#include "../JwtService.h"
#include "../UserService.h"
#include "../NotificationService.h"
#include "../../exceptions/invalid_token_error.h"
#include "../../exceptions/missing_required_field_error.h"

using json = nlohmann::json;

class SendFriendRequestService final : public RequestService {
    const std::shared_ptr<FriendshipService> friendshipService;
    const std::shared_ptr<JwtService> jwtService;
    const std::shared_ptr<UserService> userService;
    const std::shared_ptr<NotificationService> notificationService;

public:
    explicit SendFriendRequestService(
        std::shared_ptr<FriendshipService> friendshipService,
        std::shared_ptr<JwtService> jwtService,
        std::shared_ptr<UserService> userService,
        std::shared_ptr<NotificationService> notificationService
    ) : friendshipService(std::move(friendshipService)),
        jwtService(std::move(jwtService)),
        userService(std::move(userService)),
        notificationService(std::move(notificationService)) {}

    std::string getHandledMethodName() override {
        return "SEND_FRIEND_REQUEST";
    }

    json handleRequest(const json& request) override {
        const std::string token = request.value("token", "");
        const std::string addresseeUsername = request.value("addresseeUsername", "");

        if (token.empty())
            throw missing_required_field_error("token");
        if (addresseeUsername.empty())
            throw missing_required_field_error("addresseeUsername");

        if (!jwtService->verifyToken(token))
            throw invalid_token_error();

        const auto requesterUuid = JwtService::getUuidFromToken(token);
        if (!requesterUuid.has_value())
            throw invalid_token_error();

        friendshipService->sendFriendRequest(requesterUuid.value(), addresseeUsername);

        const auto addressee = userService->getUserByUsername(addresseeUsername);
        if (addressee.has_value()) {
            json notification;
            notification["type"] = "FRIEND_REQUEST";
            notification["from"] = requesterUuid.value().str();
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
    const std::shared_ptr<JwtService> jwtService;

public:
    explicit AcceptFriendRequestService(
        std::shared_ptr<FriendshipService> friendshipService,
        std::shared_ptr<JwtService> jwtService
    ) : friendshipService(std::move(friendshipService)),
        jwtService(std::move(jwtService)) {}

    std::string getHandledMethodName() override {
        return "ACCEPT_FRIEND_REQUEST";
    }

    json handleRequest(const json& request) override {
        const std::string token = request.value("token", "");
        const std::string requesterUuidStr = request.value("requesterUuid", "");

        if (token.empty())
            throw missing_required_field_error("token");
        if (requesterUuidStr.empty())
            throw missing_required_field_error("requesterUuid");

        if (!jwtService->verifyToken(token))
            throw invalid_token_error();

        const auto userUuid = JwtService::getUuidFromToken(token);
        if (!userUuid.has_value())
            throw invalid_token_error();

        const auto requesterUuid = UUIDv4::UUID::fromStrFactory(requesterUuidStr);

        friendshipService->acceptFriendRequest(userUuid.value(), requesterUuid);

        json response;
        response["code"] = 200;
        response["message"] = "Friend request accepted";
        return response;
    }
};

class RejectFriendRequestService final : public RequestService {
    const std::shared_ptr<FriendshipService> friendshipService;
    const std::shared_ptr<JwtService> jwtService;

public:
    explicit RejectFriendRequestService(
        std::shared_ptr<FriendshipService> friendshipService,
        std::shared_ptr<JwtService> jwtService
    ) : friendshipService(std::move(friendshipService)),
        jwtService(std::move(jwtService)) {}

    std::string getHandledMethodName() override {
        return "REJECT_FRIEND_REQUEST";
    }

    json handleRequest(const json& request) override {
        const std::string token = request.value("token", "");
        const std::string requesterUuidStr = request.value("requesterUuid", "");

        if (token.empty())
            throw missing_required_field_error("token");
        if (requesterUuidStr.empty())
            throw missing_required_field_error("requesterUuid");

        if (!jwtService->verifyToken(token))
            throw invalid_token_error();

        const auto userUuid = JwtService::getUuidFromToken(token);
        if (!userUuid.has_value())
            throw invalid_token_error();

        const auto requesterUuid = UUIDv4::UUID::fromStrFactory(requesterUuidStr);

        friendshipService->rejectFriendRequest(userUuid.value(), requesterUuid);

        json response;
        response["code"] = 200;
        response["message"] = "Friend request rejected";
        return response;
    }
};

class GetFriendsService final : public RequestService {
    const std::shared_ptr<FriendshipService> friendshipService;
    const std::shared_ptr<JwtService> jwtService;

public:
    explicit GetFriendsService(
        std::shared_ptr<FriendshipService> friendshipService,
        std::shared_ptr<JwtService> jwtService
    ) : friendshipService(std::move(friendshipService)),
        jwtService(std::move(jwtService)) {}

    std::string getHandledMethodName() override {
        return "GET_FRIENDS";
    }

    json handleRequest(const json& request) override {
        const std::string token = request.value("token", "");

        if (token.empty())
            throw missing_required_field_error("token");

        if (!jwtService->verifyToken(token))
            throw invalid_token_error();

        const auto userUuid = JwtService::getUuidFromToken(token);
        if (!userUuid.has_value())
            throw invalid_token_error();

        const auto friends = friendshipService->getFriends(userUuid.value());

        json response;
        response["code"] = 200;
        response["message"] = "Friends retrieved successfully";
        response["friends"] = json::array();

        for (const auto& friendUuid : friends) {
            response["friends"].push_back(friendUuid.str());
        }

        return response;
    }
};

class GetPendingRequestsService final : public RequestService {
    const std::shared_ptr<FriendshipService> friendshipService;
    const std::shared_ptr<JwtService> jwtService;

public:
    explicit GetPendingRequestsService(
        std::shared_ptr<FriendshipService> friendshipService,
        std::shared_ptr<JwtService> jwtService
    ) : friendshipService(std::move(friendshipService)),
        jwtService(std::move(jwtService)) {}

    std::string getHandledMethodName() override {
        return "GET_PENDING_REQUESTS";
    }

    json handleRequest(const json& request) override {
        const std::string token = request.value("token", "");

        if (token.empty())
            throw missing_required_field_error("token");

        if (!jwtService->verifyToken(token))
            throw invalid_token_error();

        const auto userUuid = JwtService::getUuidFromToken(token);
        if (!userUuid.has_value())
            throw invalid_token_error();

        const auto pendingRequests = friendshipService->getPendingRequests(userUuid.value());

        json response;
        response["code"] = 200;
        response["message"] = "Pending requests retrieved successfully";
        response["pendingRequests"] = json::array();

        for (const auto& friendship : pendingRequests) {
            json requestObj;
            requestObj["requesterId"] = friendship.requesterId.str();
            requestObj["addresseeId"] = friendship.addresseeId.str();
            requestObj["status"] = friendship.status;
            response["pendingRequests"].push_back(requestObj);
        }

        return response;
    }
};