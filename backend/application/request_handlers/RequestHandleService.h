#pragma once

#include <nlohmann/json.hpp>
#include <utility>

#include "RegisterRequestService.h"
#include "../UserService.h"
#include "../../exceptions/unknown_method_error.h"
#include "../../exceptions/user_already_exists_error.h"
#include "../../exceptions/bad_request_format_error.h"
#include "../../utils/Logger.h"

using json = nlohmann::json;

class RequestHandleService {
    const std::unordered_map<std::string, std::shared_ptr<RequestService>> request_services;
public:
    explicit RequestHandleService(std::unordered_map<std::string, std::shared_ptr<RequestService>> request_services)
        : request_services(std::move(request_services)) {}

    json handleRequest(const json& request) const {
        const std::string method = request.value("method", "");
        json response;

        try {
            if (method.empty() || !request.contains("body"))
                throw bad_request_format_error();

            auto it = request_services.find(method);
            if(it != request_services.end())
                return it->second->handleRequest(request["body"]);

            throw unknown_method_error(method);
        } catch (const unknown_method_error& e) {
            Logger::log(std::string("Unknown method: ") + method, Logger::Level::WARNING);
            response["code"] = 400;
            response["message"] = e.what();

            return response;
        } catch (const bad_request_format_error& e) {
            Logger::log(std::string("Bad format: ") + request.dump(), Logger::Level::WARNING);
            response["code"] = 400;
            response["message"] = e.what();

            return response;
        } catch (const user_already_exists_error& e) {
            response["code"] = 409;
            response["message"] = e.what();

            return response;
        }  catch (const std::exception& e) {
            Logger::log(std::string("Error handling request: ") + e.what(), Logger::Level::ERROR);
            response["code"] = 500;
            response["message"] = "Internal server error: ";

            return response;
        }
        // else if(method == "AUTH") {
        //     const std::string username = request.value("username", "");
        //     const std::string password = request.value("password", "");
        //
        //     std::optional<std::string> token = userService->authenticate(username, password);
        //     if(token.has_value()) {
        //         response["code"] = 200;
        //         response["message"] = "Authentication successful";
        //         response["token"] = token.value();
        //     } else {
        //         response["code"] = 401;
        //         response["message"] = "Invalid credentials";
        //     }
        // }

        response["code"] = 400;
        response["message"] = "Unknown method";

        return response;
    }
};