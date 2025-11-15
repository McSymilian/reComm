#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <format>
#include <iostream>
#include <unistd.h>
#include <CLI/CLI.hpp>
#include <nlohmann/json.hpp>

#include "application/AuthRequestService.h"
#include "application/RequestHandleService.h"
#include "infrastructure/FileUserRepository.h"
#include "application/UserService.h"

using json = nlohmann::json;

constexpr int DEFAULT_PORT = 8080;
constexpr int DEFAULT_VERBALITY = 10;
const std::string DEFAULT_DB_PATH = "users.json";

int main(int argc, char** argv) {
    int port = DEFAULT_PORT;
    std::string dbPath = DEFAULT_DB_PATH;
    short verbalityLevel = DEFAULT_VERBALITY;

    CLI::App app{"reComm :: UDP Server"};

    app.add_option("-p,--port", port, "Port number")
            ->check(CLI::Range(1, 65535));

    app.add_option("-v,--verbality", verbalityLevel, "Level of log communication activity")
            ->check(CLI::Range(0, 10));

    app.add_option("-d,--database", dbPath, "Database file path");

    CLI11_PARSE(app, argc, argv);
    Logger::setVerbalityLevel(verbalityLevel);

    const auto repository = std::make_shared<FileUserRepository>(dbPath);
    const auto userService = std::make_shared<UserService>(repository);

    const auto authRequestService = std::make_shared<AuthRequestService>(userService);
    const auto registerRequestService = std::make_shared<RegisterRequestService>(userService);
    const std::unordered_map<std::string, std::shared_ptr<RequestService>> requestServices {
        {registerRequestService->getHandledMethodName(), registerRequestService},
        {authRequestService->getHandledMethodName(), authRequestService}
    };
    const auto handleRequestService = RequestHandleService(requestServices);

    struct sockaddr_in localAddress, clientAddress;
    socklen_t clientAddressLen = sizeof(clientAddress);

    localAddress.sin_family = AF_INET;
    localAddress.sin_port = htons(port);
    localAddress.sin_addr.s_addr = htonl(INADDR_ANY);

    int server_socket = socket(AF_INET, SOCK_DGRAM, 0);

    if(server_socket == -1) {
        Logger::log("Could not create socket", Logger::Level::ERROR);
        exit(EXIT_FAILURE);
    }

    if(bind(server_socket, (struct sockaddr*)&localAddress, sizeof(localAddress)) == -1) {
        Logger::log("Could not bind", Logger::Level::ERROR);
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    Logger::log(std::format("Serwer UPD nasłuchuje na porcie {}", port), Logger::Level::INFO, Logger::Importance::HIGH);
    Logger::log(std::format("Źródło bazy danych {}", dbPath), Logger::Level::INFO, Logger::Importance::HIGH);
    Logger::log(std::format("Poziom rozmowności {}", verbalityLevel), Logger::Level::INFO, Logger::Importance::HIGH);

    char buff[4096];

    for(;;) {
        std::memset(buff, 0, sizeof(buff));
        int n = recvfrom(server_socket, buff, sizeof(buff)-1, 0,
                        (struct sockaddr*)&clientAddress, &clientAddressLen);

        if(n > 0) {
            try {
                json request;
                try {
                    request = json::parse(buff);
                } catch(const std::exception& e) {
                    request = json::parse("{}");
                }

                Logger::log(std::format("Request: {}", request.dump()));

                json response = handleRequestService.handleRequest(request);

                std::string responseStr = response.dump();
                sendto(server_socket, responseStr.c_str(), responseStr.size(), 0,
                      (struct sockaddr*)&clientAddress, clientAddressLen);

                Logger::log(std::format("Response: {}", responseStr));
            } catch(const std::exception& e) {
                Logger::log(std::format("Internal Error: {}", e.what()), Logger::Level::ERROR, Logger::Importance::HIGH);
            }
        }
    }

    close(server_socket);
    return 0;
}
