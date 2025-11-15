#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <unistd.h>
#include <CLI/CLI.hpp>
#include <nlohmann/json.hpp>

#include "infrastructure/FileUserRepository.h"
#include "application/UserService.h"

using json = nlohmann::json;

json handleRequest(const json& request, UserService& userService) {
    json response;
    const std::string method = request.value("method", "");

    if(method == "REGISTER") {
        const std::string username = request.value("username", "");
        const std::string password = request.value("password", "");
        std::optional<std::string> token = userService.registerUser(username, password);
        if(token.has_value()) {
            response["token"] = token.value();
            response["code"] = 201;
            response["message"] = "User registered successfully";
        } else {
            response["code"] = 409;
            response["message"] = "Username already exists";
        }
    }
    else if(method == "AUTH") {
        const std::string username = request.value("username", "");
        const std::string password = request.value("password", "");
        std::optional<std::string> token = userService.authenticate(username, password);
        if(token.has_value()) {
            response["code"] = 200;
            response["message"] = "Authentication successful";
            response["token"] = token.value();
        } else {
            response["code"] = 401;
            response["message"] = "Invalid credentials";
        }
    }
    else {
        response["code"] = 400;
        response["message"] = "Unknown method";
    }

    return response;
}

constexpr int DEFAULT_PORT = 8080;
const std::string DEFAULT_DB_PATH = "users.json";

int main(int argc, char** argv) {
    int port = DEFAULT_PORT;
    std::string dbPath = DEFAULT_DB_PATH;

    CLI::App app{"reComm :: UDP Server"};
    app.add_option("-p,--port", port, "Port number")
            ->check(CLI::Range(1, 65535));
    app.add_option("-d,--database", dbPath, "Database file path");
    CLI11_PARSE(app, argc, argv);

    auto repository = std::make_shared<FileUserRepository>(dbPath);
    UserService userService(repository);

    struct sockaddr_in localAddress, clientAddress;
    socklen_t clientAddressLen = sizeof(clientAddress);

    localAddress.sin_family = AF_INET;
    localAddress.sin_port = htons(port);
    localAddress.sin_addr.s_addr = htonl(INADDR_ANY);

    int server_socket = socket(AF_INET, SOCK_DGRAM, 0);

    if(server_socket == -1) {
        perror("Could not create socket");
        exit(EXIT_FAILURE);
    }

    if(bind(server_socket, (struct sockaddr*)&localAddress, sizeof(localAddress)) == -1) {
        perror("Could not bind");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    std::cout << "Serwer UDP nasłuchuje na porcie " << port << "\n";
    std::cout << "Baza danych: " << dbPath << "\n";

    char buff[4096];

    for(;;) {
        std::memset(buff, 0, sizeof(buff));
        int n = recvfrom(server_socket, buff, sizeof(buff)-1, 0,
                        (struct sockaddr*)&clientAddress, &clientAddressLen);

        if(n > 0) {
            try {
                json request = json::parse(buff);
                json response = handleRequest(request, userService);

                std::string responseStr = response.dump();
                sendto(server_socket, responseStr.c_str(), responseStr.size(), 0,
                      (struct sockaddr*)&clientAddress, clientAddressLen);

                std::cout << "Request: " << request.dump() << "\n";
                std::cout << "Response: " << response.dump() << "\n";
            } catch(const std::exception& e) {
                std::cerr << "Error: " << e.what() << "\n";
            }
        }
    }

    close(server_socket);
    return 0;
}
