cmake_minimum_required(VERSION 3.28)

set(CMAKE_C_COMPILER /usr/bin/gcc)
set(CMAKE_CXX_COMPILER /usr/bin/g++)
add_compile_options(-std=c++20)
project(reComm)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

enable_language(CXX)

message(STATUS "C++ Compiler: ${CMAKE_CXX_COMPILER}")
message(STATUS "C++ Compiler Version: ${CMAKE_CXX_COMPILER_VERSION}")

add_executable(reComm main.cpp
        src/application/request_handlers/RequestHandleService.h
        src/application/request_handlers/RequestService.h
        src/application/request_handlers/RegisterRequestService.h
        src/application/request_handlers/AuthRequestService.h
        src/application/request_handlers/GroupRequestService.h
        src/application/request_handlers/MessageRequestService.h

        src/application/FriendshipService.h
        src/application/GroupService.h
        src/application/UserService.h
        src/application/JwtService.h

        src/domain/friendship/Friendship.h
        src/domain/friendship/FriendshipRepository.h

        src/domain/group/Group.h
        src/domain/group/GroupRepository.h

        src/domain/user/User.h
        src/domain/user/UserRepository.h

        src/infrastructure/FileUserRepository.h
        src/infrastructure/FileFriendshipRepository.h
        src/infrastructure/FileGroupRepository.h

        src/exceptions/invalid_credentials_error.h
        src/exceptions/user_already_exists_error.h
        src/exceptions/bad_request_format_error.h
        src/exceptions/unknown_method_error.h
        src/exceptions/user_not_found_error.h
        src/exceptions/cannot_be_self_friend_error.h
        src/exceptions/already_friends_error.h
        src/exceptions/friendship_request_already_sent_error.h
        src/exceptions/save_friendship_request_error.h
        src/exceptions/group_not_found_error.h
        src/exceptions/not_group_member_error.h
        src/exceptions/cannot_add_non_friend_to_group_error.h
        src/exceptions/user_already_in_group_error.h
        src/exceptions/cannot_leave_group_as_last_member_error.h
        src/exceptions/friendship_request_not_found_error.h
        src/exceptions/friendship_request_already_processed_error.h
        src/exceptions/friendship_request_process_error.h
        src/exceptions/unauthorized_error.h

        src/utils/Logger.h
        src/domain/message/Message.h
        src/domain/message/MessageRepository.h
        src/infrastructure/FileMessageRepository.h
        src/application/MessageService.h
)

include(FetchContent)
set(JWT_BUILD_TESTS OFF)
set(JWT_BUILD_EXAMPLES OFF)
FetchContent_Declare(
        cli11
        GIT_REPOSITORY https://github.com/CLIUtils/CLI11.git
        GIT_TAG v2.3.2
)
FetchContent_Declare(
        json
        GIT_REPOSITORY https://github.com/nlohmann/json.git
        GIT_TAG v3.12.0
)
FetchContent_Declare(
        uuid_v4
        GIT_REPOSITORY https://github.com/crashoz/uuid_v4.git
        GIT_TAG master
)
FetchContent_Declare(
        jwt-cpp
        GIT_REPOSITORY https://github.com/Thalhammer/jwt-cpp.git
        GIT_TAG v0.7.1
)

FetchContent_MakeAvailable(
        cli11
        json
        uuid_v4
        jwt-cpp
)

find_package(OpenSSL REQUIRED)

target_link_libraries(reComm PRIVATE
        CLI11::CLI11
        nlohmann_json::nlohmann_json
        uuid_v4
        OpenSSL::Crypto
        jwt-cpp::jwt-cpp
)

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU" AND CMAKE_CXX_COMPILER_VERSION VERSION_LESS 9.0)
    target_link_libraries(reComm PRIVATE stdc++fs)
endif()

if (CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif ()