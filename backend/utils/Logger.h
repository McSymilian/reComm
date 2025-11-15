#pragma once

#include <iostream>
#include <chrono>
#include <iomanip>
#include <sstream>
#include <string>

class Logger {
    static constexpr const char* RESET = "\033[0m";
    static constexpr const char* RED = "\033[31m";
    static constexpr const char* YELLOW = "\033[33m";
    inline static int currentVerbalityLevel = 10;
public:
    enum class Level {
        INFO,
        WARNING,
        ERROR
    };

    enum class Importance {
        NONE = 0,
        LOW = 1,
        MEDIUM = 5,
        HIGH = 10
    };

    static void setVerbalityLevel(const int level) {
        currentVerbalityLevel = 10 - level;
    }

    static void log(
        const std::string& message,
        Level level = Level::INFO,
        Importance importanceLevel = Importance::LOW
    ) {
        log(message, static_cast<int>(importanceLevel), level);
    }

    static void log(
        const std::string& message,
        int importanceLevel,
        Level level = Level::INFO
    ) {
        if (importanceLevel < currentVerbalityLevel)
            return;

        auto now = std::chrono::system_clock::now();
        auto time_t = std::chrono::system_clock::to_time_t(now);
        auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()) % 1000;

        std::stringstream ss;
        ss << std::put_time(std::gmtime(&time_t), "%Y-%m-%dT%H:%M:%S")
           << '.' << std::setfill('0') << std::setw(3) << ms.count() << 'Z';

        std::ostream& out = (level == Level::ERROR) ? std::cerr : std::cout;
        
        const char* color = RESET;
        switch(level) {
            case Level::INFO: color = RESET; break;
            case Level::WARNING: color = YELLOW; break;
            case Level::ERROR: color = RED; break;
        }

        out << color << "[" << ss.str() << "] ";
        
        switch(level) {
            case Level::INFO: out << "[INFO] "; break;
            case Level::WARNING: out << "[WARNING] "; break;
            case Level::ERROR: out << "[ERROR] "; break;
        }
        
        out << message << std::endl;
    }
};
