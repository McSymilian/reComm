#pragma once

#include <string>
#include <chrono>
#include <algorithm>
#include <optional>
#include "uuid_v4.h"
#include <nlohmann/json.hpp>
#include <fstream>
#include "../domain/message/MessageRepository.h"
#include <vector>
#if __has_include(<filesystem>)
    #include <filesystem>
    namespace fs = std::filesystem;
#elif __has_include(<experimental/filesystem>)
    #include <experimental/filesystem>
    namespace fs = std::experimental::filesystem;
#else
    #error "No filesystem support"
#endif

class FileMessageRepository final : public MessageRepository {
    fs::path filePath;
    static constexpr std::string DB_FILE = "messages.json";

    static nlohmann::json messageToJson(const Message& message) {
        return {
                {"messageId", message.messageId.str()},
                {"senderId", message.senderId.str()},
                {"receiverId", message.receiverId.str()},
                {"type", message.type == MessageType::GROUP ? "GROUP" : "PRIVATE"},
                {"senderName", message.senderName},
                {"content", message.content},
                {"sentAt", std::chrono::system_clock::to_time_t(message.sentAt)},
                {"deliveredAt", std::chrono::system_clock::to_time_t(message.deliveredAt)}
        };
    }

    static std::optional<Message> jsonToMessage(const nlohmann::json& json) {
        try {
            const auto messageIdValue = json.value("messageId", "");
            const auto senderIdValue = json.value("senderId", "");
            const auto receiverIdValue = json.value("receiverId", "");


            if(messageIdValue.empty() || senderIdValue.empty() || receiverIdValue.empty())
                return std::nullopt;

            const auto messageId = UUIDv4::UUID::fromStrFactory(messageIdValue);
            const auto senderId = UUIDv4::UUID::fromStrFactory(senderIdValue);
            const auto receiverId = UUIDv4::UUID::fromStrFactory(receiverIdValue);

            const std::string typeStr = json.value("type", "GROUP");
            const MessageType type = (typeStr == "PRIVATE") ? MessageType::PRIVATE : MessageType::GROUP;

            return Message{
                messageId,
                senderId,
                receiverId,
                type,
                json.value("senderName", ""),
                json.value("content", ""),
                std::chrono::system_clock::from_time_t(json.value("sentAt", static_cast<std::time_t>(0))),
                std::chrono::system_clock::from_time_t(json.value("deliveredAt", static_cast<std::time_t>(0)))
            };
        } catch (...) {
            return std::nullopt;
        }
    }

    nlohmann::json loadData() const {
        if(!fs::exists(filePath)) {
            return nlohmann::json::array();
        }

        std::ifstream file(filePath);
        if(!file.is_open())
            return nlohmann::json::array();

        nlohmann::json data;
        file >> data;
        return data;
    }

    void saveData(const nlohmann::json& data) const {
        std::ofstream file(filePath);
        file << data.dump(2);
    }

public:
    explicit FileMessageRepository(const std::string& path) {
        if (path.back() == '/')
            filePath = path + DB_FILE;
        else
            filePath = path + '/' + DB_FILE;
    }

    bool save(const Message &message) override {
        auto data = loadData();
        const auto messageIdStr = message.messageId.str();

        for(auto& item : data) {
            if(item["messageId"] == messageIdStr) {
                item = messageToJson(message);
                saveData(data);
                return true;
            }
        }

        data.push_back(messageToJson(message));
        saveData(data);
        return true;
    }

    std::vector<Message> findMessagesByReceiverId(const UUIDv4::UUID &receiverId,
        const std::chrono::system_clock::time_point &since, size_t limit, size_t offset) override {
        auto data = loadData();
        std::vector<Message> messages;
        const auto receiverIdStr = receiverId.str();
        const auto sinceTimeT = std::chrono::system_clock::to_time_t(since);

        for(const auto& item : data) {
            if(item["receiverId"] == receiverIdStr) {
                const auto sentAt = item["sentAt"].get<std::time_t>();
                if(sentAt >= sinceTimeT) {
                    if(auto message = jsonToMessage(item)) {
                        messages.push_back(message.value());
                    }
                }
            }
        }

        std::ranges::sort(messages,
          [](const Message& a, const Message& b) {
              return a.sentAt > b.sentAt;
          });

        if(offset >= messages.size()) {
            return {};
        }

        const auto startIdx = static_cast<std::vector<Message>::difference_type>(offset);
        const auto endIdx = static_cast<std::vector<Message>::difference_type>(std::min(offset + limit, messages.size()));

        return {messages.begin() + startIdx, messages.begin() + endIdx};
    }

    std::vector<Message> findPrivateMessages(const UUIDv4::UUID &user1Id,
        const UUIDv4::UUID &user2Id, const std::chrono::system_clock::time_point &since,
        size_t limit, size_t offset) override {
        auto data = loadData();
        std::vector<Message> messages;
        const auto user1Str = user1Id.str();
        const auto user2Str = user2Id.str();
        const auto sinceTimeT = std::chrono::system_clock::to_time_t(since);

        for(const auto& item : data) {
            const std::string typeStr = item.value("type", "GROUP");
            if(typeStr != "PRIVATE") continue;

            const std::string senderId = item.value("senderId", "");
            const std::string receiverId = item.value("receiverId", "");

            const bool isMatch = (senderId == user1Str && receiverId == user2Str) ||
                                (senderId == user2Str && receiverId == user1Str);

            if(isMatch) {
                const auto sentAt = item["sentAt"].get<std::time_t>();
                if(sentAt >= sinceTimeT) {
                    if(auto message = jsonToMessage(item)) {
                        messages.push_back(message.value());
                    }
                }
            }
        }

        std::ranges::sort(messages,
          [](const Message& a, const Message& b) {
              return a.sentAt > b.sentAt;
          });

        if(offset >= messages.size()) {
            return {};
        }

        const auto startIdx = static_cast<std::vector<Message>::difference_type>(offset);
        const auto endIdx = static_cast<std::vector<Message>::difference_type>(std::min(offset + limit, messages.size()));

        return {messages.begin() + startIdx, messages.begin() + endIdx};
    }
};