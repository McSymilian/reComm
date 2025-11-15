#pragma once
#include <nlohmann/json.hpp>

#include "RequestService.h"
#include "../UserService.h"
#include "../../exceptions/invalid_credentials_error.h"

using json = nlohmann::json;
class AuthRequestService final : public RequestService {
    const std::shared_ptr<UserService> userService;
public:
    explicit AuthRequestService(std::shared_ptr<UserService> userService) : userService(std::move(userService)) {}

    std::string getHandledMethodName() override {
        return "AUTH";
    }

    json handleRequest(const json& request) override {
        const std::string username = request.value("username", "");
        const std::string password = request.value("password", "");

        std::optional<std::string> token = userService->authenticate(username, password);
        if(!token.has_value())
            throw invalid_credentials_error();

        json response;
        response["token"] = token.value();
        response["code"] = 200;
        response["message"] = "Authenticated";
        return response;

    }
};