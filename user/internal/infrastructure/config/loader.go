package config

import (
	"github.com/BurntSushi/toml"
	"os"
)

const DefaultConfigPath = "./configs/config.toml"

func LoadConfig(val interface{}) {
	configPath := getEnv("CONFIG_PATH", DefaultConfigPath)
	_, err := toml.DecodeFile(configPath, val)
	if err != nil {
		panic(err)
	}
}

func getEnv(key string, defaultVal string) string {
	if value, exists := os.LookupEnv(key); exists {
		return value
	}
	return defaultVal
}
