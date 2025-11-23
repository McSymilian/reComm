#pragma once

#include <string>
#include <vector>
#include <chrono>
#include "uuid_v4.h"
#include <nlohmann/json.hpp>

struct Group {
    UUIDv4::UUID groupId;
    std::string name;
    UUIDv4::UUID creatorId;
    std::vector<UUIDv4::UUID> members;
    std::chrono::system_clock::time_point createdAt;
    std::chrono::system_clock::time_point updatedAt;

    nlohmann::json toJson() const {
        nlohmann::json membersJson = nlohmann::json::array();
        for (const auto& member : members) {
            membersJson.push_back(member.str());
        }

        return {
            {"groupId", groupId.str()},
            {"name", name},
            {"creatorId", creatorId.str()},
            {"members", membersJson},
            {"createdAt", std::chrono::system_clock::to_time_t(createdAt)},
            {"updatedAt", std::chrono::system_clock::to_time_t(updatedAt)}
        };
    }

    static std::optional<Group> fromJson(const nlohmann::json& j) {
        try {
            const auto gIDValue = j.value("groupId", "");
            const auto cIDValue = j.value("creatorId", "");

            if (gIDValue == "" || cIDValue == "")
                return std::nullopt;

            const auto groupId = UUIDv4::UUID::fromStrFactory(gIDValue);
            const auto creatorId = UUIDv4::UUID::fromStrFactory(cIDValue);

            std::vector<UUIDv4::UUID> members;
            for (const auto& memberStr : j["members"]) {
                auto memberId = UUIDv4::UUID::fromStrFactory(memberStr.get<std::string>());
                if (memberId != nullptr)
                    members.push_back(memberId);
            }

            return Group{
                groupId,
                j["name"].get<std::string>(),
                creatorId,
                members,
                std::chrono::system_clock::from_time_t(j["createdAt"].get<std::time_t>()),
                std::chrono::system_clock::from_time_t(j["updatedAt"].get<std::time_t>())
            };
        } catch (...) {
            return std::nullopt;
        }
    }
};

