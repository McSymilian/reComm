#pragma once
#include "../domain/group/GroupRepository.h"
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

class FileGroupRepository final : public GroupRepository {
    fs::path filePath;
    static constexpr std::string DB_FILE = "groups.json";

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
    explicit FileGroupRepository(const std::string& path) {
        if (path.back() == '/')
            filePath = path + DB_FILE;
        else
            filePath = path + '/' + DB_FILE;
    }

    bool save(const Group& group) override {
        auto data = loadData();
        const auto groupIdStr = group.groupId.str();

        for(auto& item : data) {
            if(item["groupId"] == groupIdStr) {
                item = group.toJson();
                saveData(data);
                return true;
            }
        }

        data.push_back(group.toJson());
        saveData(data);
        return true;
    }

    std::optional<Group> findById(const UUIDv4::UUID& groupId) override {
        auto data = loadData();
        const auto groupIdStr = groupId.str();

        for(const auto& item : data) {
            if(item["groupId"] == groupIdStr) {
                return Group::fromJson(item);
            }
        }

        return std::nullopt;
    }

    std::vector<Group> findByMemberId(const UUIDv4::UUID& userId) override {
        auto data = loadData();
        std::vector<Group> groups;
        const auto userIdStr = userId.str();

        for(const auto& item : data) {
            const auto& members = item["members"];
            for(const auto& memberId : members) {
                if(memberId.get<std::string>() == userIdStr) {
                    if(auto group = Group::fromJson(item)) {
                        groups.push_back(group.value());
                    }
                    break;
                }
            }
        }

        return groups;
    }

    bool updateName(const UUIDv4::UUID& groupId, const std::string& newName) override {
        auto data = loadData();
        const auto groupIdStr = groupId.str();

        for(auto& item : data) {
            if(item["groupId"] == groupIdStr) {
                item["name"] = newName;
                item["updatedAt"] = std::chrono::system_clock::to_time_t(
                    std::chrono::system_clock::now());
                saveData(data);
                return true;
            }
        }

        return false;
    }

    bool addMember(const UUIDv4::UUID& groupId, const UUIDv4::UUID& memberId) override {
        auto data = loadData();
        const auto groupIdStr = groupId.str();
        const auto memberIdStr = memberId.str();

        for(auto& item : data) {
            if(item["groupId"] == groupIdStr) {
                auto& members = item["members"];
                for(const auto& member : members) {
                    if(member.get<std::string>() == memberIdStr) {
                        return false;
                    }
                }

                members.push_back(memberIdStr);
                item["updatedAt"] = std::chrono::system_clock::to_time_t(
                    std::chrono::system_clock::now());
                saveData(data);
                return true;
            }
        }

        return false;
    }

    bool removeMember(const UUIDv4::UUID& groupId, const UUIDv4::UUID& memberId) override {
        auto data = loadData();
        const auto groupIdStr = groupId.str();
        const auto memberIdStr = memberId.str();

        for(auto& item : data) {
            if(item["groupId"] == groupIdStr) {
                auto& members = item["members"];
                auto newEnd = std::remove_if(members.begin(), members.end(),
                    [&memberIdStr](const nlohmann::json& member) {
                        return member.get<std::string>() == memberIdStr;
                    });

                if(newEnd != members.end()) {
                    members.erase(newEnd, members.end());
                    item["updatedAt"] = std::chrono::system_clock::to_time_t(
                        std::chrono::system_clock::now());
                    saveData(data);
                    return true;
                }

                return false;
            }
        }

        return false;
    }

    bool isMember(const UUIDv4::UUID& groupId, const UUIDv4::UUID& userId) override {
        auto data = loadData();
        const auto groupIdStr = groupId.str();
        const auto userIdStr = userId.str();

        for(const auto& item : data) {
            if(item["groupId"] == groupIdStr) {
                const auto& members = item["members"];
                for(const auto& member : members) {
                    if(member.get<std::string>() == userIdStr) {
                        return true;
                    }
                }
                return false;
            }
        }

        return false;
    }

    bool deleteGroup(const UUIDv4::UUID& groupId) override {
        auto data = loadData();
        const auto groupIdStr = groupId.str();

        auto newEnd = std::remove_if(data.begin(), data.end(),
            [&groupIdStr](const nlohmann::json& item) {
                return item["groupId"].get<std::string>() == groupIdStr;
            });

        if(newEnd != data.end()) {
            data.erase(newEnd, data.end());
            saveData(data);
            return true;
        }

        return false;
    }
};

