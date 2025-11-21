#pragma once
#include "../domain/user/UserRepository.h"
#include <nlohmann/json.hpp>
#include <fstream>

#if __has_include(<filesystem>)
    #include <filesystem>
    namespace fs = std::filesystem;
#elif __has_include(<experimental/filesystem>)
    #include <experimental/filesystem>
    namespace fs = std::experimental::filesystem;
#else
    #error "No filesystem support"
#endif

class FileUserRepository final : public UserRepository {
    fs::path filePath;
    static constexpr std::string DB_FILE = "users.json";
    
    nlohmann::json loadData() const {
        if(!fs::exists(filePath)) {
            return nlohmann::json::array();
        }
        
        std::ifstream file(filePath);
        nlohmann::json data;
        file >> data;
        return data;
    }
    
    void saveData(const nlohmann::json& data) const {
        std::ofstream file(filePath);
        file << data.dump(2);
    }
    
public:
    explicit FileUserRepository(const std::string& path) {
        if (path.back() == '/')
            filePath = path + DB_FILE;
        else
            filePath = path + '/' + DB_FILE;
    }
    
    bool save(const User& user) override {
        auto data = loadData();
        for(auto& item : data) {
            if(item["username"] == user.username) {
                item = user.toJson();
                saveData(data);
                return true;
            }
        }

        data.push_back(user.toJson());
        saveData(data);
        return true;
    }
    
    std::optional<User> findByUsername(const std::string& username) override {
        auto data = loadData();
        
        for(const auto& item : data) {
            if(item["username"] == username) {
                return User::fromJson(item);
            }
        }
        
        return std::nullopt;
    }
    
    std::vector<User> findAll() override {
        auto data = loadData();
        std::vector<User> users;
        
        for(const auto& item : data) {
            users.push_back(User::fromJson(item));
        }
        
        return users;
    }

    bool exists(const std::string& username) override {
        return findByUsername(username).has_value();
    }

    bool exists(const UUIDv4::UUID &uuid) override {
        return findByUUID(uuid).has_value();
    }

    std::optional<User> findByUUID(const UUIDv4::UUID &uuid) override {
        auto data = loadData();

        for(const auto& item : data) {
            if(item["uuid"] == uuid.str()) {
                return User::fromJson(item);
            }
        }

        return std::nullopt;
    }
};
