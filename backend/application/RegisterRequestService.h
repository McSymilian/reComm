#pragma once
#include <nlohmann/json.hpp>

#include "RequestService.h"
#include "UserService.h"
#include "../exceptions/user_already_exists_error.h"

using json = nlohmann::json;
class RegisterRequestService final : public RequestService {
    const std::shared_ptr<UserService> userService;
public:
    explicit RegisterRequestService(std::shared_ptr<UserService> userService) : userService(std::move(userService)) {}

    std::string getHandledMethodName() override {
        return "REGISTER";
    }

    json handleRequest(const json& request) override {
        const std::string username = request.value("username", "");
        const std::string password = request.value("password", "");

        std::optional<std::string> token = userService->registerUser(username, password);
        if(token->empty())
            throw user_already_exists_error("Username is already taken");

        json response;
        response["token"] = token.value();
        response["code"] = 201;
        response["message"] = "User registered successfully";
        return response;
    }
};