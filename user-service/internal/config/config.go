package config

import (
	"fmt"
	"gopkg.in/yaml.v3"
	"log/slog"
)

import (
	"log"
	"os"
	"time"
)

type DBConfig struct {
	Type     string `yaml:"type"`
	Host     string `yaml:"host"`
	Port     int    `yaml:"port"`
	Name     string `yaml:"name"`
	Password string `yaml:"password"`
	User     string `yaml:"user"`
}

func (cfg DBConfig) RenderURL() string {
	return fmt.Sprintf("%s://%s:%s@%s:%d/%s", cfg.Type, cfg.User, cfg.Password, cfg.Host, cfg.Port, cfg.Name)
}

type HTTPConfig struct {
	Host           string        `yaml:"host"`
	Port           int           `yaml:"port"`
	RequestTimeout time.Duration `yaml:"request_timeout"`
	IdleTimeout    time.Duration `yaml:"idle_timeout"`
}

type LogConfig struct {
	Level      slog.Level `yaml:"level"`
	RenderJSON bool       `yaml:"render_json"`
}

type Config struct {
	DB   DBConfig   `yaml:"db"`
	HTTP HTTPConfig `yaml:"http"`
	Log  LogConfig  `yaml:"log"`
}

func MustLoad() *Config {
	configPath := os.Getenv("CONFIG_PATH")
	if configPath == "" {
		log.Fatal("CONFIG_PATH environment variable not set")
	}

	if _, err := os.Stat(configPath); os.IsNotExist(err) {
		log.Fatalf("Config file does not exist: %s", configPath)
	}

	f, err := os.Open(configPath)
	if err != nil {
		log.Fatalf("Unable to open config file: %s", configPath)
	}

	var cfg Config
	decoder := yaml.NewDecoder(f)

	if err := decoder.Decode(&cfg); err != nil {
		log.Fatalf("Unable to parse config file: %s", configPath)
	}

	return &cfg
}
