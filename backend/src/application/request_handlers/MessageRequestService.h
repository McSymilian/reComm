#pragma once
#include <nlohmann/json.hpp>
#include <memory>

#include "RequestService.h"
#include "../MessageService.h"
#include "../../domain/user/UserRepository.h"
#include "../../exceptions/missing_required_field_error.h"

using json = nlohmann::json;

class SendGroupMessageService final : public RequestService {
    const std::shared_ptr<MessageService> messageService;

public:
    explicit SendGroupMessageService(
        std::shared_ptr<MessageService> messageService
    ) : messageService(std::move(messageService)) {}

    std::string getHandledMethodName() override {
        return "SEND_GROUP_MESSAGE";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string groupIdStr = request.value("groupId", "");
        const std::string content = request.value("content", "");

        if (groupIdStr.empty())
            throw missing_required_field_error("groupId");
        if (content.empty())
            throw missing_required_field_error("content");

        const auto groupUuid = UUIDv4::UUID::fromStrFactory(groupIdStr);
        if (groupUuid == nullptr)
            throw std::runtime_error("Invalid group ID");

        const auto messageId = messageService->sendGroupMessage(userUUID, groupUuid, content);

        json response;
        response["code"] = 200;
        response["message"] = "Group message sent successfully";
        response["messageId"] = messageId.str();
        return response;
    }
};

class GetGroupMessagesService final : public RequestService {
    const std::shared_ptr<MessageService> messageService;

public:
    explicit GetGroupMessagesService(
        std::shared_ptr<MessageService> messageService
    ) : messageService(std::move(messageService)) {}

    std::string getHandledMethodName() override {
        return "GET_GROUP_MESSAGES";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string groupIdStr = request.value("groupId", "");

        if (groupIdStr.empty())
            throw missing_required_field_error("groupId");

        const auto groupUuid = UUIDv4::UUID::fromStrFactory(groupIdStr);
        if (groupUuid == nullptr)
            throw std::runtime_error("Invalid group ID");

        const size_t limit = request.value("limit", 100);
        const size_t offset = request.value("offset", 0);

        std::vector<Message> messages;

        if (request.contains("since")) {
            const auto sinceTimestamp = request["since"].get<std::time_t>();
            const auto since = std::chrono::system_clock::from_time_t(sinceTimestamp);
            messages = messageService->getGroupMessages(groupUuid, userUUID, since, limit, offset);
        } else {
            messages = messageService->getRecentGroupMessages(groupUuid, userUUID, limit);
        }

        json messagesJson = json::array();
        for(const auto& msg : messages) {
            json msgJson;
            msgJson["messageId"] = msg.messageId.str();
            msgJson["senderId"] = msg.senderId.str();
            msgJson["receiverId"] = msg.receiverId.str();
            msgJson["type"] = (msg.type == MessageType::GROUP) ? "GROUP" : "PRIVATE";
            msgJson["content"] = msg.content;
            msgJson["sentAt"] = std::chrono::system_clock::to_time_t(msg.sentAt);
            msgJson["deliveredAt"] = std::chrono::system_clock::to_time_t(msg.deliveredAt);
            messagesJson.push_back(msgJson);
        }

        json response;
        response["code"] = 200;
        response["messages"] = messagesJson;
        response["count"] = messages.size();
        return response;
    }
};

class SendPrivateMessageService final : public RequestService {
    const std::shared_ptr<MessageService> messageService;
    const std::shared_ptr<UserRepository> userRepo;

public:
    explicit SendPrivateMessageService(
        std::shared_ptr<MessageService> messageService,
        std::shared_ptr<UserRepository> userRepo
    ) : messageService(std::move(messageService)),
        userRepo(std::move(userRepo)) {}

    std::string getHandledMethodName() override {
        return "SEND_PRIVATE_MESSAGE";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string receiverUsername = request.value("receiverUsername", "");
        const std::string content = request.value("content", "");

        if (receiverUsername.empty())
            throw missing_required_field_error("receiverUsername");
        if (content.empty())
            throw missing_required_field_error("content");

        const auto receiverUser = userRepo->findByUsername(receiverUsername);
        if (!receiverUser.has_value())
            throw user_not_found_error();

        const auto messageId = messageService->sendPrivateMessage(userUUID, receiverUser->uuid, content);

        json response;
        response["code"] = 200;
        response["message"] = "Private message sent successfully";
        response["messageId"] = messageId.str();
        return response;
    }
};

class GetPrivateMessagesService final : public RequestService {
    const std::shared_ptr<MessageService> messageService;
    const std::shared_ptr<UserRepository> userRepo;

public:
    explicit GetPrivateMessagesService(
        std::shared_ptr<MessageService> messageService,
        std::shared_ptr<UserRepository> userRepo
    ) : messageService(std::move(messageService)),
        userRepo(std::move(userRepo)) {}

    std::string getHandledMethodName() override {
        return "GET_PRIVATE_MESSAGES";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string otherUsername = request.value("otherUsername", "");

        if (otherUsername.empty())
            throw missing_required_field_error("otherUsername");

        const auto otherUser = userRepo->findByUsername(otherUsername);
        if (!otherUser.has_value())
            throw user_not_found_error();

        const size_t limit = request.value("limit", 100);
        const size_t offset = request.value("offset", 0);

        std::vector<Message> messages;

        if (request.contains("since")) {
            const auto sinceTimestamp = request["since"].get<std::time_t>();
            const auto since = std::chrono::system_clock::from_time_t(sinceTimestamp);
            messages = messageService->getPrivateMessages(userUUID, otherUser->uuid, since, limit, offset);
        } else {
            messages = messageService->getRecentPrivateMessages(userUUID, otherUser->uuid, limit);
        }

        json messagesJson = json::array();
        for(const auto& msg : messages) {
            json msgJson;
            msgJson["messageId"] = msg.messageId.str();
            msgJson["senderId"] = msg.senderId.str();
            msgJson["receiverId"] = msg.receiverId.str();
            msgJson["type"] = (msg.type == MessageType::GROUP) ? "GROUP" : "PRIVATE";
            msgJson["content"] = msg.content;
            msgJson["sentAt"] = std::chrono::system_clock::to_time_t(msg.sentAt);
            msgJson["deliveredAt"] = std::chrono::system_clock::to_time_t(msg.deliveredAt);
            messagesJson.push_back(msgJson);
        }

        json response;
        response["code"] = 200;
        response["messages"] = messagesJson;
        response["count"] = messages.size();
        return response;
    }
};

class SendMessageService final : public RequestService {
    const std::shared_ptr<MessageService> messageService;

public:
    explicit SendMessageService(
        std::shared_ptr<MessageService> messageService
    ) : messageService(std::move(messageService)) {}

    std::string getHandledMethodName() override {
        return "SEND_MESSAGE";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string groupIdStr = request.value("groupId", "");
        const std::string content = request.value("content", "");

        if (groupIdStr.empty())
            throw missing_required_field_error("groupId");
        if (content.empty())
            throw missing_required_field_error("content");

        const auto groupUuid = UUIDv4::UUID::fromStrFactory(groupIdStr);
        if (groupUuid == nullptr)
            throw std::runtime_error("Invalid group ID");

        const auto messageId = messageService->sendGroupMessage(userUUID, groupUuid, content);

        json response;
        response["code"] = 200;
        response["message"] = "Message sent successfully";
        response["messageId"] = messageId.str();
        return response;
    }
};

class GetRecentMessagesService final : public RequestService {
    const std::shared_ptr<MessageService> messageService;

public:
    explicit GetRecentMessagesService(
        std::shared_ptr<MessageService> messageService
    ) : messageService(std::move(messageService)) {}

    std::string getHandledMethodName() override {
        return "GET_RECENT_MESSAGES";
    }

    json handleRequest(const json& request, const UUIDv4::UUID userUUID) override {
        const std::string groupIdStr = request.value("groupId", "");

        if (groupIdStr.empty())
            throw missing_required_field_error("groupId");

        const auto groupUuid = UUIDv4::UUID::fromStrFactory(groupIdStr);
        if (groupUuid == nullptr)
            throw std::runtime_error("Invalid group ID");

        const size_t limit = request.value("limit", 100);

        const auto messages = messageService->getRecentGroupMessages(groupUuid, userUUID, limit);

        json messagesJson = json::array();
        for(const auto& msg : messages) {
            json msgJson;
            msgJson["messageId"] = msg.messageId.str();
            msgJson["senderId"] = msg.senderId.str();
            msgJson["receiverId"] = msg.receiverId.str();
            msgJson["type"] = (msg.type == MessageType::GROUP) ? "GROUP" : "PRIVATE";
            msgJson["content"] = msg.content;
            msgJson["sentAt"] = std::chrono::system_clock::to_time_t(msg.sentAt);
            msgJson["deliveredAt"] = std::chrono::system_clock::to_time_t(msg.deliveredAt);
            messagesJson.push_back(msgJson);
        }

        json response;
        response["code"] = 200;
        response["messages"] = messagesJson;
        response["count"] = messages.size();
        return response;
    }
};

