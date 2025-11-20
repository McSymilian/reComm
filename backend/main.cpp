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
#include <thread>
#include <memory>
#include <CLI/CLI.hpp>
#include <nlohmann/json.hpp>

#include "src/application/request_handlers/AuthRequestService.h"
#include "src/application/request_handlers/RequestHandleService.h"
#include "src/infrastructure/FileUserRepository.h"
#include "src/application/UserService.h"

using json = nlohmann::json;

constexpr int DEFAULT_PORT = 8080;
constexpr int DEFAULT_VERBALITY = 10;
const std::string DEFAULT_DB_PATH = "users.json";

void handleClient(int client_socket, const RequestHandleService& handleRequestService, const sockaddr_in& clientAddress) {
    char buff[4096] = {};

    char clientIP[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &(clientAddress.sin_addr), clientIP, INET_ADDRSTRLEN);
    int clientPort = ntohs(clientAddress.sin_port);

    Logger::log(std::format("Nowe połączenie z {}:{}", clientIP, clientPort), Logger::Level::INFO, Logger::Importance::LOW);

    ssize_t n = recv(client_socket, buff, sizeof(buff)-1, 0);

    if(n > 0) {
        try {
            json request;
            try {
                request = json::parse(buff);
            } catch(const std::exception&) {
                request = json::parse("{}");
            }

            Logger::log(std::format("Request from {}:{}: {}", clientIP, clientPort, request.dump()), Logger::Level::INFO, Logger::Importance::LOW);

            const json response = handleRequestService.handleRequest(request);

            std::string responseStr = response.dump() + "\n";
            send(client_socket, responseStr.c_str(), responseStr.size(), 0);

            Logger::log(std::format("Response to {}:{}: {}", clientIP, clientPort, responseStr), Logger::Level::INFO, Logger::Importance::LOW);
        } catch(const std::exception& e) {
            Logger::log(std::format("Internal Error for {}:{}: {}", clientIP, clientPort, e.what()), Logger::Level::ERROR, Logger::Importance::HIGH);
        }
    } else if(n == 0) {
        Logger::log(std::format("Client {}:{} disconnected", clientIP, clientPort), Logger::Level::INFO, Logger::Importance::LOW);
    } else {
        Logger::log(std::format("Error receiving data from {}:{}", clientIP, clientPort), Logger::Level::ERROR, Logger::Importance::MEDIUM);
    }

    close(client_socket);
    Logger::log(std::format("Zamknięto połączenie z {}:{}", clientIP, clientPort), Logger::Level::INFO, Logger::Importance::LOW);
}

int main(int argc, char** argv) {
    int port = DEFAULT_PORT;
    std::string dbPath = DEFAULT_DB_PATH;
    short verbalityLevel = DEFAULT_VERBALITY;

    CLI::App app{"reComm :: TCP Server"};

    app.add_option("-p,--port", port, "Port number")
            ->check(CLI::Range(1, 65535));

    app.add_option("-v,--verbality", verbalityLevel, "Level of log communication activity")
            ->check(CLI::Range(0, 10));

    app.add_option("-d,--database", dbPath, "Database file path");

    CLI11_PARSE(app, argc, argv);
    Logger::setVerbalityLevel(verbalityLevel);

    struct sockaddr_in localAddress, clientAddress;
    socklen_t clientAddressLen = sizeof(clientAddress);

    localAddress.sin_family = AF_INET;
    localAddress.sin_port = htons(port);
    localAddress.sin_addr.s_addr = htonl(INADDR_ANY);

    const int server_socket = socket(AF_INET, SOCK_STREAM, 0);

    if(server_socket == -1) {
        Logger::log("Could not create socket", Logger::Level::ERROR, Logger::Importance::MEDIUM);
        exit(EXIT_FAILURE);
    }

    constexpr int opt = 1;
    if(setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) == -1) {
        Logger::log("Could not set socket options", Logger::Level::ERROR, Logger::Importance::MEDIUM);
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    if(bind(server_socket, reinterpret_cast<struct sockaddr *>(&localAddress), sizeof(localAddress)) == -1) {
        Logger::log("Could not bind", Logger::Level::ERROR, Logger::Importance::MEDIUM);
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    if(listen(server_socket, 5) == -1) {
        Logger::log("Could not listen", Logger::Level::ERROR, Logger::Importance::MEDIUM);
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    Logger::log(std::format("Serwer TCP nasłuchuje na porcie {}", port), Logger::Level::INFO, Logger::Importance::HIGH);
    Logger::log(std::format("Źródło bazy danych {}", dbPath), Logger::Level::INFO, Logger::Importance::HIGH);
    Logger::log(std::format("Poziom rozmowności {}", verbalityLevel), Logger::Level::INFO, Logger::Importance::HIGH);

    const auto repository = std::make_shared<FileUserRepository>(dbPath);
    const auto jwtService = std::make_shared<JwtService>("super_tajne_hasło_do_jwt_nie_zmienie_w_produkcji");
    const auto userService = std::make_shared<UserService>(repository, jwtService);

    const auto authRequestService = std::make_shared<AuthRequestService>(userService);
    const auto registerRequestService = std::make_shared<RegisterRequestService>(userService);
    const std::unordered_map<std::string, std::shared_ptr<RequestService>> requestServices {
            {registerRequestService->getHandledMethodName(), registerRequestService},
            {authRequestService->getHandledMethodName(), authRequestService}
    };
    const auto handleRequestService = RequestHandleService(requestServices);

    for(;;) {
        int client_socket = accept(server_socket, reinterpret_cast<struct sockaddr *>(&clientAddress), &clientAddressLen);

        if(client_socket == -1) {
            Logger::log("Could not accept connection", Logger::Level::ERROR, Logger::Importance::MEDIUM);
            continue;
        }

        std::thread clientThread(handleClient, client_socket, std::ref(handleRequestService), clientAddress);
        clientThread.detach();
    }

    close(server_socket);
    return 0;
}
