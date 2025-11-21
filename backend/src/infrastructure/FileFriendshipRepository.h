#pragma once
#include "../domain/friendship/FriendshipRepository.h"
#include <nlohmann/json.hpp>
#include <fstream>

#if __has_include(<filesystem>)
    #include <filesystem>
    namespace fs = std::filesystem;
#elif __has_include(<experimental/filesystem>)
    #include <experimental/filesystem>
    namespace fs = std::experimental::filesystem;
#else
    #error "No filesystem support"
#endif

class FileFriendshipRepository final : public FriendshipRepository {
    fs::path filePath;
    static constexpr std::string DB_FILE = "friendship.json";

    static std::string statusToString(const FriendshipStatus status) {
        switch(status) {
            case FriendshipStatus::PENDING: return "PENDING";
            case FriendshipStatus::ACCEPTED: return "ACCEPTED";
            case FriendshipStatus::REJECTED: return "REJECTED";
        }
        return "PENDING";
    }

    static FriendshipStatus stringToStatus(const std::string& str) {
        if(str == "ACCEPTED") return FriendshipStatus::ACCEPTED;
        if(str == "REJECTED") return FriendshipStatus::REJECTED;
        return FriendshipStatus::PENDING;
    }

    static nlohmann::json friendshipToJson(const Friendship& friendship) {
        return {
            {"requesterId", friendship.requesterId.str()},
            {"addresseeId", friendship.addresseeId.str()},
            {"status", statusToString(friendship.status)},
            {"createdAt", std::chrono::system_clock::to_time_t(friendship.createdAt)},
            {"updatedAt", std::chrono::system_clock::to_time_t(friendship.updatedAt)}
        };
    }

    static std::optional<Friendship> jsonToFriendship(const nlohmann::json& json) {
        try {
            auto requesterId = UUIDv4::UUID::fromStrFactory(json["requesterId"].get<std::string>());
            auto addresseeId = UUIDv4::UUID::fromStrFactory(json["addresseeId"].get<std::string>());

            if(!requesterId || !addresseeId)
                return std::nullopt;

            return Friendship{
                requesterId.value(),
                addresseeId.value(),
                stringToStatus(json["status"].get<std::string>()),
                std::chrono::system_clock::from_time_t(json["createdAt"].get<std::time_t>()),
                std::chrono::system_clock::from_time_t(json["updatedAt"].get<std::time_t>())
            };
        } catch(...) {
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
    explicit FileFriendshipRepository(const std::string& path) {
        if (path.back() == '/')
            filePath = path + DB_FILE;
        else
            filePath = path + '/' + DB_FILE;
    }

    bool save(const Friendship& friendship) override {
        auto data = loadData();

        for(auto& item : data) {
            if(item["requesterId"] == friendship.requesterId.str() &&
               item["addresseeId"] == friendship.addresseeId.str()) {
                item = friendshipToJson(friendship);
                saveData(data);
                return true;
            }
        }

        data.push_back(friendshipToJson(friendship));
        saveData(data);
        return true;
    }

    bool updateStatus(const UUIDv4::UUID& requesterId,
                     const UUIDv4::UUID& addresseeId,
                     FriendshipStatus status) override {
        auto data = loadData();
        const auto requesterIdStr = requesterId.str();
        const auto addresseeIdStr = addresseeId.str();

        for(auto& item : data) {
            if(item["requesterId"] == requesterIdStr &&
               item["addresseeId"] == addresseeIdStr) {
                item["status"] = statusToString(status);
                item["updatedAt"] = std::chrono::system_clock::to_time_t(
                    std::chrono::system_clock::now());
                saveData(data);
                return true;
            }
        }

        return false;
    }

    std::optional<Friendship> find(const UUIDv4::UUID& requesterId,
                                  const UUIDv4::UUID& addresseeId) override {
        auto data = loadData();
        const auto requesterIdStr = requesterId.str();
        const auto addresseeIdStr = addresseeId.str();

        for(const auto& item : data) {
            if(item["requesterId"] == requesterIdStr &&
               item["addresseeId"] == addresseeIdStr) {
                return jsonToFriendship(item);
            }
        }

        return std::nullopt;
    }

    std::vector<UUIDv4::UUID> getFriends(const UUIDv4::UUID& userId) override {
        auto data = loadData();
        std::vector<UUIDv4::UUID> friends;
        const auto userIdStr = userId.str();

        for(const auto& item : data) {
            if(item["status"] != "ACCEPTED")
                continue;

            if(item["requesterId"] == userIdStr) {
                if(auto uuid = UUIDv4::UUID::fromStrFactory(item["addresseeId"].get<std::string>()))
                    friends.push_back(uuid.value());
            } else if(item["addresseeId"] == userIdStr) {
                if(auto uuid = UUIDv4::UUID::fromStrFactory(item["requesterId"].get<std::string>()))
                    friends.push_back(uuid.value());
            }
        }

        return friends;
    }

    std::vector<Friendship> getPendingRequests(const UUIDv4::UUID& userId) override {
        auto data = loadData();
        std::vector<Friendship> requests;
        const auto userIdStr = userId.str();

        for(const auto& item : data) {
            if(item["addresseeId"] == userIdStr && item["status"] == "PENDING") {
                if(auto friendship = jsonToFriendship(item))
                    requests.push_back(friendship.value());
            }
        }

        return requests;
    }

    bool areFriends(const UUIDv4::UUID& user1, const UUIDv4::UUID& user2) override {
        auto data = loadData();
        const auto user1Str = user1.str();
        const auto user2Str = user2.str();

        for(const auto& item : data) {
            if(item["status"] != "ACCEPTED")
                continue;

            if((item["requesterId"] == user1Str && item["addresseeId"] == user2Str) ||
               (item["requesterId"] == user2Str && item["addresseeId"] == user1Str)) {
                return true;
            }
        }

        return false;
    }
};
