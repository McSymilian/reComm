#pragma once
#include <string>
#include <nlohmann/json.hpp>
#include "uuid_v4.h"

struct User {
    std::string username;
    std::string passwordHash;
    UUIDv4::UUID uuid;

    nlohmann::json toJson() const {
        return {
                {"username", username},
                {"passwordHash", passwordHash},
                {"uuid", uuid.str()}
        };
    }

    static User fromJson(const nlohmann::json& j) {
        auto uuid_str = j.value("uuid", "");
        UUIDv4::UUID user_uuid;

        if(!uuid_str.empty())
            user_uuid = UUIDv4::UUID::fromStrFactory(uuid_str);

        return User{
            j["username"].get<std::string>(),
            j["passwordHash"].get<std::string>(),
            user_uuid
        };
    }
};
