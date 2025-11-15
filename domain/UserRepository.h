#pragma once
#include "User.h"
#include <optional>
#include <vector>

class UserRepository {
public:
    virtual ~UserRepository() = default;
    
    virtual bool save(const User& user) = 0;
    virtual std::optional<User> findByUsername(const std::string& username) = 0;
    virtual std::vector<User> findAll() = 0;
    virtual bool exists(const std::string& uuid) = 0;
};
