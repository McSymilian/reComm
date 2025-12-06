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

#include "src/application/FriendshipService.h"
#include "src/application/GroupService.h"
#include "src/application/MessageService.h"
#include "src/application/request_handlers/AuthRequestService.h"
#include "src/application/request_handlers/FriendRequestService.h"
#include "src/application/request_handlers/GroupRequestService.h"
#include "src/application/request_handlers/MessageRequestService.h"
#include "src/application/request_handlers/RequestHandleService.h"
#include "src/infrastructure/FileUserRepository.h"
#include "src/application/UserService.h"
#include "src/infrastructure/FileFriendshipRepository.h"
#include "src/infrastructure/FileGroupRepository.h"
#include "src/infrastructure/FileMessageRepository.h"
#include "src/infrastructure/ConnectionManager.h"
#include "src/infrastructure/FileNotificationRepository.h"
#include "src/application/NotificationService.h"

using json = nlohmann::json;

constexpr int DEFAULT_PORT = 8080;
constexpr int DEFAULT_VERBALITY = 10;
const std::string DEFAULT_DB_PATH = "db";

void handleClient(
    const int client_socket,
    const RequestHandleService& handleRequestService,
    const std::shared_ptr<ConnectionManager>& connectionManager,
    const std::shared_ptr<NotificationService>& notificationService,
    const sockaddr_in& clientAddress
) {
    char clientIP[INET_ADDRSTRLEN];
    inet_ntop(AF_INET, &clientAddress.sin_addr, clientIP, INET_ADDRSTRLEN);
    int clientPort = ntohs(clientAddress.sin_port);

    Logger::log(std::format("Nowe połączenie z {}:{}", clientIP, clientPort), Logger::Level::INFO, Logger::Importance::LOW);

    std::optional<UUIDv4::UUID> authenticatedUserId;

    bool shouldClose = false;
    while(!shouldClose) {
        char buff[4096] = {};
        ssize_t n = recv(client_socket, buff, sizeof(buff)-1, 0);
        if(n > 0) {
            try {
                json request;
                try {
                    request = json::parse(buff);
                } catch(const std::exception&) {
                    Logger::log(std::format("Received text: {}", std::string(buff)), Logger::Level::WARNING, Logger::Importance::LOW);
                    request = json::parse("{}");
                }

                Logger::log(std::format("Request from {}:{}: {}", clientIP, clientPort, request.dump()), Logger::Level::INFO, Logger::Importance::LOW);

                const json response = handleRequestService.handleRequest(request, client_socket, authenticatedUserId);

                std::string responseStr = response.dump() + "\n";
                ssize_t sent = send(client_socket, responseStr.c_str(), responseStr.size(), 0);

                if (response.contains("close"))
                    shouldClose = true;

                if(sent == -1) {
                    Logger::log(std::format("Error sending response to {}:{}", clientIP, clientPort), Logger::Level::ERROR, Logger::Importance::MEDIUM);
                    shouldClose = true;
                } else
                    Logger::log(std::format("Response to {}:{}: {}", clientIP, clientPort, responseStr), Logger::Level::INFO, Logger::Importance::LOW);

            } catch(const std::exception& e) {
                Logger::log(std::format("Internal error for {}:{}: {}", clientIP, clientPort, e.what()), Logger::Level::ERROR, Logger::Importance::HIGH);
                shouldClose = true;
            }
        } else if(n == 0) {
            Logger::log(std::format("Client {}:{} disconnected", clientIP, clientPort), Logger::Level::INFO, Logger::Importance::LOW);
            shouldClose = true;
        } else {
            Logger::log(std::format("Error receiving data from {}:{}", clientIP, clientPort), Logger::Level::ERROR, Logger::Importance::MEDIUM);
            shouldClose = true;
        }
    }

    if(authenticatedUserId.has_value())
        connectionManager->unregisterConnection(authenticatedUserId.value());


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

    if(bind(server_socket, reinterpret_cast<sockaddr *>(&localAddress), sizeof(localAddress)) == -1) {
        Logger::log("Could not bind", Logger::Level::ERROR, Logger::Importance::MEDIUM);
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    if(listen(server_socket, 5) == -1) {
        Logger::log("Could not listen", Logger::Level::ERROR, Logger::Importance::MEDIUM);
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    const auto friendship_repository = std::make_shared<FileFriendshipRepository>(dbPath);
    const auto user_repository = std::make_shared<FileUserRepository>(dbPath);
    const auto group_repository = std::make_shared<FileGroupRepository>(dbPath);
    const auto message_repository = std::make_shared<FileMessageRepository>(dbPath);
    const auto notification_repository = std::make_shared<FileNotificationRepository>(dbPath);
    const auto connectionManager = std::make_shared<ConnectionManager>();
    const auto jwtService = std::make_shared<JwtService>("super_tajne_hasło_do_jwt_nie_zmienie_w_produkcji");
    const auto userService = std::make_shared<UserService>(user_repository, jwtService);
    const auto friendshipService = std::make_shared<FriendshipService>(friendship_repository, user_repository);
    const auto groupService = std::make_shared<GroupService>(group_repository, friendship_repository, user_repository);
    const auto notificationService = std::make_shared<NotificationService>(notification_repository, connectionManager);
    const auto messageService = std::make_shared<MessageService>(message_repository, group_repository, user_repository, friendship_repository, notificationService);

    const auto authRequestService = std::make_shared<AuthRequestService>(userService);
    const auto registerRequestService = std::make_shared<RegisterRequestService>(userService);

    // Friendship services
    const auto sendFriendRequestService = std::make_shared<SendFriendRequestService>(friendshipService, userService, notificationService);
    const auto acceptFriendRequestService = std::make_shared<AcceptFriendRequestService>(friendshipService, userService);
    const auto rejectFriendRequestService = std::make_shared<RejectFriendRequestService>(friendshipService, userService);
    const auto getFriendsService = std::make_shared<GetFriendsService>(friendshipService, userService);
    const auto getPendingRequestsService = std::make_shared<GetPendingRequestsService>(friendshipService, userService);

    // Group services
    const auto createGroupService = std::make_shared<CreateGroupService>(groupService);
    const auto addMemberToGroupService = std::make_shared<AddMemberToGroupService>(groupService);
    const auto updateGroupNameService = std::make_shared<UpdateGroupNameService>(groupService);
    const auto leaveGroupService = std::make_shared<LeaveGroupService>(groupService);
    const auto deleteGroupService = std::make_shared<DeleteGroupService>(groupService);
    const auto getUserGroupsService = std::make_shared<GetUserGroupsService>(groupService);
    const auto getGroupDetailsService = std::make_shared<GetGroupDetailsService>(groupService);
    const auto getGroupMembersService = std::make_shared<GetGroupMembersService>(groupService, user_repository);

    // Message services
    const auto sendMessageService = std::make_shared<SendMessageService>(messageService);
    const auto sendGroupMessageService = std::make_shared<SendGroupMessageService>(messageService);
    const auto sendPrivateMessageService = std::make_shared<SendPrivateMessageService>(messageService, user_repository);
    const auto getGroupMessagesService = std::make_shared<GetGroupMessagesService>(messageService);
    const auto getPrivateMessagesService = std::make_shared<GetPrivateMessagesService>(messageService, user_repository);
    const auto getRecentMessagesService = std::make_shared<GetRecentMessagesService>(messageService);

    const std::unordered_map<std::string, std::shared_ptr<RequestService>> requestServices {
            {registerRequestService->getHandledMethodName(), registerRequestService},
            {authRequestService->getHandledMethodName(), authRequestService},
            {sendFriendRequestService->getHandledMethodName(), sendFriendRequestService},
            {acceptFriendRequestService->getHandledMethodName(), acceptFriendRequestService},
            {rejectFriendRequestService->getHandledMethodName(), rejectFriendRequestService},
            {getFriendsService->getHandledMethodName(), getFriendsService},
            {getPendingRequestsService->getHandledMethodName(), getPendingRequestsService},
            {createGroupService->getHandledMethodName(), createGroupService},
            {addMemberToGroupService->getHandledMethodName(), addMemberToGroupService},
            {updateGroupNameService->getHandledMethodName(), updateGroupNameService},
            {leaveGroupService->getHandledMethodName(), leaveGroupService},
            {deleteGroupService->getHandledMethodName(), deleteGroupService},
            {getUserGroupsService->getHandledMethodName(), getUserGroupsService},
            {getGroupDetailsService->getHandledMethodName(), getGroupDetailsService},
            {getGroupMembersService->getHandledMethodName(), getGroupMembersService},
            {sendMessageService->getHandledMethodName(), sendMessageService},
            {sendGroupMessageService->getHandledMethodName(), sendGroupMessageService},
            {sendPrivateMessageService->getHandledMethodName(), sendPrivateMessageService},
            {getGroupMessagesService->getHandledMethodName(), getGroupMessagesService},
            {getPrivateMessagesService->getHandledMethodName(), getPrivateMessagesService},
            {getRecentMessagesService->getHandledMethodName(), getRecentMessagesService}
    };
    const auto handleRequestService = RequestHandleService(requestServices, jwtService, connectionManager, notificationService);

    Logger::log(std::format("Serwer TCP nasłuchuje na porcie {}", port), Logger::Level::INFO, Logger::Importance::HIGH);
    Logger::log(std::format("Źródło bazy danych {}", dbPath), Logger::Level::INFO, Logger::Importance::HIGH);
    Logger::log(std::format("Poziom rozmowności {}", verbalityLevel), Logger::Level::INFO, Logger::Importance::HIGH);


    for(;;) {
        int client_socket = accept(server_socket, reinterpret_cast<struct sockaddr *>(&clientAddress), &clientAddressLen);

        if(client_socket == -1) {
            Logger::log("Could not accept connection", Logger::Level::ERROR, Logger::Importance::MEDIUM);
            continue;
        }

        std::thread clientThread(handleClient, client_socket, std::ref(handleRequestService), connectionManager, notificationService, clientAddress);
        clientThread.detach();
    }

    close(server_socket);
    return 0;
}
