#pragma once
#include <nlohmann/json.hpp>
#include <memory>

#include "RequestService.h"
#include "../FriendshipService.h"
#include "../JwtService.h"
#include "../../exceptions/invalid_token_error.h"
#include "../../exceptions/missing_required_field_error.h"

using json = nlohmann::json;

// Wysyłanie zaproszenia do znajomych
class SendFriendRequestService final : public RequestService {
    const std::shared_ptr<FriendshipService> friendshipService;
    const std::shared_ptr<JwtService> jwtService;

public:
    explicit SendFriendRequestService(
        std::shared_ptr<FriendshipService> friendshipService,
        std::shared_ptr<JwtService> jwtService
    ) : friendshipService(std::move(friendshipService)),
        jwtService(std::move(jwtService)) {}

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

        auto requesterUuid = JwtService::getUuidFromToken(token);
        if (!requesterUuid.has_value())
            throw invalid_token_error();

        friendshipService->sendFriendRequest(requesterUuid.value(), addresseeUsername);

        json response;
        response["code"] = 200;
        response["message"] = "Friend request sent successfully";
        return response;
    }
};

// Akceptowanie zaproszenia do znajomych
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

        auto userUuid = JwtService::getUuidFromToken(token);
        if (!userUuid.has_value())
            throw invalid_token_error();

        auto requesterUuid = UUIDv4::UUID::fromStrFactory(requesterUuidStr);

        friendshipService->acceptFriendRequest(userUuid.value(), requesterUuid);

        json response;
        response["code"] = 200;
        response["message"] = "Friend request accepted";
        return response;
    }
};

// Odrzucanie zaproszenia do znajomych
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

        auto userUuid = JwtService::getUuidFromToken(token);
        if (!userUuid.has_value())
            throw invalid_token_error();

        auto requesterUuid = UUIDv4::UUID::fromStrFactory(requesterUuidStr);

        friendshipService->rejectFriendRequest(userUuid.value(), requesterUuid);

        json response;
        response["code"] = 200;
        response["message"] = "Friend request rejected";
        return response;
    }
};

// Pobieranie listy znajomych
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

        auto userUuid = JwtService::getUuidFromToken(token);
        if (!userUuid.has_value())
            throw invalid_token_error();

        auto friends = friendshipService->getFriends(userUuid.value());

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

// Pobieranie oczekujących zaproszeń
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

        auto userUuid = JwtService::getUuidFromToken(token);
        if (!userUuid.has_value())
            throw invalid_token_error();

        auto pendingRequests = friendshipService->getPendingRequests(userUuid.value());

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

