#pragma once

#include <nlohmann/json.hpp>
#include <utility>
#include "RegisterRequestService.h"
#include "../../exceptions/unknown_method_error.h"
#include "../../exceptions/user_already_exists_error.h"
#include "../../exceptions/bad_request_format_error.h"
#include "../../exceptions/invalid_credentials_error.h"
#include "../../exceptions/user_not_found_error.h"
#include "../../exceptions/already_friends_error.h"
#include "../../exceptions/cannot_be_self_friend_error.h"
#include "../../exceptions/friendship_request_already_sent_error.h"
#include "../../exceptions/friendship_request_already_processed_error.h"
#include "../../exceptions/friendship_request_not_found_error.h"
#include "../../exceptions/friendship_request_process_error.h"
#include "../../exceptions/save_friendship_request_error.h"
#include "../../exceptions/invalid_token_error.h"
#include "../../exceptions/missing_required_field_error.h"
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
        } catch (const missing_required_field_error& e) {
            Logger::log(std::string("Missing required field: ") + e.what(), Logger::Level::WARNING);
            response["code"] = 400;
            response["message"] = e.what();

            return response;
        } catch (const user_already_exists_error& e) {
            response["code"] = 409;
            response["message"] = e.what();

            return response;
        } catch (const invalid_credentials_error& e) {
            response["code"] = 401;
            response["message"] = e.what();

            return response;
        } catch (const invalid_token_error& e) {
            response["code"] = 401;
            response["message"] = e.what();

            return response;
        } catch (const user_not_found_error& e) {
            response["code"] = 404;
            response["message"] = e.what();

            return response;
        } catch (const already_friends_error& e) {
            response["code"] = 409;
            response["message"] = e.what();

            return response;
        } catch (const cannot_be_self_friend_error& e) {
            response["code"] = 400;
            response["message"] = e.what();

            return response;
        } catch (const friendship_request_already_sent_error& e) {
            response["code"] = 409;
            response["message"] = e.what();

            return response;
        } catch (const friendship_request_already_processed_error& e) {
            response["code"] = 409;
            response["message"] = e.what();

            return response;
        } catch (const friendship_request_not_found_error& e) {
            response["code"] = 404;
            response["message"] = e.what();

            return response;
        } catch (const friendship_request_process_error& e) {
            response["code"] = 500;
            response["message"] = e.what();

            return response;
        } catch (const save_friendship_request_error& e) {
            response["code"] = 500;
            response["message"] = e.what();

            return response;
        }  catch (const std::exception& e) {
            Logger::log(std::string("Error handling request: ") + e.what(), Logger::Level::ERROR);
            response["code"] = 500;
            response["message"] = "Internal server error: ";

            return response;
        }
    }
};