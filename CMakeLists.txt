cmake_minimum_required(VERSION 3.28)
project(reComm)

set(CMAKE_CXX_STANDARD 20)
add_executable(reComm main.cpp
        domain/User.h
        domain/UserRepository.h
        application/UserService.h
        infrastructure/FileUserRepository.h
        infrastructure/FileUserRepository.h)

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
