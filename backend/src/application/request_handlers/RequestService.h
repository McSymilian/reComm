#pragma once

#include <nlohmann/json.hpp>

using json = nlohmann::json;

class RequestService {
public:
    virtual ~RequestService() = default;

    virtual std::string getHandledMethodName() = 0;
    virtual json handleRequest(const json& request, const UUIDv4::UUID userUUID) = 0;
    virtual bool requireAuthentication() {
        return true;
    }
};