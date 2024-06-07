package config

import (
	load "user/internal/infrastructure/config"
	db "user/internal/infrastructure/db/config"
	logger "user/internal/infrastructure/logger/config"
	api "user/internal/presentation/api/config"
)

func NewConfig() Config {
	var conf Config
	load.LoadConfig(&conf)
	return conf
}

func NewDBConfig(config Config) db.DBConfig {
	return config.DBConfig
}

func NewAPIConfig(config Config) api.APIConfig {
	return config.APIConfig
}

func NewLoggerConfig(config Config) logger.LoggerConfig {
	return config.LoggerConfig
}
