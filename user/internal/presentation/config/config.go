package config

import (
	db "user/internal/infrastructure/db/config"
	logger "user/internal/infrastructure/logger/config"
	api "user/internal/presentation/api/config"
)

type Config struct {
	db.DBConfig         `toml:"db"`
	api.APIConfig       `toml:"api"`
	logger.LoggerConfig `toml:"logging"`
}
