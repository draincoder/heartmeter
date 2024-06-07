package config

import (
	"fmt"
)

type DBConfig struct {
	Host              string `toml:"host"`
	Port              int    `toml:"port"`
	Database          string `toml:"database"`
	User              string `toml:"user"`
	Password          string `toml:"password"`
	MaxIdleConnection int    `toml:"max_idle_connection"`
}

func (conf *DBConfig) RenderURL() string {
	return fmt.Sprintf("postgres://%s:%s@%s:%d/%s",
		conf.User, conf.Password, conf.Host, conf.Port, conf.Database,
	)
}
