package config

import "time"

type APIConfig struct {
	Host           string        `toml:"host"`
	Port           int           `toml:"port"`
	RequestTimeout time.Duration `toml:"request_timeout"`
	IdleTimeout    time.Duration `toml:"idle_timeout"`
	BaseURLPrefix  string        `toml:"base_url_prefix"`
}
